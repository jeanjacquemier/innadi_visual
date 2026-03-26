import subprocess
import sys
from pathlib import Path


def test_draw_random_shapes_creates_file(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "draw_random_shapes.py"
    assert script.exists(), f"Script not found at {script}"

    out = tmp_path / "out.png"
    cmd = [sys.executable, str(script), "--output", str(out), "--count", "10", "--width", "200", "--height", "150"]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("STDOUT:\n", proc.stdout)
        print("STDERR:\n", proc.stderr)
    assert proc.returncode == 0, f"Script failed: {proc.stderr}"
    assert out.exists(), "Output file not created"
    assert out.stat().st_size > 0, "Output file is empty"
