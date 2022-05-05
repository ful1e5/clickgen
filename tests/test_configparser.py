from pathlib import Path

from clickgen.configparser import (
    parse_toml_config_section,
    parse_toml_file,
    parse_toml_theme_section,
)

td = {"theme": {"name": "test", "comment": "test", "website": "test"}}


def test_parse_toml_theme_section():
    t = parse_toml_theme_section(td)
    assert t.name == "test"
    assert t.comment == "test"
    assert t.website == "test"


def test_parse_toml_theme_section_with_kwargs():
    kwargs = {"name": "new", "comment": "new", "website": "new"}
    t = parse_toml_theme_section(td, **kwargs)
    assert t.name == kwargs["name"]
    assert t.comment == kwargs["comment"]
    assert t.website == kwargs["website"]


dd = {
    "config": {
        "bitmaps_dir": "test",
        "out_dir": "test",
        "platforms": "test",
        "x11_sizes": 10,
        "win_size": 11,
    }
}


def test_parse_toml_config_section():
    c = parse_toml_config_section("", dd)
    assert isinstance(c.bitmaps_dir, Path)
    assert c.bitmaps_dir.name is "test"
    assert c.bitmaps_dir.is_absolute()
    assert isinstance(c.out_dir, Path)
    assert c.out_dir.name is "test"
    assert c.out_dir.is_absolute()

    assert c.platforms == "test"
    assert c.x11_sizes == 10
    assert c.win_size == 11


def test_parse_toml_config_section_with_absolute_paths():
    dd["config"]["bitmaps_dir"] = Path("test").absolute()
    dd["config"]["out_dir"] = Path("test").absolute()

    c = parse_toml_config_section("", dd)

    assert isinstance(c.bitmaps_dir, Path)
    assert c.bitmaps_dir.is_absolute()
    assert str(c.bitmaps_dir) == str(dd["config"]["bitmaps_dir"])
    assert isinstance(c.out_dir, Path)
    assert str(c.out_dir) == str(dd["config"]["out_dir"])


def test_parse_toml_config_section_with_kwargs():

    kwargs = {
        "bitmaps_dir": "new",
        "out_dir": "new",
        "platforms": "new",
        "x11_sizes": [100, 10],
        "win_size": 110,
    }

    c = parse_toml_config_section("", dd, **kwargs)
    assert c.bitmaps_dir == kwargs["bitmaps_dir"]
    assert c.out_dir == kwargs["out_dir"]
    assert c.platforms == kwargs["platforms"]
    assert c.x11_sizes == kwargs["x11_sizes"]
    assert c.win_size == kwargs["win_size"]


def test_parse_toml_file(samples_dir: Path):
    fp = samples_dir / "sample.toml"
    c = parse_toml_file(str(fp.absolute()))
    assert c.cursors[0].win_cursor_name == "Default.cur"
    assert c.cursors[1].win_cursor_name == "Work.ani"

    assert c.cursors[0].x11_cursor_name == "left_ptr"
    assert c.cursors[1].x11_cursor_name == "wait"
