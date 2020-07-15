#!/usr/bin/env python
# encoding: utf-8

import os
import json

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


def get_mock_animated_images_list() -> [str]:
    images: [str] = os.listdir(os.path.join(basedir, 'images'))
    animated_list: [str] = []

    for image in images:
        if '-' in image:
            animated_list.append(image)

    return animated_list


def get_mock_static_images_list() -> [str]:
    images: [str] = os.listdir(os.path.join(basedir, 'images'))
    animated_list: [str] = []

    for image in images:
        if '-' not in image:
            animated_list.append(image)

    return animated_list


def get_mock_hotspots() -> any:
    with open(os.path.join(basedir, 'hotspots.json')) as hotspots_file:
        return json.loads(hotspots_file.read())
