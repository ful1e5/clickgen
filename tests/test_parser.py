import pytest

from clickgen.parser import open_blob


def test_open_blob(blob, dummy_blob, blobs, dummy_blobs, hotspot):
    open_blob(blob, hotspot)
    with pytest.raises(Exception):
        open_blob(dummy_blob, hotspot)

    open_blob(blobs, hotspot)
    with pytest.raises(Exception):
        open_blob(dummy_blobs, hotspot)
