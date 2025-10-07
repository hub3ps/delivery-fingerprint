#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
from generate_tenant import generate_for_tenant

ROOT = Path(__file__).resolve().parent.parent
TENANTS = ROOT / "tenants"
DOCS = ROOT / "docs"

tenants = [p.name for p in TENANTS.glob("*") if (p/"input").exists()]
for t in tenants:
    generate_for_tenant(t)

mk = (ROOT/"mkdocs.yml").read_text(encoding="utf-8").splitlines()
nav_lines, in_clients = [], False
for line in mk:
    if line.strip().startswith("- Clientes:"):
        in_clients = True
        nav_lines.append(line)
        for t in sorted(tenants):
            nav_lines.append(f"    - {t}: clients/{t}/index.md")
        continue
    if in_clients:
        if not line.startswith("    "):
            in_clients = False
            nav_lines.append(line)
        else:
            pass
    else:
        nav_lines.append(line)
(ROOT/"mkdocs.yml").write_text("\n".join(nav_lines), encoding="utf-8")

index = ["# Overview\n"]
if not tenants:
    index.append("\n_Nenhum cliente com `input/` encontrado. Adicione exports em `tenants/<cliente>/input/`._\n")
else:
    index.append("\n## Clientes\n")
    for t in sorted(tenants):
        index.append(f"- [{t}](clients/{t}/index.md)")
(DOCS/"index.md").write_text("\n".join(index), encoding="utf-8")

print("OK - Tenants:", tenants)
