#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
# XCursor
#

import pytest
from clickgen.builders import XCursor


def test_XCursor_config_file_not_found_exception(image_dir) -> None:
    with pytest.raises(FileNotFoundError) as excinfo:
        XCursor(image_dir, image_dir)
    assert str(excinfo.value) == f"'{image_dir.name}' is not found or not a config file"


def test_XCursor(static_config, image_dir) -> None:
    x = XCursor(static_config, image_dir)
    assert x.config_file == static_config

    # We know 'out_dir' is not exists
    assert x.out_dir.exists() is True
    assert x.out_dir == image_dir / "cursors"
