#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="clickgen",
        description="The hassle-free cursor building toolbox",
    )

    # Positional Args.
    parser.add_argument(
        "png",
        metavar="PNG",
        type=str,
        nargs="+",
        help="Path to .png file. If animated, Try to mask frame-number using asterisk( * ). For Example 'wait-*.png'",
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        dest="out_dir",
        metavar="OUT",
        type=str,
        default="./",
        help="To change output directory. (default: %(default)s)",
    )

    # Optional Args.
    parser.add_argument(
        "-hot",
        "--hotspot",
        dest="hotspot",
        metavar="cord",
        nargs=2,
        default=(0, 0),
        type=int,
        help="To set 'x' & 'y' coordinates of cursor's hotspot. (default: %(default)s)",
    )
    parser.add_argument(
        "-t",
        "--type",
        dest="type",
        choices=("windows", "xcursor", "all"),
        default="all",
        help="Set cursor type, Which you want to build. (default: '%(default)s')",
    )

    parser.add_argument(
        "-s",
        "--sizes",
        dest="sizes",
        metavar="size",
        nargs="+",
        default=[22],
        type=int,
        help="Set pixel-size for cursor. (default: %(default)s)",
    )

    parser.add_argument(
        "-d",
        "--delay",
        dest="delay",
        metavar="ms",
        default=50,
        type=int,
        help="Set animated cursor's frames delay in 'micro-second'. (default: %(default)s)",
    )

    args = parser.parse_args()
    print(args)
    # hotspot = (args.hotspot[0], args.hotspot[1])
    # sizes = [(s, s) for s in args.sizes]
    # out_dir = Path(args.out_dir)
    # if not out_dir.exists():
    #     out_dir.mkdir(parents=True, exist_ok=True)
