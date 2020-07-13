#!/usr/bin/env python
# encoding: utf-8

# TODO: Tests

import os
import itertools
from PIL import Image

from ..helpers import get_logger
from ..types import Path, IntegerList, StringList, IntegerTuple, CoordinateTuple, Logger


# Logger
logger: Logger = get_logger('clickgen:configsgen')

# Default configs path is <working_dir>/configs/
DEFAULT_CONFIGS_PATH = os.path.join(os.getcwd(), 'configs')


def get_cursor_list(imgs_dir: Path, animated: bool = False) -> StringList:
    all_curosr_list, cursor_list = [], []

    for file_path in os.listdir(imgs_dir):
        all_curosr_list.append(os.path.basename(file_path))

    if (animated):
        # animated cursor have filename-01,02,03..n postfix
        temp: StringList = [cursor for cursor in all_curosr_list if
                            cursor.find("-") >= 0]
        temp.sort()
        cursor_list: StringList = [list(g) for _, g in itertools.groupby(
            temp, lambda x: x.partition("-")[0])]
    else:
        for cursor in all_curosr_list:
            if cursor.find("-") <= 0:
                cursor_list.append(cursor)
        cursor_list.sort()

    return cursor_list


def resize_cursor(cursor: str, size: IntegerList, imgs_dir: Path, coordinates: CoordinateTuple, out_dir: Path = DEFAULT_CONFIGS_PATH) -> IntegerTuple:

    # helper variables
    in_path = os.path.join(imgs_dir, cursor)
    out_dir = os.path.join(out_dir, '%sx%s' % (size, size))
    out_path = os.path.join(out_dir, cursor)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # opening original image
    image = Image.open(in_path)

    width = image.size[0]
    height = image.size[1]

    aspect = width / float(height)

    ideal_width = size
    ideal_height = size

    ideal_aspect = ideal_width / float(ideal_height)

    if aspect > ideal_aspect:
        # Then crop the left and right edges:
        new_width = int(ideal_aspect * height)
        offset = (width - new_width) / 2
        resize = (offset, 0, width - offset, height)
    else:
        # ... crop the top and bottom:
        new_height = int(width / ideal_aspect)
        offset = (height - new_height) / 2
        resize = (0, offset, width, height-offset)

    thumb = image.crop(resize).resize(
        (ideal_width, ideal_height), Image.ANTIALIAS)

    # save resized image
    thumb.save(out_path)

    #  finding new X & Y coordinates
    if coordinates is None:
        Rx = Ry = int(size / 2)
    else:
        (xhot, yhot) = coordinates
        Rx = round(size / width * xhot)
        Ry = round(size / height * yhot)

    return (Rx, Ry)


def write_xcur(config_file_path: Path, content: StringList) -> None:
    # sort line, So all lines in order according to size (24x24, 28x28, ..)
    content.sort()

    # remove newline end of file `xcursorgen` generate error
    content[-1] = content[-1].rstrip("\n")

    with open(config_file_path, "w") as config_file:
        for line in content:
            config_file.write(line)
        config_file.close()


def generate_static_cursor(imgs_dir: Path, out_dir: Path, sizes: IntegerList, hotspots: any) -> None:
    list: StringList = get_cursor_list(imgs_dir)

    for cursor in list:

        config_file_path: Path = os.path.join(
            out_dir, cursor.replace(".png", ".in"))

        content: StringList = []

        # setting Hotspots from JSON data
        # set to `None` if not have JSON data or `key` not in JSON
        cursor_name = cursor.split('.')[0]
        coordinate: CoordinateTuple = None

        try:
            hotspot = hotspots[cursor_name]
            xhot: int = hotspot['xhot']
            yhot: int = hotspot['yhot']
            coordinate = (xhot, yhot)
        except TypeError:
            xhot = None
            yhot = None

        for size in sizes:
            resized_xhot, resized_yhot = resize_cursor(
                cursor, size, imgs_dir, coordinate, out_dir=out_dir)

            logger.info('%sx%s %s hotspots set to (%s,%s)' %
                        (size, size, cursor_name, resized_xhot, resized_yhot))

            line = "%s %s %s %sx%s/%s\n" % (size,
                                            resized_xhot, resized_yhot, size, size, cursor)
            content.append(line)

        write_xcur(config_file_path, content)


def generate_animated_cursor(imgs_dir: Path, out_dir: Path, sizes: IntegerList, hotspots: any):
    list: StringList = get_cursor_list(imgs_dir, animated=True)
    delay: int = 20

    for group in list:
        group_name = str(group[0]).split("-")[0]
        config_file_path: Path = os.path.join(out_dir, group_name + ".in")

        content: StringList = []

        # setting Hotspots from JSON data
        # set to `None` if not have JSON data or `key` not in JSON
        coordinate: CoordinateTuple = None

        try:
            hotspot = hotspots[group_name]
            xhot = hotspot['xhot']
            yhot = hotspot['yhot']
            coordinate = (xhot, yhot)
        except TypeError:
            xhot = None
            yhot = None

        for cursor in group:
            for size in sizes:
                resized_xhot, resized_yhot = resize_cursor(
                    cursor, size, imgs_dir, coordinate, out_dir=out_dir)

                logger.info('%sx%s %s hotspots set to (%s,%s)' %
                            (size, size, group_name, resized_xhot, resized_yhot))

                line = "%s %s %s %sx%s/%s %s\n" % (size,
                                                   resized_xhot, resized_yhot, size, size, cursor, delay)
            content.append(line)

        write_xcur(config_file_path, content)


def main(imgs_dir: Path, cursor_sizes: IntegerList, hotspots: any, out_dir: Path = DEFAULT_CONFIGS_PATH) -> Path:
    """
        Generate Configs files.
        hotspots is JSON data for each cursor having xhot & yhot parameters.
        Provide `None` value set hotspots to middle of cursor.
        hotspots is default set to `None`
    """

    logger.info('configs are writen to %s' % out_dir)

    generate_static_cursor(imgs_dir, sizes=cursor_sizes,
                           hotspots=hotspots, out_dir=out_dir)
    # generate_animated_cursor(imgs_dir, sizes=cursor_sizes,
    #                          hotspots=hotspots, out_dir=out_dir)

    return (os.path.abspath(out_dir))
