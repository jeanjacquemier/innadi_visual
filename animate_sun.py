#!/usr/bin/env python3
"""
Simple utility to draw a symbolic sun: a filled circle with radial lines as rays.

Provides:
 - draw_sun(draw, center, radius, ray_count=8, ray_length=None, ray_width=3, fill=(255,215,0), outline=(255,140,0), ray_color=None)

Run as a script to create `sun_demo.png` for a quick preview.
"""
from PIL import Image, ImageDraw
import math
from typing import Tuple
import random


def draw_sun(
    draw: ImageDraw.ImageDraw,
    center: Tuple[int, int],
    radius: int,
    ray_count: int = 8,
    ray_length: int | None = None,
    ray_width: int = 1,
    fill: Tuple[int, int, int] = (255, 255, 255),
    outline: Tuple[int, int, int] = (0, 0, 0),
    ray_color: Tuple[int, int, int] | None = None,
):
    """Draw a simple symbolic sun on the provided ImageDraw object.

    - draw: PIL ImageDraw object
    - center: (x,y) center of the sun
    - radius: radius of the sun's central circle
    - ray_count: number of rays to draw
    - ray_length: additional length beyond the circle radius for rays; defaults to radius * 0.8
    - ray_width: stroke width for rays
    - fill: fill color for the central circle
    - outline: outline color for the central circle
    - ray_color: color for the rays (defaults to outline)
    """
    if ray_color is None:
        ray_color = outline

    cx, cy = center
    if ray_length is None:
        ray_length = int(radius * 0.5)

    # draw rays
    for i in range(ray_count):
        ray_length = ray_length * random.uniform(.5, 1.5)
        radius = radius * random.uniform(.8, 1.2)
        angle = (2 * math.pi * i) / ray_count
        # start a little inside the circle edge for nicer overlap
        sx = cx + math.cos(angle) * (radius * 1.2)
        sy = cy + math.sin(angle) * (radius * 1.2)
        ex = cx + math.cos(angle) * (radius + ray_length)
        ey = cy + math.sin(angle) * (radius + ray_length)
        draw.line([(sx, sy), (ex, ey)], fill=ray_color, width=ray_width)

    # draw central circle (filled with outline)
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
    draw.ellipse(bbox, fill=fill, outline=outline)


def _demo(index: int = 0):
    # create a simple demo image
    W, H = 400, 400
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # sun parameters
    center = (W // 2, H // 2)
    radius = 60
    draw_sun(draw, center, radius, ray_count=5, ray_width=1)

    out = f"sun_images/sun_demo_{index}.png"
    img.save(out)
    print(f"Wrote demo image: {out}")


if __name__ == "__main__":
    for i in range(5):
        _demo(i)