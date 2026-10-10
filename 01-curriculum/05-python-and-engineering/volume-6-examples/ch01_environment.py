"""Chapter 1: check that this machine can run the book's examples."""
import sys
from importlib.metadata import version

NEEDED = ["pydantic", "sqlalchemy", "hypothesis", "polars", "pytest"]


def main() -> int:
    print(f"python      {sys.version_info.major}.{sys.version_info.minor}"
          f".{sys.version_info.micro}")
    for name in NEEDED:
        print(f"{name:<11} {version(name)}")
    in_venv = sys.prefix != sys.base_prefix
    print(f"virtual environment: {'yes' if in_venv else 'NO'}")
    if sys.version_info < (3, 13):
        print("These examples need Python 3.13 or later.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
