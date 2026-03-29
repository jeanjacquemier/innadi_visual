"""Example: generate a small batch of images with different seeds and sizes.

Run as:
    python3 examples/generate_batch.py

This script imports generate_batch from `draw_random_shapes.py` and creates a few images in the current directory.
"""
import os
from pathlib import Path

# make sure repo root is on sys.path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from draw_random_shapes import generate_batch


def main():
    out_dir = Path.cwd() / "example_outputs"
    out_dir.mkdir(exist_ok=True)

    # Example 1: 3 images using same size but different seeds
    # Example 1: 5 images using same size but different seeds, and create a GIF
    print("Generating example batch 1 (5 images, seed base 100) and a GIF")
    generate_batch(
        output=str(out_dir / "example1.png"),
        batch=100,
        start_index=1,
        seed=100,
        make_gif=True,
        gif_name=str(out_dir / "example1.gif"),
        gif_duration=500,
        width=1920,
        height=1200,
        count=400,
        background="#000000",
    )
  

if __name__ == "__main__":
    main()
