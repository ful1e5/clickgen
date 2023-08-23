#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
from glob import glob
from pathlib import Path
from threading import Lock
from typing import List

from clickgen.parser import open_blob
from clickgen.writer import to_win, to_x11

if __name__ == "__main__":
    print_lock = Lock()

    # mkdir 'out'
    out = Path("out")
    out.mkdir(parents=True, exist_ok=True)

    fnames = glob("pngs/wait-*.png")
    pngs: List[bytes] = []
    for f in sorted(fnames):
        with open(f, "rb") as p:
            pngs.append(p.read())

    try:
        ani = open_blob(pngs, hotspot=(100, 100))

        # save Windows animated cursor
        aext, aresult = to_win(ani.frames)
        with open(out / f"test-ani{aext}", "wb") as o:
            o.write(aresult)

        # save X11 animated cursor
        axresult = to_x11(ani.frames)
        with open(out / "xtest-ani", "wb") as o:
            o.write(axresult)

        with open("pngs/pointer.png", "rb") as p:
            cur = open_blob([p.read()], hotspot=(50, 50))

            # save Windows static cursor
            ext, result = to_win(cur.frames)
            with open(out / f"test{ext}", "wb") as o:
                o.write(result)

            # save X11 static cursor
            xresult = to_x11(cur.frames)
            with open(out / "xtest", "wb") as o:
                o.write(xresult)
    except Exception:
        with print_lock:
            print("Error occurred while processing ", file=sys.stderr)
            traceback.print_exc()

    print("Building ... DONE")
