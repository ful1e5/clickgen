from pathlib import Path

from clickgen.configparser import (
    parse_config_section,
    parse_theme_section,
    parse_toml_file,
)

td = {"theme": {"name": "test", "comment": "test", "website": "test"}}


def test_parse_theme_section():
    t = parse_theme_section(td)
    assert t.name == "test"
    assert t.comment == "test"
    assert t.website == "test"


def test_parse_theme_section_with_kwargs():
    kwargs = {"name": "new", "comment": "new", "website": "new"}
    t = parse_theme_section(td, **kwargs)
    assert t.name == kwargs["name"]
    assert t.comment == kwargs["comment"]
    assert t.website == kwargs["website"]


dd1 = {
    "config": {
        "bitmaps_dir": "test",
        "out_dir": "test",
        "platforms": "test",
        "x11_sizes": 10,
        "win_size": 11,
    }
}


def test_win_size_deprecation_message(capsys):
    parse_config_section("", dd1)

    captured = capsys.readouterr()
    assert (
        "Warning: Option 'win_size' is deprecated. Use 'win_sizes' inside individual cursor settings or set to 'cursor.fallback'"
        in captured.out
    )


def test_x11_sizes_deprecation_message(capsys):
    parse_config_section("", dd1)

    captured = capsys.readouterr()
    assert (
        "Warning: Option 'x11_size' is deprecated. Use 'x11_sizes' inside individual cursor settings or set to 'cursor.fallback'"
        in captured.out
    )


dd2 = {
    "config": {
        "bitmaps_dir": "test",
        "out_dir": "test",
        "platforms": "test",
    }
}


def test_parse_config_section():
    c = parse_config_section("", dd2)
    assert isinstance(c.bitmaps_dir, Path)
    assert c.bitmaps_dir.name is "test"
    assert c.bitmaps_dir.is_absolute()
    assert isinstance(c.out_dir, Path)
    assert c.out_dir.name is "test"
    assert c.out_dir.is_absolute()

    assert c.platforms == "test"


def test_parse_config_section_with_absolute_paths():
    dd2["config"]["bitmaps_dir"] = str(Path("test").absolute())
    dd2["config"]["out_dir"] = str(Path("test").absolute())

    c = parse_config_section("", dd2)

    assert isinstance(c.bitmaps_dir, Path)
    assert c.bitmaps_dir.is_absolute()
    assert str(c.bitmaps_dir) == dd2["config"]["bitmaps_dir"]
    assert isinstance(c.out_dir, Path)
    assert str(c.out_dir) == dd2["config"]["out_dir"]


def test_parse_config_section_with_kwargs():
    kwargs = {
        "bitmaps_dir": "new",
        "out_dir": "new",
        "platforms": "new",
    }

    c = parse_config_section("", dd2, **kwargs)
    assert c.bitmaps_dir == kwargs["bitmaps_dir"]
    assert c.out_dir == kwargs["out_dir"]
    assert c.platforms == kwargs["platforms"]


def test_parse_file(samples_dir: Path):
    fp = samples_dir / "sample.toml"
    c = parse_toml_file(str(fp.absolute()))
    assert c.cursors[0].win_cursor_name == "Default.cur"
    assert c.cursors[1].win_cursor_name == "Work.ani"

    assert c.cursors[0].x11_cursor_name == "left_ptr"
    assert c.cursors[1].x11_cursor_name == "wait"
