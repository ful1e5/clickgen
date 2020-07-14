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


def get_mock_images_path() -> str:
    return os.path.join(basedir, 'images')


def get_mock_image() -> str:
    return os.path.join(basedir, 'images', 'mock_static.png')


def get_mock_images_list() -> [str]:
    return os.listdir(os.path.join(basedir, 'images'))
