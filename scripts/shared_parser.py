import re
import json
from pathlib import Path

# ---------- helpers ----------

def extract_expressions(text: str):
    """Extrai conteúdos entre {{ ... }} preservando quebras (n8n-style)."""
    return re.findall(r"{{\s*([^{}]+?)\s*}}", text or "", flags=re.DOTALL)

def find_node_refs(expr: str):
    """Detecta referências a outros nós dentro de uma expressão."""
    refs = []
    # $node["Nome do Nó"]
    for m in re.finditer(r'\$node\[\s*"(.*?)"\s*\]', expr):
        refs.append(("node", m.group(1)))
    # marcadores comuns do n8n (não contam como dependência, mas registramos)
    if "$json" in expr:     refs.append(("json", "$json"))
    if "$prevNode" in expr: refs.append(("prevNode", "$prevNode"))
    if "$flow" in expr:     refs.append(("flow", "$flow"))
    if "$binary" in expr:   refs.append(("binary", "$binary"))
    if "$now" in expr:      refs.append(("now", "$now"))
    for m in re.finditer(r'\$env\.([A-Za-z_][A-Za-z0-9_]*)', expr):
        refs.append(("env", m.group(1)))
    return refs

def looks_like_sql(s: str):
    if not isinstance(s, str): return False
    t = s.strip().lower()
    return any(k in t for k in ["select ", "insert into", "update ", "delete from"])

def collect_sql_tables(sql: str):
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", sql or "")
    keywords = set('select,insert,into,update,delete,from,where,join,left,right,inner,outer,on,group,by,order,limit,values,set,returning'.split(','))
    return [t for t in tokens if t.lower() not in keywords]

def get_connections(connection_obj):
    """Converte o objeto 'connections' do n8n em lista de arestas (from, to, path)."""
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

# ---------- parse workflows ----------

def parse_workflows(input_dir: Path):
    """
    Lê todos os JSONs do diretório de input.
    - Varre TODO o nó (não só parameters) para achar {{expressões}} e SQL
    - Extrai nós, arestas, expressões, sql e blocos de código
    """

    def walk_dict(d, path="$"):
        if isinstance(d, dict):
            for k, v in d.items():
                yield from walk_dict(v, f"{path}.{k}")
        elif isinstance(d, list):
            for i, v in enumerate(d):
                yield from walk_dict(v, f"{path}[{i}]")
        else:
            yield path, d

    nodes_all, edges_all, expr_all, sql_all, code_all = [], [], [], [], []

    for jf in input_dir.glob("*.json"):
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[WARN] Falha ao ler {jf.name}: {e}")
            continue

        # pode ser um workflow único (dict) ou uma lista de workflows
        workflows = []
        if isinstance(data, dict) and "nodes" in data and "connections" in data:
            workflows = [data]
        elif isinstance(data, list):
            workflows = [w for w in data if isinstance(w, dict) and "nodes" in w]

        for wf in workflows:
            wfname = wf.get("name") or jf.stem
            nodes = wf.get("nodes", [])
            conns = wf.get("connections", {})

            # Nós + varredura de expressões/SQL
            for n in nodes:
                nodes_all.append({
                    "workflow": wfname,
                    "id": n.get("id",""),
                    "name": n.get("name",""),
                    "type": n.get("type",""),
                    "disabled": n.get("disabled", False),
                })

                # procura {{...}} e SQL em QUALQUER campo do nó
                for path, val in walk_dict(n, "$.node"):
                    if isinstance(val, str):
                        # expressões
                        for expr in extract_expressions(val):
                            refs = find_node_refs(expr)
                            expr_all.append({
                                "workflow": wfname,
                                "node": n.get("name",""),
                                "param_path": path,
                                "expression": expr.strip(),
                                "refs": ", ".join([f"{k}:{v}" for k,v in refs]) if refs else ""
                            })
                        # SQL
                        if looks_like_sql(val):
                            sql_all.append({
                                "workflow": wfname,
                                "node": n.get("name",""),
                                "param_path": path,
                                "sql_excerpt": (val.strip()[:400] + "...") if len(val) > 400 else val.strip(),
                                "tables_guess": ", ".join(sorted(set(collect_sql_tables(val))))[:200]
                            })

                # blocos de código comuns
                for key in ["functionCode", "jsCode", "code"]:
                    code = n.get("parameters", {}).get(key)
                    if isinstance(code, str) and code.strip():
                        code_all.append({
                            "workflow": wfname,
                            "node": n.get("name",""),
                            "param_key": key,
                            "loc": len(code.splitlines()),
                            "excerpt": (code.strip()[:400] + "...") if len(code) > 400 else code.strip()
                        })

            # Conexões -> arestas
            for a, b, ptype in get_connections(conns):
                edges_all.append({
                    "workflow": wfname,
                    "from": a,
                    "to": b,
                    "path": ptype
                })

    return nodes_all, edges_all, expr_all, sql_all, code_all

# ---------- render helpers ----------

