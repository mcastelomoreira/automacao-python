#!/usr/bin/env python3
"""
calcula_basico.py — Cálculos simples de notas e vendas.

Uso:
  python calcula_basico.py notas 7.5 8 6.2 9
  python calcula_basico.py vendas 120.90 45 32.5 88 10

Subcomandos:
  notas  → recebe uma lista de notas e calcula média, mediana, min, max.
  vendas → recebe valores de vendas (R$) e calcula total, ticket médio e quantidade.

Opções:
  --aprovacao <media>  → (apenas para 'notas') define média mínima para aprovação (default: 7.0)
"""
from __future__ import annotations
import argparse
import statistics as stats

def cmd_notas(valores, aprovacao):
    nums = [float(x) for x in valores]
    media = sum(nums)/len(nums)
    mediana = stats.median(nums)
    print("📚 Notas")
    print(f"- Quantidade: {len(nums)}")
    print(f"- Média: {media:.2f}")
    print(f"- Mediana: {mediana:.2f}")
    print(f"- Mínima: {min(nums):.2f}")
    print(f"- Máxima: {max(nums):.2f}")
    print(f"- Situação: {'APROVADO' if media >= aprovacao else 'REPROVADO'} (corte: {aprovacao:.2f})")

def cmd_vendas(valores):
    nums = [float(x) for x in valores]
    total = sum(nums)
    qtd = len(nums)
    ticket = total / qtd if qtd else 0.0
    print("🛒 Vendas")
    print(f"- Quantidade de vendas: {qtd}")
    print(f"- Faturamento total: R$ {total:,.2f}")
    print(f"- Ticket médio: R$ {ticket:,.2f}")

def main():
    ap = argparse.ArgumentParser(description="Cálculos simples de notas e vendas.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_notas = sub.add_parser("notas", help="Calcula estatísticas de uma lista de notas")
    ap_notas.add_argument("valores", nargs="+", help="Valores de notas (ex.: 7.5 8 6.2 9)")
    ap_notas.add_argument("--aprovacao", type=float, default=7.0, help="Mínimo para aprovação (default: 7.0)")

    ap_vendas = sub.add_parser("vendas", help="Calcula total e ticket médio de vendas (R$)")
    ap_vendas.add_argument("valores", nargs="+", help="Valores de vendas em reais (ex.: 120.9 45 32.5)")

    args = ap.parse_args()

    if args.cmd == "notas":
        cmd_notas(args.valores, args.aprovacao)
    elif args.cmd == "vendas":
        cmd_vendas(args.valores)

if __name__ == "__main__":
    main()
