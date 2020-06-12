#!/usr/bin/env python
# encoding: utf-8

import os

basedir = os.path.dirname(__file__)
mock_config_path = os.path.join(basedir, 'configs')


def get_static_mock_config_path() -> str:
    path = os.path.join(mock_config_path, 'mock_static.in')
    return path


def get_animated_mock_config_path() -> str:
    return os.path.join(mock_config_path, 'mock_animated.in')
