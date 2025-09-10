#!/usr/bin/env python3
"""
organiza_arquivos.py — Organiza arquivos em pastas por extensão.

Uso:
  python organiza_arquivos.py /caminho/origem [--dest /caminho/destino] [--dry-run] [--copy]

- Move (padrão) ou copia (--copy) os arquivos da pasta ORIGEM para subpastas
  agrupadas pela extensão em DESTINO.
- Se DESTINO não for informado, usa a própria ORIGEM.
- Arquivos sem extensão vão para a pasta "sem_extensao".
- Em conflitos de nome, acrescenta um sufixo incremental _1, _2, ...

Exemplos:
  python organiza_arquivos.py ./meus_downloads
  python organiza_arquivos.py ./meus_downloads --dest ./organizado
  python organiza_arquivos.py ./meus_downloads --dry-run
  python organiza_arquivos.py ./meus_downloads --copy
"""
from __future__ import annotations
import argparse
import shutil
from pathlib import Path

def safe_move_or_copy(src: Path, dst: Path, copy: bool=False):
    dst.parent.mkdir(parents=True, exist_ok=True)
    final = dst
    if final.exists():
        stem, suffix = dst.stem, dst.suffix
        i = 1
        while final.exists():
            final = dst.with_name(f"{stem}_{i}{suffix}")
            i += 1
    if copy:
        shutil.copy2(src, final)
    else:
        shutil.move(str(src), str(final))
    return final

def main():
    ap = argparse.ArgumentParser(description="Organiza arquivos em pastas por extensão.")
    ap.add_argument("origem", type=Path, help="Pasta de origem (será percorrida recursivamente)")
    ap.add_argument("--dest", type=Path, default=None, help="Pasta de destino (default: a própria origem)")
    ap.add_argument("--dry-run", action="store_true", help="Apenas mostra o que faria, sem mover/copiar")
    ap.add_argument("--copy", action="store_true", help="Copiar ao invés de mover")
    args = ap.parse_args()

    origem: Path = args.origem
    destino: Path = args.dest if args.dest else origem

    if not origem.exists() or not origem.is_dir():
        raise SystemExit(f"Pasta de origem inválida: {origem}")

    count = 0
    for p in origem.rglob("*"):
        if not p.is_file():
            continue
        # Se destino estiver dentro da origem, não reprocessa pastas já criadas
        if destino in p.parents:
            pass
        ext = (p.suffix.lower().lstrip(".") or "sem_extensao")
        target_dir = destino / ext
        target_path = target_dir / p.name
        if args.dry_run:
            print(f"[DRY] {'COPIARIA' if args.copy else 'MOVERIA'}: {p}  ->  {target_path}")
        else:
            final = safe_move_or_copy(p, target_path, copy=args.copy)
            print(f"{'COPIADO' if args.copy else 'MOVIDO'}: {p}  ->  {final}")
        count += 1
    print(f"Concluído. Arquivos processados: {count}")

if __name__ == "__main__":
    main()
