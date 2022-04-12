#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import traceback
from pathlib import Path
from threading import Lock
from typing import BinaryIO, List

import clickgen
from clickgen.parser import open_blob
from clickgen.parser.png import DELAY, SIZES
from clickgen.writer.windows import to_win
from clickgen.writer.x11 import to_x11


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="clickgen",
        description="The hassle-free cursor building toolbox",
    )

    parser.add_argument(
        "files",
        type=argparse.FileType("rb"),
        nargs="+",
        help="Cursor bitmap files to generate (*.png)",
    )
    parser.add_argument(
        "-o",
        "--output",
        "--output-dir",
        default=os.curdir,
        help="Directory to store generated cursor file.",
    )
    parser.add_argument(
        "-p",
        "--platform",
        choices=["windows", "x11", "all"],
        default="all",
        help="Platform for generated cursor file.",
    )
    parser.add_argument(
        "-x",
        "--hotspot-x",
        type=int,
        default=0,
        help="x-offset of cursor (as fraction of width)",
    )
    parser.add_argument(
        "-y",
        "--hotspot-y",
        type=int,
        default=0,
        help="y-offset of cursor (as fraction of height)",
    )
    parser.add_argument(
        "-s",
        "--sizes",
        dest="sizes",
        nargs="+",
        default=SIZES,
        type=int,
        help="Set pixel-size for cursor.",
    )
    parser.add_argument(
        "-d",
        "--delay",
        default=DELAY,
        type=int,
        help="Set delay between frames of cursor.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {clickgen.__version__}",  # type: ignore
    )

    args = parser.parse_args()
    print_lock = Lock()
    files: List[BinaryIO] = args.files

    hotspot = (args.hotspot_x, args.hotspot_y)
    name = Path(files[0].name.split("-")[0])
    output = Path(args.output, name.stem)
    blobs: List[bytes] = [f.read() for f in files]

    try:
        cursor = open_blob(blobs, hotspot, args.sizes, args.delay)
    except Exception:
        with print_lock:
            print(f"Error occurred while processing {name.name}:", file=sys.stderr)
            traceback.print_exc()
    else:

        def gen_xcursor() -> None:
            result = to_x11(cursor.frames)
            output.write_bytes(result)

        def gen_wincursor() -> None:
            ext, result = to_win(cursor.frames)
            win_output = output.with_suffix(ext)
            win_output.write_bytes(result)

        if args.platform == "x11":
            gen_xcursor()
        elif args.platform == "windows":
            gen_wincursor()
        else:
            gen_xcursor()
            gen_wincursor()
