# 🤖 Automação em Python (scripts simples e úteis)

Três scripts prontos para praticar **lógica**, **bibliotecas nativas** e deixar seu GitHub mais forte:

## 1) `organiza_arquivos.py`
Organiza arquivos em subpastas por **extensão** (ex.: `pdf/`, `jpg/`, `xlsx/`).
- Move (padrão) ou copia (`--copy`).
- Suporta recursivo, **dry-run** e resolve conflitos de nome.

**Exemplos**
```bash
python organiza_arquivos.py ./meus_downloads
python organiza_arquivos.py ./meus_downloads --dest ./organizado
python organiza_arquivos.py ./meus_downloads --dry-run
python organiza_arquivos.py ./meus_downloads --copy
