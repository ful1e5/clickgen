#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from argparse import Namespace
import shlex
import io
import struct
import math
from PIL import Image
from PIL import ImageFilter

p = struct.pack

program_name = 'anicursorgen'
program_version = '1.0.0'


def main(input_config: str, output_file: str, prefix: str):
    """
        'win.py' is restrong of 'anicursorgen.py'.
        'input_config' is path to config_file.
        'output_file' is a path to store process cursor.
        In 'input_config' & 'output_file' absolute or relative both aceptable.
        'prefix' is a path to '.png files' link in the config_file, if relative path implemented.
        Generate .cur & .ani files based on '.in' config file.
        anicursorgen.py main copy found at <https://github.com/ubuntu/yaru/blob/master/icons/src/cursors/anicursorgen.py>
    """

    args = Namespace(add_shadows=False,
                     blur=3.125,
                     color='0x00000040',
                     down_shift=3.125,
                     input_config='-',
                     output_file='-',
                     prefix=None,
                     right_shift=9.375)

    if (input_config is not None):
        args.input_config = input_config
    if (output_file is not None):
        args.output_file = output_file
    if (prefix is not None):
        args.prefix = prefix

    try:
        if args.color[0] != '0' or args.color[1] not in [
                'x', 'X'
        ] or len(args.color) != 10:
            raise ValueError
        args.color = (int(args.color[2:4], 16), int(args.color[4:6], 16),
                      int(args.color[6:8], 16), int(args.color[8:10], 16))
    except:
        print("Can't parse the color '{}'".format(args.color), file=sys.stderr)
        return 1

    if args.prefix is None:
        args.prefix = os.getcwd()

    if args.input_config == '-':
        input_config = sys.stdin
    else:
        input_config = open(args.input_config, 'rb')

    if args.output_file == '-':
        output_file = sys.stdout
    else:
        output_file = open(args.output_file, 'wb')

    result = make_cursor_from(input_config, output_file, args)

    input_config.close()
    output_file.close()

    return result


def make_cursor_from(inp, out, args):
    frames = parse_config_from(inp, args.prefix)

    animated = frames_have_animation(frames)

    if animated:
        result = make_ani(frames, out, args)
    else:
        buf = make_cur(frames, args)
        copy_to(out, buf)
        result = 0

    return result


def copy_to(out, buf):
    buf.seek(0, io.SEEK_SET)
    while True:
        b = buf.read(1024)
        if len(b) == 0:
            break
        out.write(b)


def frames_have_animation(frames):
    sizes = set()

    for frame in frames:
        if frame[4] == 0:
            continue
        if frame[0] in sizes:
            return True
        sizes.add(frame[0])

    return False


def make_cur(frames, args, animated=False):
    buf = io.BytesIO()
    buf.write(p('<HHH', 0, 2, len(frames)))
    frame_offsets = []

    # def frame_size_cmp(f1, f2):
    #     if f1[0] < f2[0]:
    #         return -1
    #     elif f1[0] > f2[0]:
    #         return 1
    #     else:
    #         return 0

    frames = sorted(frames, reverse=True)

    for frame in frames:
        width = frame[0]
        if width > 255:
            width = 0
        height = width
        buf.write(p('<BBBB HH', width, height, 0, 0, frame[1], frame[2]))
        size_offset_pos = buf.seek(0, io.SEEK_CUR)
        buf.write(p('<II', 0, 0))
        frame_offsets.append([size_offset_pos])

    for i, frame in enumerate(frames):
        frame_offset = buf.seek(0, io.SEEK_CUR)
        frame_offsets[i].append(frame_offset)

        frame_png = Image.open(frame[3])

        if args.add_shadows:
            succeeded, shadowed = create_shadow(frame_png, args)
            if succeeded == 0:
                frame_png.close()
                frame_png = shadowed


#   Windows 10 fails to read PNG-compressed cursors for some reason
#   and the information about storing PNG-compressed cursors is
#   sparse. This is why PNG compression is not used.
#   Previously this was conditional on cursor size (<= 48 to be uncompressed).
        compressed = False

        #   On the other hand, Windows 10 refuses to read very large
        #   uncompressed animated cursor files, but does accept
        #   PNG-compressed animated cursors for some reason. Go figure.
        if animated:
            compressed = True

        if compressed:
            write_png(buf, frame, frame_png)
        else:
            write_cur(buf, frame, frame_png)

        frame_png.close()

        frame_end = buf.seek(0, io.SEEK_CUR)
        frame_offsets[i].append(frame_end - frame_offset)

    for frame_offset in frame_offsets:
        buf.seek(frame_offset[0])
        buf.write(p('<II', frame_offset[2], frame_offset[1]))

    return buf


def make_framesets(frames):
    framesets = []
    sizes = set()

    # This assumes that frames are sorted
    size = 0
    for i, frame in enumerate(frames):
        if size == 0 or frame[0] != size:
            size = frame[0]
            counter = 0

            if size in sizes:
                print(
                    "Frames are not sorted: frame {} has size {}, but we have seen that already"
                    .format(i, size),
                    file=sys.stderr)
                return None

            sizes.add(size)

        if counter >= len(framesets):
            framesets.append([])

        framesets[counter].append(frame)
        counter += 1

    for i in range(1, len(framesets)):
        if len(framesets[i - 1]) != len(framesets[i]):
            print("Frameset {} has size {}, expected {}".format(
                i, len(framesets[i]), len(framesets[i - 1])),
                  file=sys.stderr)
            return None

    for frameset in framesets:
        for i in range(1, len(frameset)):
            if frameset[i - 1][4] != frameset[i][4]:
                print(
                    "Frameset {} has duration {} for framesize {}, but {} for framesize {}"
                    .format(i, frameset[i][4], frameset[i][0],
                            frameset[i - 1][4], frameset[i - 1][0]),
                    file=sys.stderr)
                return None

    # def frameset_size_cmp(f1, f2):
    #     if f1[0][0] < f2[0][0]:
    #         return -1
    #     elif f1[0][0] > f2[0][0]:
    #         return 1
    #     else:
    #         return 0

    framesets = sorted(framesets, reverse=True)

    return framesets


