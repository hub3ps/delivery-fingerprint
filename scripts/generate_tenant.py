#!/usr/bin/env python3
import yaml
from pathlib import Path
from shared_parser import parse_workflows, mermaid_from_edges, md_table, build_impact

ROOT_DIR   = Path(__file__).resolve().parent.parent
TENANTS_DIR = ROOT_DIR / "tenants"
DOCS_DIR    = ROOT_DIR / "docs" / "clients"

def generate_for_tenant(tenant: str):
    from shared_parser import parse_workflows, mermaid_from_edges, md_table, build_impact
    import re

    def slug(s: str):
        s = re.sub(r"\s+", "-", s.strip())
        s = re.sub(r"[^A-Za-z0-9\-_]", "", s)
        return s.lower() or "node"

    tdir = TENANTS_DIR / tenant
    input_dir = tdir / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    # Metadados opcionais
    config = {"name": tenant, "description": ""}
    cfg_path = tdir / "config.yml"
    if cfg_path.exists():
        try:
            cfg_data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
            config.update(cfg_data)
        except Exception as e:
            print(f"[WARN] Falha ao ler {cfg_path}: {e}")

    # Parse tudo
    nodes, edges, exprs, sqls, codes = parse_workflows(input_dir)

    # Pastas destino
    base = DOCS_DIR / tenant
    base.mkdir(parents=True, exist_ok=True)

    tabdir = base / "tabelas"
    tabdir.mkdir(parents=True, exist_ok=True)

    nodes_dir = base / "nodes"
    nodes_dir.mkdir(parents=True, exist_ok=True)

    # ---------- Index do cliente ----------
    (base / "index.md").write_text(
        f"""# {config.get('name', tenant)}

{(config.get('description') or '').strip()}

- [Grafo](grafo.md)
- [Nós](nodes/index.md)
- [Conexões](tabelas/edges.md) • [Expressões](tabelas/expressions.md) • [SQL](tabelas/sql.md) • [Código](tabelas/code.md)
- [Impacto](impacto.md)
""",
        encoding="utf-8",
    )

    # ---------- Grafo ----------
    grafo = mermaid_from_edges(edges, rankdir="TB")
    (base / "grafo.md").write_text("# Grafo de Dependências\n\n```mermaid\n" + grafo + "\n```\n", encoding="utf-8")

    # ---------- Tabelas cruas ----------
    def write_table(relpath: str, rows: list, headers: list, title: str):
        (tabdir / relpath).write_text("# " + title + "\n\n" + md_table(rows, headers) + "\n", encoding="utf-8")

    write_table("nodes.md",       nodes, ["workflow", "id", "name", "type", "disabled"], "Nós")
    write_table("edges.md",       edges, ["workflow", "from", "to", "path"],            "Conexões")
    write_table("expressions.md", exprs, ["workflow", "node", "param_path", "expression", "refs"], "Expressões")
    write_table("sql.md",         sqls,  ["workflow", "node", "param_path", "sql_excerpt", "tables_guess"], "SQL")
    write_table("code.md",        codes, ["workflow", "node", "param_key", "loc", "excerpt"], "Código")

    # ---------- Índice de Nós ----------
    # agrupamentos de dados por nó
    expr_by_node = {}
    for r in exprs:
        expr_by_node.setdefault(r["node"], []).append(r)

    sql_by_node = {}
    for r in sqls:
        sql_by_node.setdefault(r["node"], []).append(r)

    code_by_node = {}
    for r in codes:
        code_by_node.setdefault(r["node"], []).append(r)

    # mapa de filhos por arestas (A -> B)
    children = {}
    for e in edges:
        a, b = e["from"], e["to"]
        children.setdefault(a, set()).add(b)

    # cria página por nó
    created = []
    for n in sorted({r["name"] for r in nodes}):
        s = slug(n)
        p = nodes_dir / f"{s}.md"

        sections = []
        sections.append(f"# {n}\n")

        # Onde este nó impacta diretamente (saídas)
        outs = sorted(children.get(n, []))
        if outs:
            sections.append("## Impacta diretamente\n")
            for o in outs:
                sections.append(f"- {o}")
            sections.append("")

        # Expressões neste nó
        if expr_by_node.get(n):
            sections.append("## Expressões\n")
            sections.append("| Caminho | Expressão | Refs |")
            sections.append("|---|---|---|")
            for r in expr_by_node[n]:
                sections.append(f"| `{r.get('param_path','')}` | `{r.get('expression','')}` | `{r.get('refs','')}` |")
            sections.append("")

        # SQL neste nó
        if sql_by_node.get(n):
            sections.append("## SQL\n")
            for r in sql_by_node[n]:
                sections.append(f"**{r.get('param_path','')}**\n\n```sql\n{r.get('sql_excerpt','')}\n```\n")
            sections.append("")

        # Código neste nó
        if code_by_node.get(n):
            sections.append("## Código\n")
            for r in code_by_node[n]:
                sections.append(f"**{r.get('param_key','')}** ({r.get('loc',0)} linhas)\n\n```js\n{r.get('excerpt','')}\n```\n")
            sections.append("")

        p.write_text("\n".join(sections), encoding="utf-8")
        created.append((n, s))

    # index dos nós (lista clicável)
    lines = ["# Nós\n", "_Abra um nó para ver expressões, código e impacto direto._\n"]
    for n, s in created:
        lines.append(f"- [{n}]({s}.md)")
    (nodes_dir / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---------- Submenu para Atendente (filhos diretos) ----------
    # cria uma pasta Atendente/ com stubs linkando para as páginas originais
    atendente = "Atendente"
    if atendente in children:
        att_dir = nodes_dir / atendente
        att_dir.mkdir(parents=True, exist_ok=True)

        # .pages para o grupo Atendente
        (att_dir / ".pages").write_text("title: Atendente (Ferramentas)\n", encoding="utf-8")

        # stubs que redirecionam/logicamente para a página do nó filho original
        for child in sorted(children[atendente]):
            # encontra o slug do filho já criado
            try:
                slug_child = next(s for (nn, s) in created if nn == child)
            except StopIteration:
                continue
            (att_dir / f"{slug(child)}.md").write_text(
                f"# {child}\n\nVeja a página principal deste nó: [abrir](/clients/{tenant}/nodes/{slug_child}.md)\n",
                encoding="utf-8"
            )

    # ---------- .pages para ordenar menu “Nós” e destacar Atendente ----------
    (nodes_dir / ".pages").write_text(
        "title: Nós\narrange:\n  - Atendente\n  - index.md\n  - '*'\n",
        encoding="utf-8",
    )

    # ---------- Impacto (direto + árvore colapsável) ----------
    (base / "impacto.md").write_text(build_impact(exprs, edges), encoding="utf-8")

    # ---------- tabelas ----------
    def write_table(relpath: str, rows: list, headers: list, title: str):
        (tabdir / relpath).write_text("# " + title + "\n\n" + md_table(rows, headers) + "\n", encoding="utf-8")

    write_table("nodes.md",       nodes, ["workflow", "id", "name", "type", "disabled"], "Nós")
    write_table("edges.md",       edges, ["workflow", "from", "to", "path"],            "Conexões")
    write_table("expressions.md", exprs, ["workflow", "node", "param_path", "expression", "refs"], "Expressões")
    write_table("sql.md",         sqls,  ["workflow", "node", "param_path", "sql_excerpt", "tables_guess"], "SQL")
    write_table("code.md",        codes, ["workflow", "node", "param_key", "loc", "excerpt"], "Código")

    # ---------- impacto (expressões + conexões) ----------
    (cdir / "impacto.md").write_text(build_impact(exprs, edges), encoding="utf-8")


if __name__ == "__main__":
    # Gera para todos os tenants que tenham a pasta input/
    tenants = [p.name for p in TENANTS_DIR.glob("*") if (p / "input").exists()]
    for t in sorted(tenants):
        generate_for_tenant(t)
