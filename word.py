#!/usr/bin/env python3
"""Genera la imagen 53x7 con la palabra pintada en las columnas que le pidas.

La rejilla del contribution graph es 53 columnas x 7 filas. Cada columna = 1
semana (domingo arriba). Con --end 2026-10-18 la columna 10 empieza el domingo
28-dic-2025 (semana que contiene el 1-ene), y la 40 el domingo 26-jul-2026.
"""
import argparse

from PIL import Image

GLYPHS = {
    "K": ["#..#", "#.#.", "##..", "#.#.", "#..#"],
    "4": ["..##", ".#.#", "#..#", "####", "...#"],
    "L": ["#.", "#.", "#.", "#.", "##"],
    "1": [".#.", "##.", ".#.", ".#.", "###"],
    "N": ["#..#", "##.#", "#.##", "#..#", "#..#"],
    "U": ["#..#", "#..#", "#..#", "#..#", ".##."],
    "X": ["#.#", "#.#", ".#.", "#.#", "#.#"],
}
WEEKS, DAYS, GAP = 53, 7, 1


def compose(word):
    """Devuelve (filas, ancho) con las letras separadas por GAP columnas."""
    rows = [["."] * WEEKS for _ in range(DAYS)]
    col = 0
    for ch in word:
        g = GLYPHS[ch]
        for y, line in enumerate(g):
            for x, c in enumerate(line):
                if c == "#":
                    rows[y][x + col] = "#"
        col += len(g[0]) + GAP
    return rows, col - GAP


def render(word, start_col, out):
    rows, width = compose(word)
    if start_col + width > WEEKS:
        raise SystemExit(f"no cabe: ancho {width} + col {start_col} > {WEEKS}")
    img = Image.new("L", (WEEKS, DAYS), 255)
    for y in range(DAYS):
        for x in range(width):
            if rows[y][x] == "#":
                img.putpixel((x + start_col, y + 1), 0)  # filas 1..5 (lun-vie)
    img.save(out)
    return rows, width


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("word")
    p.add_argument("--start-col", type=int, default=11)
    p.add_argument("--out", default="word.png")
    a = p.parse_args()
    rows, width = render(a.word, a.start_col, a.out)
    # Preview ASCII (con el desplazamiento real de columnas)
    for y in range(DAYS):
        line = "".join("#" if x >= a.start_col and rows[y][x - a.start_col] == "#"
                       else "." for x in range(WEEKS))
        print(line)
    print(f"{a.word}: ancho {width}, columnas {a.start_col}..{a.start_col + width - 1} -> {a.out}")
