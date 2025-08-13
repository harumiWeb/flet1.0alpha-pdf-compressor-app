import argparse
from tomlkit.toml_file import TOMLFile

def bump_version(level: str):
    pyproject = TOMLFile("pyproject.toml")
    data = pyproject.read()
    version = data["project"]["version"]
    major, minor, patch = map(int, version.split("."))

    if level == "major":
        major += 1
        minor = 0
        patch = 0
    elif level == "minor":
        minor += 1
        patch = 0
    elif level == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump level: {level}")

    new_version = f"{major}.{minor}.{patch}"
    data["project"]["version"] = new_version
    pyproject.write(data)
    print(f"✅ Version bumped to {new_version}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bump project version in pyproject.toml")
    parser.add_argument(
        "level",
        choices=["major", "minor", "patch"],
        help="Which part of the version to bump"
    )
    args = parser.parse_args()
    bump_version(args.level)