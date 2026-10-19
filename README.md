# Contribution Art

Dibuja una imagen (tu cara, un logo, tu texto) en tu **contribution graph** de GitHub usando commits retroactivos.

## Uso

```bash
# 1. crea un repo vacio en GitHub (solo para esto) y clona
# 2. desde dentro del repo:
python3 draw.py tu-imagen.png
git push
```

Por defecto dibuja sobre las ultimas 53 semanas terminando **hoy**. Para terminar en otra fecha:

```bash
python3 draw.py logo.png --end 2025-12-31
```

- `--dry-run` cuenta los commits sin crear nada.
- `python3 draw.py --selftest` comprueba la logica de calendario.

Cualquier imagen vale: se reescala a 53x7 con antialias y la luminosidad decide cuantos commits pone (claro = apagado, oscuro = encendido, con 4 niveles de verde).

## Requisitos

- Python 3 con Pillow.
- Repo git con **tu mismo email** en `git config user.email` (si no, GitHub no te cuenta los commits). Verificacion:

```bash
git config user.email   # debe ser uno associado a tu cuenta de GitHub
```

## Aviso

- Solo pinta **fechas pasadas**; commits con fecha futura no cuentan hasta que llegue ese dia.
- Un repo dedicado, no lo mezcles con tu trabajo real. Hacerlo en repos ajenos parece spam.
- Si tus contribuciones privadas estan ocultas, activa "Private contributions" en el perfil para que se note.
