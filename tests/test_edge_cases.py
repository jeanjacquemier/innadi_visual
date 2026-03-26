import subprocess
import sys
from pathlib import Path


def run_script(args):
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "draw_random_shapes.py"
    cmd = [sys.executable, str(script)] + args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc


def test_invalid_background_falls_back(tmp_path):
    out = tmp_path / "bg.png"
    proc = run_script(["--output", str(out), "--background", "notacolor", "--count", "5"]) 
    # Script should succeed and still create an image (falls back to white)
    assert proc.returncode == 0, f"Script failed: {proc.stderr}"
    assert out.exists(), "Output file not created for invalid background"
    assert out.stat().st_size > 0, "Output file is empty"


def test_zero_count_creates_background_image(tmp_path):
    out = tmp_path / "zero.png"
    proc = run_script(["--output", str(out), "--count", "0", "--width", "200", "--height", "150"]) 
    assert proc.returncode == 0, f"Script failed: {proc.stderr}"
    assert out.exists(), "Output file not created for zero count"
    assert out.stat().st_size > 0, "Output file is empty"


def test_invalid_dimensions_fail(tmp_path):
    out = tmp_path / "bad.png"
    # width 0 should cause Pillow to raise an error and script to exit non-zero
    proc = run_script(["--output", str(out), "--count", "5", "--width", "0", "--height", "100"]) 
    assert proc.returncode != 0, "Script unexpectedly succeeded with invalid width"
