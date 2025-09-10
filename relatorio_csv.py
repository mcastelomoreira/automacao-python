#!/usr/bin/env python3
"""
relatorio_csv.py — Gera um relatório simples a partir de um CSV.

Uso:
  python relatorio_csv.py caminho/arquivo.csv [--out relatorio.md]

- Detecta delimitador automaticamente.
- Mostra contagem de linhas, colunas, amostra e resumo numérico (min, max, média, soma).
- Exporta para Markdown se --out for informado; caso contrário, imprime no console.

Exemplos:
  python relatorio_csv.py data/vendas_exemplo.csv
  python relatorio_csv.py data/vendas_exemplo.csv --out data/relatorio_vendas.md
"""
from __future__ import annotations
import argparse
import csv
import io
from pathlib import Path
from statistics import mean
from typing import List

def sniff_dialect(sample_bytes: bytes):
    try:
        dialect = csv.Sniffer().sniff(sample_bytes.decode("utf-8", errors="ignore"))
        return dialect
    except Exception:
        return csv.excel

def is_float(x: str) -> bool:
    try:
        float(x.replace(",", "."))
        return True
    except Exception:
        return False

def to_float(x: str) -> float:
    return float(x.replace(",", "."))

def summarize_numeric(values: List[str]):
    nums = [to_float(v) for v in values if is_float(v)]
    if not nums:
        return None
    from statistics import mean
    return {"count": len(nums), "min": min(nums), "max": max(nums), "mean": mean(nums), "sum": sum(nums)}

def make_report(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    raw = path.read_bytes()
    dialect = sniff_dialect(raw[:4096])
    f = io.StringIO(raw.decode("utf-8", errors="ignore"))
    reader = csv.reader(f, dialect)
    rows = list(reader)
    if not rows:
        return "# Relatório CSV\n\nArquivo vazio."
    header = rows[0]
    data = rows[1:]
    n_rows = len(data)
    n_cols = len(header)
    sample_lines = data[:5]

    summaries = {}
    for idx, col in enumerate(header):
        col_values = [r[idx] for r in data if len(r) > idx]
        num_summary = summarize_numeric(col_values)
        if num_summary:
            summaries[col] = num_summary

    md = io.StringIO()
    md.write(f"# Relatório CSV — {path.name}\n\n")
    md.write(f"- Linhas (dados): **{n_rows}**\n")
    md.write(f"- Colunas: **{n_cols}** → {', '.join(header)}\n\n")

    if summaries:
        md.write("## Resumo Numérico por Coluna\n\n")
        md.write("| Coluna | Count | Min | Max | Média | Soma |\n")
        md.write("|-------:|------:|----:|----:|------:|-----:|\n")
        for col, s in summaries.items():
            md.write(f"| {col} | {s['count']} | {s['min']:.2f} | {s['max']:.2f} | {s['mean']:.2f} | {s['sum']:.2f} |\n")
        md.write("\n")

    md.write("## Amostra (até 5 linhas)\n\n")
    md.write("| " + " | ".join(header) + " |\n")
    md.write("|" + "|".join(['---'] * len(header)) + "|\n")
    for r in sample_lines:
        cells = [c.replace('|', '\\|') for c in r] + [""] * (len(header)-len(r))
        md.write("| " + " | ".join(cells[:len(header)]) + " |\n")
    return md.getvalue()

def main():
    ap = argparse.ArgumentParser(description="Gera relatório simples a partir de um CSV.")
    ap.add_argument("csv_path", type=Path, help="Caminho do arquivo CSV")
    ap.add_argument("--out", type=Path, default=None, help="Saída em Markdown (.md)")
    args = ap.parse_args()

    report = make_report(args.csv_path)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"Relatório gerado em: {args.out}")
    else:
        print(report)

if __name__ == "__main__":
    main()
