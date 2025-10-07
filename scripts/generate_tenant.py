#!/usr/bin/env python3
import yaml
from pathlib import Path
from shared_parser import parse_workflows, mermaid_from_edges, md_table, build_impact

ROOT_DIR   = Path(__file__).resolve().parent.parent
TENANTS_DIR = ROOT_DIR / "tenants"
DOCS_DIR    = ROOT_DIR / "docs" / "clients"


def generate_for_tenant(tenant: str):
    """
    Gera a documentação para um tenant específico (cliente ou conjunto de fluxos).
    Espera encontrar exports JSON em: tenants/<tenant>/input/*.json
    Escreve páginas em: docs/clients/<tenant>/
    """
    tdir = TENANTS_DIR / tenant
    input_dir = tdir / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    # Metadados opcionais do tenant (título/descrição)
    config = {"name": tenant, "description": ""}
    cfg_path = tdir / "config.yml"
    if cfg_path.exists():
        try:
            cfg_data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
            config.update(cfg_data)
        except Exception as e:
            print(f"[WARN] Falha ao ler {cfg_path}: {e}")

    # Parse dos workflows (nós, arestas, expressões, sql, código)
    nodes, edges, exprs, sqls, codes = parse_workflows(input_dir)

    # Pastas de saída
    cdir = DOCS_DIR / tenant
    cdir.mkdir(parents=True, exist_ok=True)
    tabdir = cdir / "tabelas"
    tabdir.mkdir(parents=True, exist_ok=True)

    # ---------- index ----------
    (cdir / "index.md").write_text(
        f"""# {config.get('name', tenant)}

{(config.get('description') or '').strip()}

- [Grafo](grafo.md)
- [Nós](tabelas/nodes.md) • [Conexões](tabelas/edges.md) • [Expressões](tabelas/expressions.md) • [SQL](tabelas/sql.md) • [Código](tabelas/code.md)
- [Impacto](impacto.md)
""",
        encoding="utf-8",
    )

    # ---------- grafo ----------
    grafo = mermaid_from_edges(edges)
    (cdir / "grafo.md").write_text(
        "# Grafo de Dependências\n\n```mermaid\n" + grafo + "\n```\n",
        encoding="utf-8",
    )

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
