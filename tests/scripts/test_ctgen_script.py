import argparse
import os
from pathlib import Path
from unittest import mock

from clickgen.scripts.ctgen import cwd, get_kwargs, main


def test_get_kwargs():
    d1 = {
        "name": "test",
        "comment": "test",
        "website": "test",
        "platforms": "test",
        "sizes": [10, 10],
        "bitmaps_dir": "test",
        "out_dir": "test",
    }
    args1 = argparse.Namespace(**d1)
    res1 = get_kwargs(args1)

    assert isinstance(res1, dict)
    assert res1["name"] == d1["name"]
    assert isinstance(res1["bitmaps_dir"], Path)
    assert isinstance(res1["out_dir"], Path)
    assert res1["x11_sizes"] == d1["sizes"]
    assert res1["win_sizes"] == d1["sizes"]

    for k in ["name", "bitmaps_dir", "out_dir", "sizes"]:
        del d1[k]
    for i, v in d1.items():
        assert res1[i] == v


def test_cwd(x11_tmp_dir: Path):
    current_dir = os.getcwd()
    with cwd(x11_tmp_dir):  # type: ignore
        assert os.getcwd() == str(x11_tmp_dir)
    assert os.getcwd() == current_dir


def test_ctgen_file_exception(samples_dir, x11_tmp_dir, capsys):
    fp = samples_dir / "pngs/pointer.png"
    with open(fp, "rb") as f:
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=argparse.Namespace(
                files=[f],
                name=None,
                comment=None,
                website=None,
                platforms=["x11"],
                sizes=None,
                bitmaps_dir=None,
                out_dir=x11_tmp_dir,
            ),
        ):
            main()
            captured = capsys.readouterr()
            assert "Error occurred while processing pointer.png:" in captured.err


def test_ctgen_with_x11_platform(samples_dir, x11_tmp_dir):
    fp = samples_dir / "sample.toml"
    with open(fp, "rb") as f:
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=argparse.Namespace(
                files=[f],
                name=None,
                comment=None,
                website=None,
                platforms=["x11"],
                sizes=None,
                bitmaps_dir=None,
                out_dir=x11_tmp_dir,
            ),
        ):
            main()


def test_ctgen_with_windows_platform(samples_dir, x11_tmp_dir, capsys):
    fp = samples_dir / "sample.toml"
    with open(fp, "rb") as f:
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=argparse.Namespace(
                files=[f],
                name=None,
                comment=None,
                website=None,
                platforms=["windows"],
                sizes=None,
                bitmaps_dir=None,
                out_dir=x11_tmp_dir,
            ),
        ):
            main()
            captured = capsys.readouterr()
            assert (
                "Error occurred while packaging windows theme 'Sample':" in captured.err
            )
