import subprocess
import sys

def test_app_startup():
    """Smoke test: Ensure the application entrypoint can be imported/run without crashing."""
    # We run 'app.main' with '--help' just to see if it boots up.
    cmd = [sys.executable, "-m", "app.main", "--help"]
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
    
    assert result.returncode == 0, "Application failed to start (ImportError or SyntaxError)"
    assert "Usage" in result.stdout or "Sensei" in result.stdout

if __name__ == "__main__":
    test_app_startup()
