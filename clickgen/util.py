#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import os
import shutil
import sys
import time
from contextlib import contextmanager
from difflib import SequenceMatcher as SM
from pathlib import Path
from typing import List, Optional, Union


def remove(p: Union[str, Path]) -> None:
    """ Utility for removing file, directory or symlink, If it's existed in filesystem. """

    if isinstance(p, str):
        p: Path = Path(p)

    if p.exists():
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
    else:
        pass


@contextmanager
def goto_cursors_dir(dir: Path):
    """ Temporary change directory to `cursors` using contextmanager. """

    CWD = os.getcwd()
    os.chdir(dir.absolute())
    try:
        yield
    except:
        raise Exception(f" Exception caught: {sys.exc_info()[0]}")
    finally:
        os.chdir(CWD)


def match_string(s: str, l: List[str]) -> Optional[str]:
    compare_ratio: float = 0.5
    result: str = s

    for e in l:
        ratio: float = SM(None, s.lower(), e.lower()).ratio()
        if ratio > compare_ratio:
            compare_ratio = ratio
            result = e
        else:
            continue

    if s != result:
        return result
    else:
        return None


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.6f} secs")
        return value

    return wrapper_timer


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)  # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")  # 4
        return value

    return wrapper_debug