from pathlib import Path

from clickgen.configparser import (
    ClickgenConfig,
    parse_config_file,
    parse_config_section,
    parse_json_file,
    parse_theme_section,
    parse_toml_file,
    parse_yaml_file,
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
        "The 'win_size' option is deprecated."
        " Please use 'win_sizes' within individual cursor settings or set it to '[cursor.fallback_settings]'."
        " For more information, visit: https://github.com/ful1e5/clickgen/discussions/59#discussioncomment-6747666"
        in captured.out
    )


def test_x11_sizes_deprecation_message(capsys):
    parse_config_section("", dd1)

    captured = capsys.readouterr()
    assert (
        "The 'x11_sizes' option is deprecated."
        " Please use 'x11_sizes' within individual cursor settings or set it to '[cursor.fallback_settings]'."
        " For more information, visit: https://github.com/ful1e5/clickgen/discussions/59#discussioncomment-6747666"
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


def assert_clickgen_config(c: ClickgenConfig):
    assert c.theme.name == "Sample"
    assert c.theme.comment == "This is sample cursor theme"
    assert c.theme.website == "https://www.example.com/"

    x11_list = [
        "pointer1",
        "pointer2",
        "pointer3",
        "pointer4",
        "pointer5",
        "pointer6",
        "pointer7",
        "pointer8",
        "pointer9",
        "pointer10",
        "pointer11",
        "pointer12",
        "pointer13",
        "wait1",
        "wait2",
    ]
    win_list = [
        "Default.cur",
        "Alternate.cur",
        "Cross.cur",
        "Diagonal_1.cur",
        "Diagonal_2.cur",
        "Handwriting.cur",
        "Help.cur",
        "Horizontal.cur",
        "IBeam.cur",
        "Link.cur",
        "Move.cur",
        "Unavailiable.cur",
        "Vertical.cur",
        "Busy.ani",
        "Work.ani",
    ]

    for cur in c.cursors:
        assert cur.win_cursor_name in win_list
        assert cur.x11_cursor_name in x11_list


def test_parse_toml_file(samples_dir: Path):
    fp = samples_dir / "sample.toml"
    c: ClickgenConfig = parse_toml_file(str(fp.absolute()))
    assert_clickgen_config(c)


def test_parse_yaml_file(samples_dir: Path):
    fp = samples_dir / "sample.yaml"
    c: ClickgenConfig = parse_yaml_file(str(fp.absolute()))
    assert_clickgen_config(c)


def test_parse_json_file(samples_dir: Path):
    fp = samples_dir / "sample.json"
    c: ClickgenConfig = parse_json_file(str(fp.absolute()))
    assert_clickgen_config(c)


def test_parse_config_files(samples_dir: Path):
    for ext in ["json", "yaml", "toml"]:
        fp = samples_dir / f"sample.{ext}"
        c: ClickgenConfig = parse_config_file(str(fp.absolute()))
        assert_clickgen_config(c)
