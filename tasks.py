from pathlib import Path

from invoke import run, task

try:
    from minchin.releaser import make_release
except ImportError:
    print("[WARN] minchin.releaser not installed.")


p = Path(__file__).parent  # directory holding this file




@task
def test(ctx, carefully=False, verbose=False, debug=False):
    """Generate the test Pelican site."""
    config = p / "test" / "pelicanconf.py"

    cli_args = ""
    if carefully:
        cli_args += " --fatal=warnings"
    if verbose:
        cli_args += " --verbose"
    if debug:
        cli_args += " --debug"

    run(f"pelican -s {config}{cli_args}")


@task
def serve_test(ctx, port="8000"):
    """Serve the generated test site."""
    # call using:
    # invoke serve_test --port 8001

    p4 = p / "test" / "output"
    print(p4)
    run(f"cd {p4} && start python -m http.server {port}")
