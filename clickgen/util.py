#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import os
import shutil
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Union


def remove_util(p: Union[str, Path]) -> None:
    """ Remove this file, directory or symlink. If Path exits on filesystem."""

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
def chdir(dir: Union[str, Path]):
    """
    Temporary change `working` directory. Use this in `with` syntax.

    :dir: path to directory.
    """

    prev_cwd = os.getcwd()
    os.chdir(str(dir))
    try:
        yield
    finally:
        os.chdir(prev_cwd)


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