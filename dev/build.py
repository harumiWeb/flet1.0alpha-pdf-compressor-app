# build.py
import tomllib
import subprocess

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)

version = data["project"]["version"]

cmd = [
    "uv", "run", "flet", "pack", "-D",
    "--add-data", "assets:assets",
    "--name", "GhostFlet PDF",
    "--file-version", version,
    "--icon", "assets/icon.png",
    "main.py", "-y"
]

subprocess.run(cmd)