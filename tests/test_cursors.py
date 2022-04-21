import pytest

from clickgen.cursors import CursorFrame, CursorImage


def test_cursor_image(cursor_image, image, hotspot, nominal):
    assert isinstance(cursor_image, CursorImage)

    assert cursor_image.image is image
    assert cursor_image.hotspot is hotspot
    assert cursor_image.nominal is nominal

    assert "hotspot=(100, 105)" in repr(cursor_image)
    assert "nominal=24" in repr(cursor_image)


def test_cursor_frame(cursor_frame, cursor_image, images, delay):
    assert isinstance(cursor_frame, CursorFrame)

    assert cursor_frame.images is images
    assert cursor_frame.delay is delay

    assert len(cursor_frame) == 3

    for i in range(10):
        if i > 2:
            with pytest.raises(IndexError):
                cursor_frame.__getitem__(i)
        else:
            item = cursor_frame.__getitem__(i)
            assert item == cursor_image
            assert isinstance(item, CursorImage)

    for c in iter(cursor_frame):
        assert isinstance(c, CursorImage)

    assert "delay=5" in repr(cursor_frame)
