from pathlib import Path

import pytest
from PIL.Image import Image

from clickgen.cursors import CursorFrame, CursorImage
from clickgen.writer.windows import to_ani, to_cur, to_win


def test_windows_cur_writer(cursor_frame, x11_tmp_dir: Path):
    o = to_cur(cursor_frame)
    assert isinstance(o, bytes)

    cfile = x11_tmp_dir / "test.cur"
    cfile.write_bytes(o)

    assert cfile.exists()
    assert cfile.is_file()


def test_windows_cur_writer_re_canvas(image: Image, hotspot, delay):
    def cur_frame(size: int):
        i = image.resize(size=(size, size), resample=3)
        return CursorImage(i, hotspot, nominal=31)

    to_cur(
        CursorFrame(
            [
                cur_frame(20),
                cur_frame(40),
                cur_frame(60),
                cur_frame(90),
                cur_frame(120),
                cur_frame(250),
            ],
            delay,
        )
    )


def test_windows_cur_writer_raises(image: Image, hotspot, delay):
    i = image.resize(size=(500, 500), resample=3)
    c = CursorImage(i, hotspot, nominal=i.size[0])
    cf = CursorFrame([c], delay)

    with pytest.raises(ValueError):
        to_cur(cf)


def test_windows_ani_writer(cursor_frame: CursorFrame, x11_tmp_dir: Path):
    o = to_ani([cursor_frame, cursor_frame])
    assert isinstance(o, bytes)

    cfile = x11_tmp_dir / "test.ani"
    cfile.write_bytes(o)

    assert cfile.exists()
    assert cfile.is_file()


def test_windows_writer(cursor_frame: CursorFrame, x11_tmp_dir: Path):
    ext, o = to_win([cursor_frame, cursor_frame])
    assert isinstance(o, bytes)

    cfile = x11_tmp_dir / f"test.{ext}"
    cfile.write_bytes(o)

    assert cfile.exists()
    assert cfile.is_file()
    assert cfile.suffix == ".ani"

    ext1, o1 = to_win([cursor_frame])
    assert isinstance(o1, bytes)

    cfile1 = x11_tmp_dir / f"test.{ext1}"
    cfile1.write_bytes(o1)

    assert cfile1.exists()
    assert cfile1.is_file()
    assert cfile1.suffix == ".cur"
