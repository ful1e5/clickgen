from pathlib import Path

from clickgen.packer import pack_x11


def test_x11_packer(x11_tmp_dir: Path):
    pack_x11(x11_tmp_dir, theme_name="test", comment="test")

    f1 = x11_tmp_dir / "cursor.theme"
    f2 = x11_tmp_dir / "index.theme"

    assert f1.exists()
    assert f2.exists()

    assert f1.read_text() == '[Icon Theme]\nName=test\nInherits="test"'
    assert f2.read_text() == '[Icon Theme]\nName=test\nComment=test\nInherits="hicolor"'
