from pathlib import Path

from clickgen.packer import pack_win


def test_windows_packer_with_cur(win_cur_tmp_dir: Path, theme_name, comment, website):
    pack_win(win_cur_tmp_dir, theme_name, comment, website)

    install_inf = win_cur_tmp_dir / "install.inf"
    uninstall_bat = win_cur_tmp_dir / "uninstall.bat"
    assert install_inf.exists()
    assert uninstall_bat.exists()
    install_data = install_inf.read_text()

    assert theme_name in install_data
    assert comment in install_data
    assert website in install_data

    for f in win_cur_tmp_dir.glob("*.cur"):
        print(f)
        assert f.name in install_data


def test_windows_packer_with_ani(win_ani_tmp_dir: Path, theme_name, comment, website):
    pack_win(win_ani_tmp_dir, theme_name, comment, website)

    install_inf = win_ani_tmp_dir / "install.inf"
    install_data = install_inf.read_text()

    for f in win_ani_tmp_dir.glob("*.ani"):
        assert f.name in install_data
