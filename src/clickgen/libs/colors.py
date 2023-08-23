#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class bcolors:
    BOLD = "\033[1m"

    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    MAGENTA = "\033[95m"
    YELLOW = "\033[93m"
    RED = "\033[91m"

    NORMAL = "\033[0m"


# Text Formate
def bold(s: str) -> str:
    return f"{bcolors.BOLD}{s}{bcolors.NORMAL}"


# Colors
def blue(s: str) -> str:
    return f"{bcolors.BLUE}{s}{bcolors.NORMAL}"


def cyan(s: str) -> str:
    return f"{bcolors.CYAN}{s}{bcolors.NORMAL}"


def green(s: str) -> str:
    return f"{bcolors.GREEN}{s}{bcolors.NORMAL}"


def magenta(s: str) -> str:
    return f"{bcolors.MAGENTA}{s}{bcolors.NORMAL}"


def red(s: str) -> str:
    return f"{bcolors.RED}{s}{bcolors.NORMAL}"


def yellow(s: str) -> str:
    return f"{bcolors.YELLOW}{s}{bcolors.NORMAL}"


# Styling
def print_text(s: str) -> None:
    print(f"{bold(blue(' -'))} {s}")


def print_subtext(s: str) -> None:
    print(f"{bold('  ::')} {s}")


def print_info(s: str) -> None:
    print(f"[Info] {s}")


def print_done(s: str) -> None:
    print(f"{green('[Done]')} {s}")


def print_warning(s: str) -> None:
    print(f"{yellow('[Warning]')} {s}")


def fail(s: str) -> str:
    return bold(red(f"[Fail] {s}"))
