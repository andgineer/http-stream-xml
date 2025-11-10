import subprocess
import sys

from invoke import Collection, Context, task

ALLOWED_VERSION_TYPES = ["release", "bug", "feature"]


@task
def version(c: Context):
    """Show the current version."""
    with open("src/github-custom-actions/__about__.py") as f:
        version_line = f.readline()
        version_num = version_line.split('"')[1]
        print(version_num)
        return version_num


def ver_task_factory(version_type: str):
    @task
    def ver(c: Context):
        """Bump the version."""
        c.run(f"./scripts/verup.sh {version_type}")

    return ver


@task
def compile_requirements(c: Context):
    "Convert requirements.in to requirements.txt and requirements.dev.txt."
    start_time = subprocess.check_output(["date", "+%s"]).decode().strip()
    c.run("uv pip compile requirements.in --output-file=requirements.txt --upgrade")
    reqs_time = subprocess.check_output(["date", "+%s"]).decode().strip()
    c.run("uv pip compile requirements.dev.in --output-file=requirements.dev.txt --upgrade")

    # Remove pip from requirements.dev.txt to avoid triggering self-modification defence in Windows
    with open("requirements.dev.txt") as f:
        filtered_lines = [line for line in f if not line.startswith("pip==")]
    with open("requirements.dev.txt", "w") as f:
        f.writelines(filtered_lines)

    end_time = subprocess.check_output(["date", "+%s"]).decode().strip()
    print(f"Req's compilation time: {int(reqs_time) - int(start_time)} seconds")
    print(f"Req's dev compilation time: {int(end_time) - int(reqs_time)} seconds")
    print(f"Total execution time: {int(end_time) - int(start_time)} seconds")

    c.run("scripts/include_pyproject_requirements.py requirements.in")

@task(pre=[compile_requirements])
def reqs(c: Context):
    """Upgrade requirements including pre-commit."""
    c.run("pip install -r requirements.dev.txt")


@task
def docs(c):
    """Build the documentation"""
    c.run("sphinx-build docs docs_build")


@task
def docs_check(c):
    """Check the documentation"""
    c.run("sphinx-build docs -W -b linkcheck -d docs_build/doctrees docs_build/html")


@task
def test(c):
    """Run the test suite"""
    c.run("./scripts/test.sh -m 'not slow'")


@task
def test_full(c):
    """Run the full test suite"""
    c.run("./scripts/test.sh")


@task
def uv(c: Context):
    """Install or upgrade uv."""
    c.run("curl -LsSf https://astral.sh/uv/install.sh | sh")


@task
def pre(c):
    """Run pre-commit checks"""
    c.run("pre-commit run --verbose --all-files")


namespace = Collection.from_module(sys.modules[__name__])
for name in ALLOWED_VERSION_TYPES:
    namespace.add_task(ver_task_factory(name), name=f"ver-{name}")
