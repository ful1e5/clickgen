import argparse
import os
import sys
import traceback
from contextlib import contextmanager
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Generator, List

import clickgen
from clickgen.configparser import parse_toml_file
from clickgen.packer.windows import pack_win
from clickgen.packer.x11 import pack_x11


def get_kwargs(args) -> Dict[str, Any]:
    kwargs = {}
    if args.name:
        kwargs["name"] = args.name
    if args.comment:
        kwargs["comment"] = args.comment
    if args.website:
        kwargs["website"] = args.website
    if args.platforms:
        kwargs["platforms"] = args.platforms

    if args.sizes:
        kwargs["win_size"] = args.sizes
        kwargs["x11_sizes"] = args.sizes

    if args.bitmaps_dir:
        kwargs["bitmaps_dir"] = Path(args.bitmaps_dir)
    if args.out_dir:
        kwargs["out_dir"] = Path(args.out_dir)

    return kwargs


@contextmanager
def cwd(path) -> Generator[None, None, None]:
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def main() -> None:  # noqa: C901
    parser = argparse.ArgumentParser(
        prog="ctgen",
        description="ctgen: Cursor Theme GENerator.",
    )

    parser.add_argument(
        "files",
        type=argparse.FileType("rb"),
        nargs="+",
        help="Config files (.toml) for generate cursor theme",
    )

    parser.add_argument(
        "-n",
        "--theme-name",
        dest="name",
        type=str,
        default=None,
        help="Force rename cursor theme name.",
    )

    parser.add_argument(
        "-c",
        "--theme-comment",
        dest="comment",
        type=str,
        default=None,
        help="Force rename comment of cursor theme.",
    )

    parser.add_argument(
        "-w",
        "--theme-website",
        dest="website",
        type=str,
        default=None,
        help="Force rename website url of cursor theme.",
    )

    parser.add_argument(
        "-d",
        "--bitmaps-dir",
        type=str,
        help="Force bitmaps directory location (which contains .png files).",
    )

    parser.add_argument(
        "-o",
        "--out-dir",
        type=str,
        help="Change output directory.",
    )

    parser.add_argument(
        "-s",
        "--sizes",
        dest="sizes",
        nargs="+",
        default=None,
        type=int,
        help=""" Change cursor size.
        Multiple sizes are assigned to XCursor
        while one size will be assigned to Windows.""",
    )

    parser.add_argument(
        "-p",
        "--platforms",
        choices=["windows", "x11"],
        default=None,
        help="Change Platform for output cursors.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {clickgen.__version__}",  # type: ignore
    )

    args = parser.parse_args()
    kwargs = get_kwargs(args)
    print_lock = Lock()

    files: List[Path] = []
    for f in args.files:
        files.append(Path(f.name))

    def process(file: Path) -> None:
        try:
            cfg = parse_toml_file(str(file.resolve()), **kwargs)
        except Exception:
            with print_lock:
                print(f"Error occurred while processing {file.name}:", file=sys.stderr)
                traceback.print_exc()
        else:
            theme = cfg.theme
            config = cfg.config
            cursors = cfg.cursors

            # Display Theme Info
            print(f"- Cursor Theme Name: {theme.name}")
            print(f"- Comment: {theme.comment}")
            print(f"- Platform Compliblity: {config.platforms}\n")

            # Generating XCursor
            if "x11" in config.platforms:
                print("Generating XCursors ...'")

                x11_out_dir = config.out_dir / theme.name / "cursors"
                x11_out_dir.mkdir(parents=True, exist_ok=True)

                for c in cursors:
                    print(f"- Bitmaping XCursor '{c.x11_cursor_name}'")
                    x_cursor = x11_out_dir / c.x11_cursor_name
                    x_cursor.write_bytes(c.x11_cursor)
                    # Creating symlinks
                    with cwd(x11_out_dir):
                        for link in c.x11_symlinks:
                            print(
                                f"   Linking XCursor '{link}' with '{c.x11_cursor_name}'"
                            )
                            os.symlink(x_cursor.name, link)

                print("Generating XCursors ... DONE\n")
                pack_x11(x11_out_dir.parent, theme.name, theme.comment)

            # Generating Windows cursors
            if "windows" in config.platforms:
                print("Generating Windows Cursors ...")

                win_out_dir = config.out_dir / f"{theme.name}-Windows"
                win_out_dir.mkdir(parents=True, exist_ok=True)

                for c in cursors:
                    if c.win_cursor and c.win_cursor_name:
                        print(
                            f"- Bitmaping Windows Cursor '{c.win_cursor_name}' from '{c.x11_cursor_name}'"
                        )
                        win_cursor = win_out_dir / c.win_cursor_name
                        win_cursor.write_bytes(c.win_cursor)

                print("Generating Windows Cursors ... DONE\n")
                try:
                    pack_win(win_out_dir, theme.name, theme.comment, theme.website)
                except Exception:
                    with print_lock:
                        print(
                            f"Error occurred while packaging windows theme '{theme.name}':",
                            file=sys.stderr,
                        )
                        traceback.print_exc()

    with ThreadPool(cpu_count()) as pool:
        pool.map(process, files)