def mermaid_from_edges(edges):
    """
    Gera Mermaid flowchart com IDs seguros.
    Mostra o nome real do nó como rótulo e usa o path como label da aresta.
    """
    # lista de nós únicos
    nodes = []
    for e in edges:
        nodes.append(e["from"])
        nodes.append(e["to"])
    uniq, seen = [], set()
    for n in nodes:
        if n not in seen:
            uniq.append(n); seen.add(n)

    # IDs seguros n1, n2, ...
    id_map = {name: f"n{i+1}" for i, name in enumerate(uniq)}

    def esc_label(s: str) -> str:
        return str(s).replace('"', '\\"').replace("`", "\\`")

    lines = ["flowchart LR"]

    # declara nós
    for name, nid in id_map.items():
        lines.append(f'{nid}["{esc_label(name)}"]')

    # arestas
    for e in edges:
        a = id_map[e["from"]]
        b = id_map[e["to"]]
        lbl = str(e.get("path", "") or "").replace("|", "\\|")
        if lbl:
            lines.append(f"{a} --|{lbl}|--> {b}")
        else:
            lines.append(f"{a} --> {b}")

    return "\n".join(lines)

def md_table(rows, headers):
    """Tabela Markdown com escape básico para '|' e quebras de linha."""
    if not rows:
        return "| (vazio) |\n|---|\n"
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"
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

# ---------- impacto ----------

def _direct_impact_maps(expr_rows, edges_rows):
    """
    Retorna:
      impact_map: dict[source_node] -> list[(workflow, affected_node, where)]
      adj: dict[source_node] -> set(affected_node)  (para BFS)
    """
    from collections import defaultdict
    impact_map = defaultdict(list)
    adj = defaultdict(set)

    # 1) EXPRESSÕES ($node["X"]) -> alterar X impacta 'node' que usa X
    for er in expr_rows:
        node = er.get("node","") or ""
        wfk  = er.get("workflow","") or ""
        refs = (er.get("refs","") or "").split(",")
        for piece in refs:
            piece = piece.strip()
            if piece.startswith("node:"):
                src = piece.split(":",1)[1]
                if src and src != node:
                    impact_map[src].append((wfk, node, er.get("param_path","")))
                    adj[src].add(node)

    # 2) CONEXÕES (A -> B) -> alterar A impacta diretamente B
    for e in edges_rows:
        wfk = e.get("workflow","") or ""
        a   = e.get("from","") or ""
        b   = e.get("to","") or ""
        p   = e.get("path","") or "connection"
        if a and b:
            impact_map[a].append((wfk, b, f"(edge:{p})"))
            adj[a].add(b)

    return impact_map, adj

def _transitive_levels(adj, start, max_depth=3):
    """
    BFS por níveis: retorna [ [nivel1], [nivel2], ... ] até max_depth.
    Não repete nós já vistos.
    """
    from collections import deque
    seen = {start}
    q = deque([(start, 0)])
    levels = [[] for _ in range(max_depth)]

    while q:
        u, d = q.popleft()
        if d == max_depth: 
            continue
        for v in sorted(adj.get(u, [])):
            if v in seen: 
                continue
            seen.add(v)
            levels[d].append(v)           # d=0 -> nível 1 a partir de start
            q.append((v, d+1))
    # remove níveis vazios no fim
    while levels and not levels[-1]:
        levels.pop()
    return levels

def build_impact(expr_rows, edges_rows, show_levels=3):
    """
    Matriz de impacto combinando:
      - Expressões ($node["..."])
      - Conexões (A -> B)
    E exibe uma cadeia transitiva (nível 1..N) expansível via <details>.
    """
    impact_map, adj = _direct_impact_maps(expr_rows, edges_rows)

    lines = ["# Matriz de Impacto (What-if)\n"]

    if not impact_map:
        lines.append("_Nenhuma referência entre nós foi detectada nas expressões ou conexões._\n")
        return "\n".join(lines)

    # Índice lateral (para MkDocs gerar TOC bonito já está ok),
    # aqui só garantimos ordenação estável:
    for target in sorted(impact_map.keys()):
        lines.append(f"## Se você alterar **{target}**\n")

        # Tabela de impacto direto
        lines.append("| Workflow | Nó afetado | Onde |")
        lines.append("|---|---|---|")
        for w, node, where in sorted(impact_map[target], key=lambda x: (x[0], x[1], x[2])):
            lines.append(f"| {w} | {node} | `{where}` |")
        lines.append("")

        # Cadeia transitiva (níveis)
        levels = _transitive_levels(adj, target, max_depth=show_levels)
        if levels:
            lines.append("<details><summary><strong>Ver cadeia completa (efeito dominó)</strong></summary>\n")
            for i, lvl in enumerate(levels, start=1):
                if not lvl: 
                    continue
                items = ", ".join(lvl)
                lines.append(f"- **Nível {i}** → {items}")
            lines.append("\n</details>\n")

    return "\n".join(lines)
