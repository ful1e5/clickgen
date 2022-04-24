import argparse
from pathlib import Path
from typing import Dict, List

import clickgen


def getpngs(p: Path) -> Dict[str, List[bytes]]:
    result: Dict[str, List[bytes]] = {}
    files: set[str] = set()
    for f in p.glob("*.png"):
        files.add(f.stem.split("-")[0])
    for f in files:
        result[f] = []
        for fp in p.glob(f"{f}*"):
            result[f].append(fp.read_bytes())
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ctgen",
        description="The hassle-free cursor theme generator",
    )

    parser.add_argument(
        "config_file",
        type=argparse.FileType("rb"),
        help="Config file for generate cursor theme",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {clickgen.__version__}",  # type: ignore
    )

    args = parser.parse_args()
    print(args)
