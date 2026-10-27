#!/usr/bin/env python3
"""Empaqueta la skill validar-negocio en dist/validar-negocio.zip para subirla a claude.ai.

Uso (desde la raíz del repositorio):  python3 plugins/estudio-negocio/empaquetar.py
"""
import os
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(AQUI, "skills", "validar-negocio")
DESTINO = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "dist", "validar-negocio.zip")

os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
n = 0
with zipfile.ZipFile(DESTINO, "w", zipfile.ZIP_DEFLATED) as z:
    for base, dirs, archivos in os.walk(SKILL):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__" and not d.startswith("."))
        for nombre in sorted(archivos):
            if nombre.endswith(".pyc") or nombre.startswith("."):
                continue
            ruta = os.path.join(base, nombre)
            arc = os.path.join("validar-negocio", os.path.relpath(ruta, SKILL))
            info = zipfile.ZipInfo(arc, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if nombre.endswith(".py") else 0o644) << 16
            with open(ruta, "rb") as f:
                z.writestr(info, f.read())
            n += 1
print(f"{DESTINO}: {n} archivos")
