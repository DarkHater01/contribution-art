#!/usr/bin/env python3
"""Dibuja una imagen en tu contribution graph de GitHub con commits retroactivos.

Uso:
    python3 draw.py foto.png
    python3 draw.py logo.png --end 2026-10-18 --repo ./mi-repo

Reglas del juego: el graph solo muestra ~52 semanas y solo pinta fechas pasadas.
Pon --end en una fecha ya transcurrida (o hoy) para ver el resultado completo.
"""
import argparse
import os
import subprocess
import sys
from datetime import date, timedelta

from PIL import Image

WEEKS = 53  # columnas del graph
DAYS = 7    # filas, domingo(arriba)..sabado(abajo)

# Luminancia -> nº de commits (4 niveles = los 4 verdes de GitHub)
LEVELS = [(200, 0), (150, 1), (100, 2), (50, 3), (0, 4)]


def grid_from_image(path):
    """Devuelve una matriz 7x53 de luminancias 0-255 desde cualquier imagen."""
    img = Image.open(path).convert("L").resize((WEEKS, DAYS), Image.LANCZOS)
    px = img.load()
    return [[px[x, y] for x in range(WEEKS)] for y in range(DAYS)]


def commits_for(lum):
    for threshold, n in LEVELS:
        if lum >= threshold:
            return n
    return 0


def date_for(start, week, day):
    return start + timedelta(weeks=week, days=day)


def dump_git_commits(repo, start, grid, dry_run=False):
    """Crea los commits vacios con fecha retroactiva. Returns nº total."""
    total = 0
    for day in range(DAYS):
        for week in range(WEEKS):
            n = commits_for(grid[day][week])
            if not n:
                continue
            d = date_for(start, week, day)
            for i in range(n):
                total += 1
                if dry_run:
                    continue
                stamp = f"{d.isoformat()}T12:{week:02d}:{i:02d}"
                env = {**os.environ, "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp}
                subprocess.run(
                    ["git", "commit", "--allow-empty", "-q", "-m", f"art {d}"],
                    cwd=repo, env=env, check=True,
                )
    return total


def main():
    p = argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--end", default=date.today().isoformat(),
                   help="fecha de la ultima columna (YYYY-MM-DD), por defecto hoy")
    p.add_argument("--repo", default=".", help="ruta del repo git destino")
    p.add_argument("--dry-run", action="store_true", help="solo contar, no commitear")
    a = p.parse_args()

    end = date.fromisoformat(a.end)
    last_sunday = end - timedelta(days=(end.weekday() + 1) % 7)
    start = last_sunday - timedelta(weeks=WEEKS - 1)

    grid = grid_from_image(a.image)
    total = dump_git_commits(a.repo, start, grid, a.dry_run)
    print(f"{total} commits entre {start} y {end} (repo: {a.repo})")
    if not a.dry_run:
        print("Ahora: git push  -> luego mira tu perfil en GitHub.")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        # calendario: la ultima columna empieza el domingo <= end
        end = date(2026, 10, 19)  # lunes
        last_sunday = end - timedelta(days=(end.weekday() + 1) % 7)
        assert last_sunday == date(2026, 10, 18), last_sunday
        start = last_sunday - timedelta(weeks=52)
        assert date_for(start, 52, 6) == end + timedelta(days=5)  # sabado de la ult. semana
        assert commits_for(255) == 0 and commits_for(10) == 4 and commits_for(160) == 1
        # imagen solida negra = todas las celdas encendidas
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            Image.new("L", (10, 10), 0).save(f.name)
        g = grid_from_image(f.name)
        assert len(g) == 7 and len(g[0]) == 53 and commits_for(g[0][0]) == 4
        os.unlink(f.name)
        print("selftest ok")
    else:
        main()
