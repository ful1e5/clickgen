from pathlib import Path

from clickgen.writer.x11 import to_x11


def test_x11_writer(cursor_frame, x11_tmp_dir: Path):
    o = to_x11([cursor_frame])
    assert isinstance(o, bytes)

    xfile = x11_tmp_dir.joinpath("test")
    xfile.write_bytes(o)

    assert xfile.exists()
    assert xfile.is_file()
