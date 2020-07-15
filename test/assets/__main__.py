#!/usr/bin/env python
# encoding: utf-8

import os
import json

basedir = os.path.dirname(__file__)

# configs
mock_config_path = os.path.join(basedir, 'configs')
static_mock_config_path = os.path.join(mock_config_path, 'mock_static.in')
animated_mock_config_path = os.path.join(mock_config_path, 'mock_animated.in')

# images
mock_images_path = os.path.join(basedir, 'images')
mock_image = os.path.join(mock_images_path, 'mock_static.png')


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
