import pytest

from clickgen.cursors import CursorFrame, CursorImage
from clickgen.parser.png import SIZES, MultiPNGParser, SinglePNGParser


def test_single_png_parser(blob, hotspot, sizes, delay):
    p = SinglePNGParser(blob, hotspot, sizes=sizes, delay=delay)

    sizes = [12, 24]
    assert sorted(list(p.sizes)) == sizes

    assert p.delay == delay

    for i, s in enumerate(sizes):
        assert isinstance(p.frames[0], CursorFrame)
        assert isinstance(p.frames[0][i], CursorImage)
        assert p.frames[0][i].nominal == s
        assert p.frames[0][i].image.size == (s, s)

    assert p.frames[0][0].hotspot == (6, 6)
    assert p.frames[0][1].hotspot == (12, 12)

    with pytest.raises(IndexError):
        p.frames[1]


def test_single_png_parser_default_args(blob, hotspot):
    p = SinglePNGParser(blob, hotspot)
    assert p.delay == 0
    assert sorted(list(p.sizes)) == SIZES


def test_single_png_parser_can_parse(blob, dummy_blob):
    assert SinglePNGParser.can_parse(blob)
    assert not SinglePNGParser.can_parse(dummy_blob)


def test_single_png_parser_raises_01(blob):
    with pytest.raises(ValueError):
        SinglePNGParser(blob, hotspot=(201, 201))
    with pytest.raises(ValueError):
        SinglePNGParser(blob, hotspot=(100, 201))
    with pytest.raises(ValueError):
        SinglePNGParser(blob, hotspot=(201, 100))


def test_multi_png_parser(blobs, hotspot, sizes, delay):
    p = MultiPNGParser(blobs, hotspot, sizes, delay)

    assert p.frames[0].delay == delay
    assert p.frames[1].delay == delay

    for i in [0, 1]:
        for j, s in enumerate(sorted(set(sizes))):
            assert isinstance(p.frames[i], CursorFrame)
            assert isinstance(p.frames[i][j], CursorImage)
            assert p.frames[i][j].nominal == s
            assert p.frames[i][j].image.size == (s, s)


def test_multi_png_parser_can_parse(blobs, dummy_blobs):
    assert MultiPNGParser.can_parse(blobs)
    assert not SinglePNGParser.can_parse(dummy_blobs)
