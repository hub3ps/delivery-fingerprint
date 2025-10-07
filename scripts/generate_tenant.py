#!/usr/bin/env python3
import yaml
from pathlib import Path
from shared_parser import parse_workflows, mermaid_from_edges, md_table, build_impact

TENANTS_DIR = Path(__file__).resolve().parent.parent / "tenants"
DOCS_DIR    = Path(__file__).resolve().parent.parent / "docs" / "clients"

def generate_for_tenant(tenant: str):
    tdir = TENANTS_DIR / tenant
    input_dir = tdir / "input"
    config = {"name": tenant, "description": ""}
    if (tdir/"config.yml").exists():
        config.update(yaml.safe_load((tdir/"config.yml").read_text(encoding="utf-8")) or {})

    nodes, edges, exprs, sqls, codes = parse_workflows(input_dir)

    cdir = DOCS_DIR / tenant
    cdir.mkdir(parents=True, exist_ok=True)

    (cdir/"index.md").write_text(
f"""# {config.get('name', tenant)}

{config.get('description','').strip()}

- [Grafo](grafo.md)
- [Nós](tabelas/nodes.md) • [Conexões](tabelas/edges.md) • [Expressões](tabelas/expressions.md) • [SQL](tabelas/sql.md) • [Código](tabelas/code.md)
- [Impacto](impacto.md)
""", encoding="utf-8")

    grafo = mermaid_from_edges(edges)
    (cdir/"grafo.md").write_text("# Grafo de Dependências\n\n```mermaid\n"+grafo+"\n```\n", encoding="utf-8")

    tdir_docs = cdir/"tabelas"
    tdir_docs.mkdir(parents=True, exist_ok=True)
    def write_table(path, rows, headers, title):
        (tdir_docs/path).write_text("# "+title+"\n\n"+md_table(rows, headers)+"\n", encoding="utf-8")

    write_table("nodes.md", nodes, ["workflow","id","name","type","disabled"], "Nós")
    write_table("edges.md", edges, ["workflow","from","to","path"], "Conexões")
    write_table("expressions.md", exprs, ["workflow","node","param_path","expression","refs"], "Expressões")
    write_table("sql.md", sqls, ["workflow","node","param_path","sql_excerpt","tables_guess"], "SQL")
    write_table("code.md", codes, ["workflow","node","param_key","loc","excerpt"], "Código")

    (cdir/"impacto.md").write_text(build_impact(exprs), encoding="utf-8")

if __name__ == "__main__":
    for t in sorted(p.name for p in (Path(__file__).resolve().parent.parent / "tenants").glob("*") if p.is_dir()):
        if (Path(__file__).resolve().parent.parent / "tenants" / t / "input").exists():
            generate_for_tenant(t)
