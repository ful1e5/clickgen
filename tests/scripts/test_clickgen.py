import argparse
from unittest import mock

import pytest

from clickgen.parser.png import DELAY, SIZES
from clickgen.scripts.clickgen import main


def test_clickgen_all_cursor_build(samples_dir, x11_tmp_dir, hotspot):
    fp = samples_dir / "pngs/pointer.png"
    with open(fp, "rb") as f:
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=argparse.Namespace(
                files=[f],
                output=x11_tmp_dir,
                hotspot_x=hotspot[0],
                hotspot_y=hotspot[1],
                sizes=SIZES,
                delay=DELAY,
                platform="all",
            ),
        ):
            main()


def test_clickgen_all_x11_build(samples_dir, x11_tmp_dir, hotspot):
    fp = samples_dir / "pngs/pointer.png"
    with open(fp, "rb") as f:
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=argparse.Namespace(
                files=[f],
                output=x11_tmp_dir,
                hotspot_x=hotspot[0],
                hotspot_y=hotspot[1],
                sizes=SIZES,
                delay=DELAY,
                platform="x11",
            ),
        ):
            main()


def test_clickgen_all_windows_build(samples_dir, x11_tmp_dir, hotspot):
    fp = samples_dir / "pngs/pointer.png"
    with open(fp, "rb") as f:
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=argparse.Namespace(
                files=[f],
                output=x11_tmp_dir,
                hotspot_x=hotspot[0],
                hotspot_y=hotspot[1],
                sizes=SIZES,
                delay=DELAY,
                platform="windows",
            ),
        ):
            main()


def test_clickgen_raises(capsys, samples_dir, x11_tmp_dir, hotspot):
    fp = samples_dir / "sample.toml"
    with open(fp, "rb") as f:
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=argparse.Namespace(
                files=[f],
                output=x11_tmp_dir,
                hotspot_x=hotspot[0],
                hotspot_y=hotspot[1],
                sizes=SIZES,
                delay=DELAY,
                platform="all",
            ),
        ):
            main()
            captured = capsys.readouterr()
            assert "Error occurred while processing sample.toml" in captured.err
