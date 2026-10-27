#!/usr/bin/env python3
"""Empaqueta cada skill del plugin en dist/<skill>.zip para subirlas a claude.ai.

Uso (desde la raíz del repositorio):  python3 plugins/estudio-negocio/empaquetar.py
"""
import os
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.join(AQUI, "skills")
DIST = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "dist")

os.makedirs(DIST, exist_ok=True)
for nombre_skill in sorted(os.listdir(SKILLS)):
    origen = os.path.join(SKILLS, nombre_skill)
    if not os.path.isfile(os.path.join(origen, "SKILL.md")):
        continue
    destino = os.path.join(DIST, f"{nombre_skill}.zip")
    n = 0
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for base, dirs, archivos in os.walk(origen):
            dirs[:] = sorted(d for d in dirs if d != "__pycache__" and not d.startswith("."))
            for nombre in sorted(archivos):
                if nombre.endswith(".pyc") or nombre.startswith("."):
                    continue
                ruta = os.path.join(base, nombre)
                info = zipfile.ZipInfo(os.path.join(nombre_skill, os.path.relpath(ruta, origen)), date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o755 if nombre.endswith(".py") else 0o644) << 16
                with open(ruta, "rb") as f:
                    z.writestr(info, f.read())
                n += 1
    print(f"{destino}: {n} archivos")
