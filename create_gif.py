#!/usr/bin/env python3
"""
Create an animated GIF from all image files in a directory.

Provides a function `generate_gif_from_dir(dir_path, output_path, pattern='*.png', duration=200, loop=0, sort=True)`
and a CLI wrapper.

Behavior:
- Collects files matching `pattern` (glob) inside `dir_path`.
- Sorts them (alphabetically) by default so frames are in predictable order.
- Loads images with Pillow, converts them to RGBA.
- Composes each frame onto a canvas sized to the maximum width/height among images so frames align.
- Saves an animated GIF to `output_path`.

Example:
  python3 create_gif.py --dir ./images --pattern "*.png" --output anim.gif --duration 250

"""
from pathlib import Path
from typing import Iterable, List, Optional
from PIL import Image
import argparse


def generate_gif_from_dir(
    dir_path: str | Path,
    output_path: str | Path,
    pattern: str = "*.png",
    duration: int = 200,
    loop: int = 0,
    sort: bool = True,
    verbose: bool = False,
) -> Path:
    """Generate an animated GIF from images in `dir_path` matching `pattern`.

    Returns the Path to the generated GIF.
    """
    dirp = Path(dir_path)
    if not dirp.exists() or not dirp.is_dir():
        raise ValueError(f"Directory not found: {dir_path}")

    files = list(dirp.glob(pattern))
    if sort:
        files.sort()

    if verbose:
        print(f"Found {len(files)} files matching {pattern} in {dirp}")

    if not files:
        raise ValueError("No files found to include in GIF")

    # Load images and compute max dimensions
    imgs: List[Image.Image] = []
    max_w = max_h = 0
    for p in files:
        try:
            im = Image.open(p).convert("RGBA")
        except Exception as e:
            if verbose:
                print(f"Skipping {p}: {e}")
            continue
        imgs.append(im)
        w, h = im.size
        if w > max_w:
            max_w = w
        if h > max_h:
            max_h = h

    if not imgs:
        raise ValueError("No valid images loaded to include in GIF")

    # Compose frames on a consistent canvas size (max_w x max_h)
    frames: List[Image.Image] = []
    for im in imgs:
        canvas = Image.new("RGBA", (max_w, max_h), (0, 0, 0, 0))
        x = (max_w - im.width) // 2
        y = (max_h - im.height) // 2
        canvas.paste(im, (x, y), im)
        frames.append(canvas.convert("P", palette=Image.ADAPTIVE))

    out_path = Path(output_path)
    # Save the first frame with the append_images parameter
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=loop,
        optimize=False,
        disposal=2,
    )

    if verbose:
        print(f"Saved GIF to: {out_path} ({len(frames)} frames)")
    return out_path


def main():
    p = argparse.ArgumentParser(description="Create an animated GIF from images in a directory")
    p.add_argument("--dir", required=True, help="Directory containing input images")
    p.add_argument("--pattern", default="*.png", help="Glob pattern to match images (default: *.png)")
    p.add_argument("--output", required=True, help="Output GIF path")
    p.add_argument("--duration", type=int, default=500, help="Frame duration in ms (default 200)")
    p.add_argument("--loop", type=int, default=0, help="Loop count for GIF (0 = infinite)")
    p.add_argument("--no-sort", action="store_true", help="Do not sort files alphabetically")
    p.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = p.parse_args()

    generate_gif_from_dir(
        args.dir,
        args.output,
        pattern=args.pattern,
        duration=args.duration,
        loop=args.loop,
        sort=not args.no_sort,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