def make_ani(frames, out, args):
    framesets = make_framesets(frames)
    if framesets is None:
        return 1

    buf = io.BytesIO()

    buf.write(b'RIFF')
    riff_len_pos = buf.seek(0, io.SEEK_CUR)
    buf.write(p('<I', 0))
    riff_len_start = buf.seek(0, io.SEEK_CUR)

    buf.write(b'ACON')
    buf.write(b'anih')
    buf.write(
        p('<IIIIIIIIII', 36, 36, len(framesets), len(framesets), 0, 0, 32, 1,
          framesets[0][0][4], 0x01))

    rates = set()
    for frameset in framesets:
        rates.add(frameset[0][4])

    if len(rates) != 1:
        buf.write(b'rate')
        buf.write(p('<I', len(framesets) * 4))
        for frameset in framesets:
            buf.write(p('<I', frameset[0][4]))

    buf.write(b'LIST')
    list_len_pos = buf.seek(0, io.SEEK_CUR)
    buf.write(p('<I', 0))
    list_len_start = buf.seek(0, io.SEEK_CUR)

    buf.write(b'fram')

    for frameset in framesets:
        buf.write(b'icon')
        cur = make_cur(frameset, args, animated=True)
        cur_size = cur.seek(0, io.SEEK_END)
        # aligned_cur_size = cur_size
        # if cur_size % 4 != 0:
        #  aligned_cur_size += 4 - cur_size % 2
        buf.write(p('<i', cur_size))
        copy_to(buf, cur)
        pos = buf.seek(0, io.SEEK_END)
        if pos % 2 != 0:
            buf.write(('\x00' * (2 - (pos % 2))).encode())

    end_at = buf.seek(0, io.SEEK_CUR)
    buf.seek(riff_len_pos, io.SEEK_SET)
    buf.write(p('<I', end_at - riff_len_start))
    buf.seek(list_len_pos, io.SEEK_SET)
    buf.write(p('<I', end_at - list_len_start))

    copy_to(out, buf)

    return 0


def write_png(out, frame, frame_png):
    frame_png.save(out, "png", optimize=True)


def write_cur(out, frame, frame_png):
    pixels = frame_png.load()

    out.write(
        p('<I II HH IIIIII', 40, frame[0], frame[0] * 2, 1, 32, 0, 0, 0, 0, 0,
          0))

    for y in reversed(list(range(frame[0]))):
        for x in range(frame[0]):
            pixel = pixels[x, y]
            out.write(p('<BBBB', pixel[2], pixel[1], pixel[0], pixel[3]))

    acc = 0
    acc_pos = 0
    for y in reversed(list(range(frame[0]))):
        wrote = 0
        for x in range(frame[0]):
            if pixels[x, y][3] <= 127:
                acc = acc | (1 << acc_pos)
            acc_pos += 1
            if acc_pos == 8:
                acc_pos = 0
                out.write(chr(acc).encode())
                wrote += 1
        if wrote % 4 != 0:
            out.write(b'\x00' * (4 - wrote % 4))


def parse_config_from(inp, prefix):
    frames = []
    for line in inp.readlines():
        line = line.decode()
        words = shlex.split(line.rstrip('\n').rstrip('\r'))
        # print(words)
        if len(words) < 4:
            continue

        try:
            size = int(words[0])
            # print(size)
            hotx = int(words[1]) - 1
            # print(hotx)
            hoty = int(words[2]) - 1
            # print(hoty)
            filename = words[3]
            # print(filename)
            if not os.path.isabs(filename):
                filename = prefix + '/' + filename
        except:
            continue

        if len(words) > 4:
            try:
                duration = int(words[4])
            except:
                continue
        else:
            duration = 0

        frames.append((size, hotx, hoty, filename, duration))

    return frames


def create_shadow(orig, args):
    blur_px = orig.size[0] / 100.0 * args.blur
    right_px = int(orig.size[0] / 100.0 * args.right_shift)
    down_px = int(orig.size[1] / 100.0 * args.down_shift)

    shadow = Image.new('RGBA', orig.size, (0, 0, 0, 0))
    shadowize(shadow, orig, args.color)
    shadow.load()

    if args.blur > 0:
        crop = (int(math.floor(-blur_px)), int(math.floor(-blur_px)),
                orig.size[0] + int(math.ceil(blur_px)),
                orig.size[1] + int(math.ceil(blur_px)))
        right_px += int(math.floor(-blur_px))
        down_px += int(math.floor(-blur_px))
        shadow = shadow.crop(crop)
        flt = ImageFilter.GaussianBlur(blur_px)
        shadow = shadow.filter(flt)
    shadow.load()

    shadowed = Image.new('RGBA', orig.size, (0, 0, 0, 0))
    shadowed.paste(shadow, (right_px, down_px))
    shadowed.crop((0, 0, orig.size[0], orig.size[1]))
    shadowed = Image.alpha_composite(shadowed, orig)

    return 0, shadowed


def shadowize(shadow, orig, color):
    o_pxs = orig.load()
    s_pxs = shadow.load()
    for y in range(orig.size[1]):
        for x in range(orig.size[0]):
            o_px = o_pxs[x, y]
            if o_px[3] > 0:
                s_pxs[x, y] = (color[0], color[1], color[2],
                               int(color[3] * (o_px[3] / 255.0)))


# if __name__ == '__main__':
# sys.exit(main())
