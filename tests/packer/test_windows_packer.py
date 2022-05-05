from pathlib import Path

import pytest

from clickgen.packer import pack_win
from clickgen.packer.windows import REQUIRED_CURSORS


def test_windows_packer_raises(x11_tmp_dir: Path, theme_name, comment, website):
    x11_tmp_dir.joinpath("Work.ani").write_text("test")

    with pytest.raises(FileNotFoundError) as e1:
        pack_win(x11_tmp_dir, theme_name, comment, website)

    assert (
        "Windows cursors are missing ['Alternate', 'Busy', 'Cross', 'Default', 'Diagonal_1', 'Diagonal_2', 'Handwriting', 'Help', 'Horizontal', 'IBeam', 'Link', 'Move', 'Unavailiable', 'Vertical']"
        in str(e1.value)
    )


def test_windows_packer_with_cur(win_cur_tmp_dir: Path, theme_name, comment, website):
    pack_win(win_cur_tmp_dir, theme_name, comment, website)

    install_inf = win_cur_tmp_dir.joinpath("install.inf")
    uninstall_bat = win_cur_tmp_dir.joinpath("uninstall.bat")
    assert install_inf.exists()
    assert uninstall_bat.exists()
    install_data = install_inf.read_text()

    assert theme_name in install_data
    assert comment in install_data
    assert website in install_data

    for c in REQUIRED_CURSORS:
        fname = f"{c}.cur"
        assert win_cur_tmp_dir.joinpath(fname).exists()
        assert fname in install_data


def test_windows_packer_with_ani(win_ani_tmp_dir: Path, theme_name, comment, website):
    pack_win(win_ani_tmp_dir, theme_name, comment, website)

    install_inf = win_ani_tmp_dir.joinpath("install.inf")
    install_data = install_inf.read_text()

    for c in REQUIRED_CURSORS:
        fname = f"{c}.ani"
        assert win_ani_tmp_dir.joinpath(fname).exists()
        assert fname in install_data
