from unittest.mock import patch

import pytest

from clickgen.parser.base import BaseParser


def test_base_parser(blob):
    p = patch.multiple(BaseParser, __abstractmethods__=set())
    p.start()

    b = BaseParser(blob)  # type: ignore

    assert isinstance(b.blob, bytes)
    assert b.blob is blob

    with pytest.raises(AttributeError):
        b.frames

    with pytest.raises(NotImplementedError):
        b.can_parse(blob)

    p.stop()
