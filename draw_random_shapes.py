#!/usr/bin/env python3

from pathlib import Path

def hex_to_rgb(hexstr: str):
    s = hexstr.strip()
    if s.startswith("#"):
        s = s[1:]
    if len(s) == 3:
        s = ''.join([c*2 for c in s])
    if len(s) != 6:
        raise ValueError("Invalid hex color: %r" % hexstr)
    return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))


def center_and_pad(input_path: Path, canvas_w: int, canvas_h: int, fill="#000000", fit: str = "skip"):
    img = Image.open(input_path)
    img = img.convert("RGBA")

    # parse fill color
    try:
        if isinstance(fill, tuple):
            bg = fill
        elif isinstance(fill, str) and fill.startswith("#"):
            bg = hex_to_rgb(fill)
        else:
            # try to let PIL parse named colors
            tmp = Image.new("RGB", (1,1), fill)
            bg = tmp.getpixel((0,0))
    except Exception:
        bg = (0,0,0)
    
    canvas = Image.new("RGBA", (canvas_w, canvas_h), bg + (255,))

    iw, ih = img.size

    # handle oversized input
    if iw > canvas_w or ih > canvas_h:
        if fit == "skip":
            # we won't change the image; paste will be clipped automatically
            pass
        elif fit == "scale":
            # scale to fit inside canvas preserving aspect ratio
            scale = min(canvas_w / iw, canvas_h / ih)
            new_size = (max(1, int(iw * scale)), max(1, int(ih * scale)))
            img = img.resize(new_size, Image.LANCZOS)
            iw, ih = img.size
        elif fit == "crop":
            # center-crop the input to the canvas size
            left = max(0, (iw - canvas_w) // 2)
            top = max(0, (ih - canvas_h) // 2)
            right = left + min(canvas_w, iw)
            bottom = top + min(canvas_h, ih)
            img = img.crop((left, top, right, bottom))
            iw, ih = img.size

    # compute top-left to paste so the image is centered
    paste_x = (canvas_w - iw) // 2
    paste_y = (canvas_h - ih) // 2

    # paste using alpha composite to preserve transparency if present
    canvas.paste(img, (paste_x, paste_y), img)

    # convert to RGB before saving to common formats
    out = canvas.convert("RGB")
    return out


"""
Create an image with random lines, circles and rectangles using Pillow.

Usage examples:
  python3 draw_random_shapes.py --output random.png --width 1920 --height 1200 --count 80
  python3 draw_random_shapes.py --output out.png --count 200 --seed 42

If Pillow is not installed the script prints install instructions.
"""
import sys
import random
import argparse
import os, glob
from typing import Tuple

try:
    from PIL import Image, ImageDraw
except Exception as e:
    print("Pillow is not installed. Install it with: pip install pillow")
    sys.exit(1)


def random_color(alpha: bool = False) -> Tuple[int, int, int]:
    # return one of: yellow, red, or green
    choices = [
        (237, 239, 96),  # yellow
        (178, 64, 47),    # red
        (0, 78, 24),    # green
    ]
    return random.choice(choices)

def clamp(v, a, b):
    return max(a, min(b, v))


def generate_image(
    width: int = 1920,
    height: int = 1200,
    count: int = 100,
    background=(0, 0, 0),
    seed: int = None,
    output: str = "random_shapes.png",
    max_attempts: int = 200,
    spacing: int = 0,
    overlap_mode: str = "none",
):
    """Generate and save an image with random shapes.

    - width, height: canvas size
    - count: total number of shapes to draw
    - background: background color tuple
    - seed: random seed (optional)
    - output: output filename
    """
    if seed is not None:
        random.seed(seed)

    img = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(img)

    max_r = min(width, height) // 30

    # track occupied bounding boxes to avoid overlaps: list of (bbox, filled)
    occupied = []

    def expanded(bbox, pad):
        l, t, r, b = bbox
        return (l - pad, t - pad, r + pad, b + pad)

    def intersects(a, b, pad=0):
        al, at, ar, ab = expanded(a, pad)
        bl, bt, br, bb = expanded(b, pad)
        return not (ar <= bl or al >= br or ab <= bt or at >= bb)
    color = random_color()
    for i in range(count):
        shape = random.choice(["line", "circle", "rectangle"])
        
        stroke = random.randint(1, 1)
        placed = False
        for attempt in range(max_attempts):
            if shape == "line":
                # force vertical line: choose x and two y's
                x = random.randint(0, width - 1)
                y1 = random.randint(0, height - 1)
                y2 = random.randint(0, height - 1)
                if y1 > y2:
                    y1, y2 = y2, y1
                half = max(1, stroke // 2)
                left = x - half
                top = y1
                right = x + half
                bottom = y2
                # ensure bbox in canvas
                left = clamp(left, 0, width - 1)
                right = clamp(right, 0, width - 1)
                top = clamp(top, 0, height - 1)
                bottom = clamp(bottom, 0, height - 1)
                if left >= right or top >= bottom:
                    continue
                bbox = (left, top, right, bottom)

            elif shape == "circle":
                # force true circle by picking center with margin r
                r = random.randint(5, max(5, max_r))
                if r * 2 > width or r * 2 > height:
                    # can't fit a circle of this size
                    continue
                cx = random.randint(r, width - 1 - r)
                cy = random.randint(r, height - 1 - r)
                left = cx - r
                top = cy - r
                right = cx + r
                bottom = cy + r
                bbox = (left, top, right, bottom)

            elif shape == "rectangle":
                # choose random rectangle width and height
                w_rect = random.randint(6, max(6, max_r))
                h_rect = random.randint(6, max(6, max_r))
                if w_rect > width or h_rect > height:
                    continue
                x = random.randint(0, width - w_rect)
                y = random.randint(0, height - h_rect)
                left = x
                top = y
                right = x + w_rect
                bottom = y + h_rect
                bbox = (left, top, right, bottom)

            # decide current filled status for this candidate shape (once)
            if shape == "line":
                cur_filled = False
            elif shape == "circle":
                cur_filled = 1#random.random() < 0.4
            else:  # square
                cur_filled = 1#random.random() < 0.35

            # check overlap according to overlap_mode and spacing
            overlapped = False
            for occ in occupied:
                occ_bbox, occ_filled = occ

                if overlap_mode == "all":
                    # everything allowed
                    allowed = True
                elif overlap_mode == "outline":
                    # allow overlap unless both are filled
                    allowed = not (occ_filled and cur_filled)
                else:  # 'none'
                    allowed = False

                if allowed:
                    continue

                if intersects(bbox, occ_bbox, pad=spacing):
                    overlapped = True
                    break

            if overlapped:
                continue

            # draw using the decided cur_filled flag
            if shape == "circle":
                if cur_filled:
                    draw.ellipse([left, top, right, bottom], fill=color)
                else:
                    draw.ellipse([left, top, right, bottom], outline=color, width=stroke)

            elif shape == "rectangle":
                if cur_filled:
                    draw.rectangle([left, top, right, bottom], fill=color)
                else:
                    draw.rectangle([left, top, right, bottom], outline=color, width=stroke)

            elif shape == "line":
                draw.line([(x, top), (x, bottom)], fill=color, width=stroke)

            occupied.append((bbox, cur_filled))
            placed = True
            break

        if not placed:
            # couldn't place this shape without overlap after many attempts; skip it
            continue

    img.save(output)
    print(f"Saved image to: {output}")


def generate_batch(
    output: str,
    batch: int = 1,
    start_index: int = 1,
    seed: int = None,
    make_gif: bool = False,
    gif_name: str | None = None,
    gif_duration: int = 200,
    gif_loop: int = 0,
    **kwargs,
):
    """Generate a batch of images.

    - output: base output filename (will have index inserted if batch>1)
    - batch: number of images to create
    - start_index: starting index for numbering
    - seed: base seed; each image will use seed + idx if provided
    - kwargs: forwarded to generate_image
    """
    width: int = 1920
    height: int = 1200
    base, ext = os.path.splitext(output)
    if batch <= 1:
        # single image
        generate_image(output=output, seed=seed, **kwargs)
        return [output]

    out_paths = []
    for i in range(batch):
        idx = start_index + i
        # format index with three digits
        out_name = f"{base}_{idx:03d}{ext}"
        use_seed = seed + i if seed is not None else None
        generate_image(output=out_name, seed=use_seed, **kwargs)
        out_paths.append(out_name)

    # optionally build a GIF from the generated images
    gif_path = None
    if make_gif and len(out_paths) > 0:
        images_to_instert = glob.glob("./images/*")
        #frames = [Image.open(p).convert("RGBA") for p in out_paths]
        frames=[]
        for i, p in enumerate(out_paths):
            #print(val)
            frames.append(Image.open(p).convert("RGBA"))
            if i % 10 == 0:
                q  = images_to_instert[(i // 3) % len(images_to_instert)]
                #img = Image.open(q).convert("RGBA")
                img = center_and_pad(q, width, height)
                for i in range(10):
                    frames.append(img)


        gif_path = gif_name if gif_name is not None else f"{base}.gif"
        # PIL will handle conversion to palette for GIF
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=gif_duration,
            loop=gif_loop,
            disposal=2,
        )
        print(f"Saved GIF to: {gif_path}")

        for f in glob.glob(f"{base}*.png"):
            os.remove(f)

    return out_paths if not make_gif else (out_paths, gif_path)


def parse_args():
    p = argparse.ArgumentParser(description="Generate an image with random lines, circles and squares using Pillow")
    p.add_argument("--width", type=int, default=1920, help="Image width")
    p.add_argument("--height", type=int, default=1200, help="Image height")
    p.add_argument("--count", type=int, default=100, help="Total number of shapes to draw")
    p.add_argument("--background", type=str, default="#000000", help="Background color (hex like #rrggbb or common name)")
    p.add_argument("--seed", type=int, default=None, help="Optional random seed for reproducible output")
    p.add_argument("--output", type=str, default="random_shapes.png", help="Output filename")
    p.add_argument("--batch", type=int, default=0, help="If >0, generate this many images (batch mode).")
    p.add_argument("--batch-start", type=int, default=1, help="Start index for batch filenames (default 1)")
    p.add_argument("--max-attempts", type=int, default=200, help="Max placement attempts per shape when avoiding overlaps")
    p.add_argument("--spacing", type=int, default=0, help="Spacing (pixels) between shapes when checking overlaps")
    p.add_argument("--overlap-mode", choices=["none", "outline", "all"], default="none", help="Overlap policy: none=forbid overlaps, outline=allow if either shape is outline, all=allow any overlap")
    return p.parse_args()


def hex_to_rgb(hexstr: str):
    hexstr = hexstr.strip()
    if hexstr.startswith("#"):
        hexstr = hexstpathr[1:]
    if len(hexstr) == 3:
        hexstr = ''.join([c*2 for c in hexstr])
    if len(hexstr) != 6:
        raise ValueError("Invalid hex color")
    r = int(hexstr[0:2], 16)
    g = int(hexstr[2:4], 16)
    b = int(hexstr[4:6], 16)
    return (r, g, b)


if __name__ == "__main__":
    args = parse_args()
    bg = args.background
    try:
        if bg.startswith("#"):
            bg_rgb = hex_to_rgb(bg)
        else:
            # allow simple color names by letting Pillow translate (create a 1x1 image)
            tmp = Image.new("RGB", (1, 1), bg)
            bg_rgb = (0, 0, 0 )#tmp.getpixel((0, 0))
    except Exception:
        print("Invalid background color; falling back to white")
        bg_rgb = (0, 0, 0)
        

    # if batch requested, generate multiple images
    if getattr(args, "batch", 0) and args.batch > 0:
        paths = generate_batch(
            output=args.output,
            batch=args.batch,
            start_index=getattr(args, "batch_start", args.batch if hasattr(args, "batch") else 1),
            seed=args.seed,
            width=args.width,
            height=args.height,
            count=args.count,
            background=bg_rgb,
            max_attempts=args.max_attempts,
            spacing=args.spacing,
            overlap_mode=args.overlap_mode,
        )
        print(f"Generated {len(paths)} images.")
    else:
        generate_image(
            width=args.width,
            height=args.height,
            count=args.count,
            background=bg_rgb,
            seed=args.seed,
            output=args.output,
            max_attempts=args.max_attempts,
            spacing=args.spacing,
            overlap_mode=args.overlap_mode,
        )
