# draw_random_shapes.py

A small utility that creates an image with random lines, circles and squares using Pillow.

Usage

Generate a default image (800x600, 100 shapes):

```bash
python3 draw_random_shapes.py
```

Specify output, size, count and seed:

```bash
python3 draw_random_shapes.py --output out.png --width 1024 --height 768 --count 200 --seed 42
```

Change background color (hex or simple name):

```bash
python3 draw_random_shapes.py --output bg.png --background "#ffeecc" --count 120
python3 draw_random_shapes.py --output blue_bg.png --background blue --count 80
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Notes

- If Pillow is missing the script will print install instructions and exit.
- Use `--seed` to create reproducible outputs.
- The script is intentionally small and dependency-free beyond Pillow and Python standard library.
