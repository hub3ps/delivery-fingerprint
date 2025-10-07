
import re, json
from pathlib import Path

def walk_dict(d, path="$"):
    if isinstance(d, dict):
        for k, v in d.items():
            yield from walk_dict(v, f"{path}.{k}")
    elif isinstance(d, list):
        for i, v in enumerate(d):
            yield from walk_dict(v, f"{path}[{i}]")
    else:
        yield path, d

def extract_expressions(text: str):
    return re.findall(r"{{\s*([^{}]+?)\s*}}", text or "", flags=re.DOTALL)

def find_node_refs(expr: str):
    refs = []
    for m in re.finditer(r'\$node\[\s*"(.*?)"\s*\]', expr):
        refs.append(("node", m.group(1)))
    if "$json" in expr: refs.append(("json", "$json"))
    if "$prevNode" in expr: refs.append(("prevNode", "$prevNode"))
    for m in re.finditer(r'\$env\.([A-Za-z_][A-Za-z0-9_]*)', expr):
        refs.append(("env", m.group(1)))
    if "$flow" in expr: refs.append(("flow", "$flow"))
    if "$binary" in expr: refs.append(("binary", "$binary"))
    if "$now" in expr: refs.append(("now", "$now"))
    return refs

def looks_like_sql(s: str):
    if not isinstance(s, str): return False
    snip = s.strip().lower()
    return any(k in snip for k in ["select ","insert into","update ","delete from"])

def collect_sql_tables(sql: str):
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", sql or "")
    keywords = set('select,insert,into,update,delete,from,where,join,left,right,inner,outer,on,group,by,order,limit,values,set,returning'.split(','))
    return [t for t in tokens if t.lower() not in keywords]

def get_connections(connection_obj):
    edges = []
    if not isinstance(connection_obj, dict): return edges
    for from_name, paths in connection_obj.items():
        if not isinstance(paths, dict): continue
        for path, connlists in paths.items():
            if not isinstance(connlists, list): continue
            for connlist in connlists:
                if not isinstance(connlist, list): continue
                for c in connlist:
                    to_name = c.get("node")
                    if to_name:
                        edges.append((from_name, to_name, path))
    return edges

def parse_workflows(input_dir: Path):
    nodes_all, edges_all, expr_all, sql_all, code_all = [], [], [], [], []
    for jf in input_dir.glob("*.json"):
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[WARN] Falha ao ler {jf.name}: {e}")
            continue

        workflows = []
        if isinstance(data, dict) and "nodes" in data and "connections" in data:
            workflows = [data]
        elif isinstance(data, list):
            workflows = [w for w in data if isinstance(w, dict) and "nodes" in w]

        for wf in workflows:
            wfname = wf.get("name") or jf.stem
            nodes = wf.get("nodes", [])
            conns = wf.get("connections", {})
            for n in nodes:
                nodes_all.append({
                    "workflow": wfname,
                    "id": n.get("id",""),
                    "name": n.get("name",""),
                    "type": n.get("type",""),
                    "disabled": n.get("disabled", False),
                })
                params = n.get("parameters", {})
                for path, val in walk_dict(params, "$.parameters"):
                    if isinstance(val, str):
                        for expr in extract_expressions(val):
                            refs = find_node_refs(expr)
                            expr_all.append({
                                "workflow": wfname,
                                "node": n.get("name",""),
                                "param_path": path,
                                "expression": expr.strip(),
                                "refs": ", ".join([f"{k}:{v}" for k,v in refs]) if refs else ""
                            })
                        if looks_like_sql(val):
                            sql_all.append({
                                "workflow": wfname,
                                "node": n.get("name",""),
                                "param_path": path,
                                "sql_excerpt": (val.strip()[:400] + "...") if len(val) > 400 else val.strip(),
                                "tables_guess": ", ".join(sorted(set(collect_sql_tables(val))))[:200]
                            })
                for key in ["functionCode","jsCode","code"]:
                    code = n.get("parameters", {}).get(key)
                    if isinstance(code, str) and code.strip():
                        code_all.append({
                            "workflow": wfname,
                            "node": n.get("name",""),
                            "param_key": key,
                            "loc": len(code.splitlines()),
                            "excerpt": (code.strip()[:400] + "...") if len(code) > 400 else code.strip()
                        })
            for a,b,ptype in get_connections(conns):
                edges_all.append({
                    "workflow": wfname,
                    "from": a,
                    "to": b,
                    "path": ptype
                })
    return nodes_all, edges_all, expr_all, sql_all, code_all

def mermaid_from_edges(edges):
    lines = ["flowchart LR"]
    for e in edges:
        a = e["from"].replace('"', "'")
        b = e["to"].replace('"', "'")
        lbl = e.get("path","main")
        lines.append(f'    "{a}" -- {lbl} --> "{b}"')
    return "\n".join(lines) if len(lines) > 1 else "flowchart LR\n"

def md_table(rows, headers):
    if not rows:
        return "| (vazio) |\n|---|\n"
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join(["---"]*len(headers)) + " |"
    lines = [header_line, sep_line]
    for r in rows[:5000]:
        cells = []
        for h in headers:
            v = str(r.get(h, ""))
            v = v.replace("\n", " ").replace("|", "\\|")
            cells.append(v)
        lines.append("| " + " | ".join(cells) + " |")
    if len(rows) > 5000:
        lines.append(f"\n> Mostrando 5000 de {len(rows)} linhas.")
    return "\n".join(lines)

def build_impact(expr_rows):
    from collections import defaultdict
    impact = defaultdict(list)
    for er in expr_rows:
        refs = er.get("refs","")
        node = er.get("node","")
        wfk = er.get("workflow","")
        for piece in refs.split(","):
            piece = piece.strip()
            if piece.startswith("node:"):
                target = piece.split(":",1)[1]
                if target and target != node:
                    impact[target].append((wfk, node, er.get("param_path","")))
    lines = ["# Matriz de Impacto (What-if)\n"]
    if not impact:
        lines.append("_Nenhuma referência entre nós foi detectada nas expressões._\n")
    else:
        for target, refs in sorted(impact.items()):
            lines.append(f"## Se você alterar **{target}**\n")
            lines.append("| Workflow | Nó afetado | Onde (param_path) |")
            lines.append("|---|---|---|")
            for w, node, path in refs:
                lines.append(f"| {w} | {node} | `{path}` |")
            lines.append("")
    return "\n".join(lines)
