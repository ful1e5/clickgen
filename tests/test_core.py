#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. moduleauthor:: Kaiz Khatri <kaizmandhu@gmail.com>
"""

import shutil
import tempfile
from pathlib import Path
from random import randint
from typing import List, Optional

import pytest
from PIL import Image

from clickgen.core import Bitmap, CursorAlias

from .utils import create_test_image

#
# Bitmap Test Cases
#


def test_static_Bitmap_as_str(static_png, hotspot) -> None:
    """Testing Bitmap class members value for **static png**."""
    str_static_png = str(static_png)
    bmp = Bitmap(str_static_png, hotspot)

    with pytest.raises(AttributeError) as excinfo:
        assert bmp.grouped_png
    assert str(excinfo.value) == "'Bitmap' object has no attribute 'grouped_png'"

    assert bmp.png == static_png
    assert bmp.animated is False
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test-0"
    assert bmp.x_hot == hotspot[0]
    assert bmp.y_hot == hotspot[1]


def test_animated_Bitmap_as_str(animated_png, hotspot) -> None:
    """Testing Bitmap class members value for **animated png**."""
    str_animated_png: List[str] = list(map(lambda x: str(x.absolute()), animated_png))
    bmp = Bitmap(str_animated_png, hotspot)

    with pytest.raises(AttributeError) as excinfo:
        assert bmp.png
    assert str(excinfo.value) == "'Bitmap' object has no attribute 'png'"

    assert bmp.grouped_png == animated_png
    assert bmp.animated is True
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test"
    assert bmp.x_hot == hotspot[0]
    assert bmp.y_hot == hotspot[1]


def test_static_Bitmap_as_Path(static_png, hotspot) -> None:
    """Testing Bitmap class with passing args as `Path` type for \
    **static png**.
    """
    bmp = Bitmap(static_png, hotspot)

    with pytest.raises(AttributeError) as excinfo:
        assert bmp.grouped_png
    assert str(excinfo.value) == "'Bitmap' object has no attribute 'grouped_png'"

    assert bmp.png == static_png
    assert bmp.animated is False
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test-0"
    assert bmp.x_hot == hotspot[0]
    assert bmp.y_hot == hotspot[1]


def test_animated_Bitmap_as_Path(animated_png, hotspot) -> None:
    """Testing Bitmap class with passing args as `Path` type for \
    **animated png**.
    """
    bmp = Bitmap(animated_png, hotspot)

    with pytest.raises(AttributeError) as excinfo:
        assert bmp.png
    assert str(excinfo.value) == "'Bitmap' object has no attribute 'png'"

    assert bmp.grouped_png == animated_png
    assert bmp.animated is True
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test"
    assert bmp.x_hot == hotspot[0]
    assert bmp.y_hot == hotspot[1]


@pytest.mark.parametrize(
    "png",
    [
        bytes(),
        [bytes()],
        [bytes(), bytes()],
        (2),
        [(2)],
        [(2), (2)],
        [2],
        [[2]],
        [[2], [2]],
        2,
        [2],
        [2, 2],
    ],
)
def test_Bitmap_png_type_error_exception(png, hotspot) -> None:
    """Testing Bitmap class ``TypeError`` exception."""
    with pytest.raises(TypeError):
        assert Bitmap(png, hotspot)


notfound = "notfound.png"
notfound_path = Path.cwd() / notfound


@pytest.mark.parametrize(
    "png",
    [
        notfound,
        [notfound],
        [notfound, notfound, notfound],
        notfound_path,
        [notfound_path],
        [notfound_path, notfound_path, notfound_path],
    ],
)
def test_Bitmap_png_not_found_exception(png, hotspot) -> None:
    """Testing Bitmap class ``FileNotFoundError`` exception."""
    with pytest.raises(FileNotFoundError):
        assert Bitmap(png, hotspot)


def test_Bitmap_non_png_exception(test_file, hotspot) -> None:
    """Testing Bitmap class ``ValueError`` (Not a valid image type) exception."""
    with pytest.raises(ValueError):
        assert Bitmap(test_file, hotspot)


def test_static_Bitmap_hotspot_underflow_exception(static_png) -> None:
    """Testing Bitmap class hotspot ``ValueError`` (provided ``hotspot`` is \
    smaller than image pixel size) exception for static png.
    """
    with pytest.raises(ValueError):
        assert Bitmap(static_png, (2, -3))
        assert Bitmap(static_png, (-2, -3))


def test_animated_Bitmap_hotspot_underflow_exception(animated_png) -> None:
    """Testing Bitmap class hotspot ``ValueError`` (provided ``hotspot`` is \
    smaller than image pixel size) exception for animated png.
    """
    with pytest.raises(ValueError):
        assert Bitmap(animated_png, (2, -3))
        assert Bitmap(animated_png, (-2, -3))


def test_static_Bitmap_hotspot_overflow_exception(static_png) -> None:
    """Testing Bitmap class hotspot ``ValueError`` (provided ``hotspot`` is \
    larger than image pixel size) exception for static png.
    """
    with pytest.raises(ValueError):
        assert Bitmap(static_png, (12, 60))
        assert Bitmap(static_png, (55, 60))


def test_animated_Bitmap_hotspot_overflow_exception(animated_png) -> None:
    """Testing Bitmap class hotspot ``ValueError`` (provided ``hotspot`` is \
    larger than image pixel size) exception for animated png.
    """
    with pytest.raises(ValueError):
        assert Bitmap(animated_png, (12, 60))
        assert Bitmap(animated_png, (55, 60))


def test_static_Bitmap_str(static_png, hotspot) -> None:
    """Testing Bitmap class ``__str__`` datamethod for **static png**."""
    bmp = Bitmap(static_png, hotspot)
    assert (
        bmp.__str__()
        == f"Bitmap(png={static_png}, key={static_png.stem}, animated=False, size=(20, 20), width=20, height=20, x_hot={hotspot[0]}, y_hot={hotspot[1]})"
    )


def test_animated_Bitmap_str(animated_png, hotspot) -> None:
    """Testing Bitmap class ``__str__`` datamethod for **animated png**."""
    bmp = Bitmap(animated_png, hotspot)
    assert (
        bmp.__str__()
        == f"Bitmap(grouped_png={animated_png}, key={animated_png[0].stem.rsplit('-',1)[0]}, animated=True, size=(20, 20), width=20, height=20, x_hot={hotspot[0]}, y_hot={hotspot[1]})"
    )


def test_static_Bitmap_repr(static_png, hotspot) -> None:
    """Testing Bitmap class ``__repr__`` datamethod for **static png**."""
    bmp = Bitmap(static_png, hotspot)
    assert (
        bmp.__repr__()
        == f"{{ 'png':{static_png}, 'key':'test-0', 'animated':False, 'size':(20, 20), 'width':20, 'height':20, 'x_hot':{hotspot[0]}, 'y_hot':{hotspot[1]} }}"
    )


def test_animated_Bitmap_repr(animated_png, hotspot) -> None:
    """Testing Bitmap class ``__repr__`` datamethod for **animated png**."""
    bmp = Bitmap(animated_png, hotspot)
    assert (
        bmp.__repr__()
        == f"{{ 'grouped_png':{animated_png}, 'key':'test', 'animated':True, 'size':(20, 20), 'width':20, 'height':20, 'x_hot':{hotspot[0]}, 'y_hot':{hotspot[1]} }}"
    )


def test_static_Bitmap_context_manager(static_png, hotspot) -> None:
    """Testing Bitmap class contextmanagment datamethod for **static png**."""
    with Bitmap(static_png, hotspot) as bmp:
        with pytest.raises(AttributeError):
            assert bmp.grouped_png
        assert bmp.png == static_png
        assert bmp.animated is False
        assert bmp.height == 20
        assert bmp.width == 20
        assert bmp.compress == 0
        assert bmp.key == "test-0"
        assert bmp.x_hot == hotspot[0]
        assert bmp.y_hot == hotspot[1]


def test_animated_Bitmap_context_manager(animated_png, hotspot) -> None:
    """Testing Bitmap class contextmanagment datamethod for **animated png**."""
    with Bitmap(animated_png, hotspot) as bmp:
        with pytest.raises(AttributeError):
            assert bmp.png
        assert bmp.grouped_png == animated_png
        assert bmp.animated is True
        assert bmp.height == 20
        assert bmp.width == 20
        assert bmp.compress == 0
        assert bmp.key == "test"
        assert bmp.x_hot == hotspot[0]
        assert bmp.y_hot == hotspot[1]


def test_Bitmap_png_must_had_equal_width_and_height_exception(
    image_dir, hotspot
) -> None:
    """Testing Bitmap class ``ValueError`` (Image width and height not same) \
    exception for **static png**.
    """
    png = create_test_image(image_dir, 1, size=(2, 3))
    with pytest.raises(ValueError):
        assert Bitmap(png, hotspot)


def test_animated_Bitmap_all_png_size_must_be_equal_exception(
    image_dir, hotspot
) -> None:
    """Testing Bitmap class ``ValueError`` (Image width and height not same) \
    exception for **animated png**.
    """
    png = create_test_image(image_dir, 2, size=(2, 2))
    png.extend(create_test_image(image_dir, 1, size=(3, 6)))
    png.extend(create_test_image(image_dir, 1, size=(3, 3)))

    with pytest.raises(ValueError):
        assert Bitmap(png, hotspot)


def test_invalid_animated_Bitmap_name_exception(image_dir, hotspot) -> None:
    """Testing Bitmap class ``ValueError`` (Invalid image name) \
    exception for **animated png**.
    """
    png = []
    images = create_test_image(image_dir, 3, size=(5, 5))

    for idx, p in enumerate(images):
        target = p.with_name(f"notvalidframe{idx}.png")
        p.rename(target)
        png.append(target)

    with pytest.raises(ValueError):
        assert Bitmap(png, hotspot)


def test_animated_Bitmap_group_had_same_key_exception(image_dir, hotspot) -> None:
    """Testing Bitmap class ``ValueError`` (Invalid image key) \
    exception for **animated png**.
    """
    png = []
    images = create_test_image(image_dir, 3, size=(5, 5))

    for idx, p in enumerate(images):
        target = p.with_name(f"{str(randint(9999,453334))}-{idx}.png")
        p.rename(target)
        png.append(target)

    with pytest.raises(ValueError):
        assert Bitmap(png, hotspot)


#
# Bitmap public method
#


def test_static_Bitmap_resize_without_save(static_png) -> None:
    """Testing Bitmap ``resize`` method without ``save`` flag for static png."""
    new_size = (10, 10)
    bmp = Bitmap(static_png, (10, 10))
    assert bmp.x_hot == 10
    assert bmp.y_hot == 10
    return_image = bmp.resize(size=new_size, save=False)
    assert return_image is not None
    assert bmp.x_hot == 10
    assert bmp.y_hot == 10

    assert isinstance(return_image, Image.Image)
    assert return_image.size == new_size


def test_animated_Bitmap_resize_without_save(animated_png) -> None:
    """Testing Bitmap ``resize`` method without ``save`` flag for animated png."""
    new_size = (10, 10)
    bmp = Bitmap(animated_png, (10, 10))
    assert bmp.x_hot == 10
    assert bmp.y_hot == 10
    return_images = bmp.resize(size=new_size, save=False)
    assert return_images is not None
    assert isinstance(return_images, list)
    assert bmp.x_hot == 10
    assert bmp.y_hot == 10
    for image in return_images:
        assert image.size == new_size


def test_static_Bitmap_resize_with_save(static_png) -> None:
    """Testing Bitmap ``resize`` method with ``save`` flag for static png."""
    new_size = (10, 10)
    bmp = Bitmap(static_png, (10, 10))
    assert bmp.x_hot == 10
    assert bmp.y_hot == 10
    is_return = bmp.resize(size=new_size, save=True)
    assert is_return is None
    assert bmp.x_hot == 5
    assert bmp.y_hot == 5
    with Image.open(static_png) as i:
        assert i.size == new_size


def test_animated_Bitmap_resize_with_save(animated_png) -> None:
    """Testing Bitmap ``resize`` method with ``save`` flag for animated png."""
    new_size = (10, 10)
    bmp = Bitmap(animated_png, (10, 10))
    assert bmp.x_hot == 10
    assert bmp.y_hot == 10
    is_return = bmp.resize(size=new_size, save=True)
    assert is_return is None
    assert bmp.x_hot == 5
    assert bmp.y_hot == 5
    for frame in animated_png:
        with Image.open(frame) as i:
            assert i.size == new_size


def test_static_Bitmap_reproduce_with_save(static_png) -> None:
    """Testing Bitmap ``reproduce`` method with ``save`` flag for static png."""
    bmp = Bitmap(static_png, (10, 10))
    return_value = bmp.reproduce(
        size=(10, 10), canvas_size=(10, 10), position="center", save=True
    )
    assert return_value is None
    assert bmp.size == (10, 10)
    assert bmp.x_hot == 5
    assert bmp.y_hot == 5
    with Image.open(static_png) as i:
        assert i.size == (10, 10)


def test_static_Bitmap_reproduce_without_save(static_png) -> None:
    """Testing Bitmap ``reproduce`` method without ``save`` flag for static png."""
    bmp = Bitmap(static_png, (10, 10))
    return_value = bmp.reproduce(
        size=(10, 10), canvas_size=(10, 10), position="center", save=False
    )
    assert return_value is not None
    assert isinstance(return_value, list) is False
    assert isinstance(return_value, Image.Image)
    assert return_value.size == (10, 10)

    assert bmp.size == (20, 20)
    assert bmp.x_hot == 10
    assert bmp.y_hot == 10


def test_animated_Bitmap_reproduce_with_save(animated_png) -> None:
    """Testing Bitmap ``reproduce`` method with ``save`` flag for animated png."""
    bmp = Bitmap(animated_png, (10, 10))
    return_value = bmp.reproduce(
        size=(10, 10), canvas_size=(10, 10), position="center", save=True
    )
    assert return_value is None
    assert bmp.size == (10, 10)
    assert bmp.x_hot == 5
    assert bmp.y_hot == 5
    for frame in animated_png:
        with Image.open(frame) as i:
            assert i.size == (10, 10)


def test_animated_Bitmap_reproduce_without_save(animated_png) -> None:
    """Testing Bitmap ``reproduce`` method without ``save`` flag for animated png."""
    bmp = Bitmap(animated_png, (10, 10))
    return_value = bmp.reproduce(
        size=(10, 10), canvas_size=(10, 10), position="center", save=False
    )
    assert return_value is not None
    assert isinstance(return_value, list)
    assert bmp.size == (20, 20)
    assert bmp.x_hot == 10
    assert bmp.y_hot == 10

    for frame in return_value:
        assert frame.size == (10, 10)


def test_static_Bitmap_rename(static_png: Path, hotspot) -> None:
    """Testing Bitmap ``rename`` method with static png."""
    bmp = Bitmap(static_png, hotspot)
    assert bmp.key == "test-0"
    assert bmp.png == static_png
    with pytest.raises(AttributeError):
        assert bmp.grouped_png

    bmp.rename("new_test")
    assert bmp.key == "new_test"
    assert bmp.png == static_png.with_name("new_test.png")
    with pytest.raises(AttributeError):
        assert bmp.grouped_png


def test_animated_Bitmap_rename(animated_png: List[Path], hotspot) -> None:
    """Testing Bitmap ``rename`` method with animated png."""
    bmp = Bitmap(animated_png, hotspot)
    assert bmp.key == "test"
    assert bmp.grouped_png == animated_png
    with pytest.raises(AttributeError):
        assert bmp.png

    bmp.rename("new_test")
    assert bmp.key == "new_test"
    for i, frame in enumerate(bmp.grouped_png):
        stem: str = animated_png[i].stem.replace("test", "new_test", 1)
        assert frame == frame.with_name(f"{stem}.png")


def test_Bitmap_copy_is_raising_not_a_directory_exception(
    static_png, hotspot, test_file
) -> None:
    """Testing Bitmap ``copy`` method ``NotADirectoryError`` exception."""
    bmp = Bitmap(static_png, hotspot)
    with pytest.raises(NotADirectoryError):
        bmp.copy(test_file)


def test_Bitmap_copy_is_not_creating_not_exists_directory(static_png, hotspot) -> None:
    """Testing Bitmap ``copy`` method creating directory is not exists."""
    bmp = Bitmap(static_png, hotspot)
    copy_dir = Path(tempfile.mkdtemp("test_copy_dir"))
    shutil.rmtree(copy_dir)
    bmp.copy(copy_dir)


def test_static_Bitmap_copy_with_path_argument(static_png, hotspot) -> None:
    """Testing Bitmap ``copy`` method with passing ``Path`` type argument for \
    static png.
    """
    bmp = Bitmap(static_png, hotspot)

    assert bmp.png == static_png
    with pytest.raises(AttributeError):
        assert bmp.grouped_png

    copy_dir = Path(tempfile.mkdtemp("test_copy_dir"))
    copy_file = copy_dir / static_png.name

    copy_bmp = bmp.copy(copy_dir)
    assert copy_file.exists()
    assert copy_bmp.png == copy_file
    with pytest.raises(AttributeError):
        assert bmp.grouped_png
    shutil.rmtree(copy_dir)


def test_animated_Bitmap_copy_with_path_argument(animated_png, hotspot) -> None:
    """Testing Bitmap ``copy`` method with passing ``Path`` type argument for \
    animated png.
    """
    bmp = Bitmap(animated_png, hotspot)

    assert bmp.grouped_png == animated_png
    with pytest.raises(AttributeError):
        assert bmp.png

    copy_dir = Path(tempfile.mkdtemp("test_copy_dir"))
    copy_files = list(map(lambda x: x.name, animated_png))
    copy_bmp = bmp.copy(copy_dir)

    for i, f in enumerate(copy_files):
        copy_file = copy_dir / f
        assert copy_file.exists()
        assert copy_bmp.grouped_png[i] == copy_file
    with pytest.raises(AttributeError):
        assert bmp.png
    shutil.rmtree(copy_dir)


def test_static_Bitmap_copy_without_path_argument(static_png, hotspot) -> None:
    """Testing Bitmap ``copy`` method without passing ``Path`` type argument for \
    static png.
    """
    bmp = Bitmap(static_png, hotspot)

    assert bmp.png == static_png
    with pytest.raises(AttributeError):
        assert bmp.grouped_png

    copy_bmp = bmp.copy()

    # Without `path` argument Bitmap.copy() is creating temporary directory or not.
    assert str(tempfile.tempdir) in str(copy_bmp.png)

    is_tmp_dir = copy_bmp.png.parent
    assert is_tmp_dir.exists()
    assert is_tmp_dir.name.__contains__(copy_bmp.key)
    assert is_tmp_dir.name.__contains__("__copy__")

    with pytest.raises(AttributeError):
        assert bmp.grouped_png


def test_animated_Bitmap_copy_without_path_argument(animated_png, hotspot) -> None:
    """Testing Bitmap ``copy`` method without passing ``Path`` type argument for \
    animated png.
    """
    bmp = Bitmap(animated_png, hotspot)

    assert bmp.grouped_png == animated_png
    with pytest.raises(AttributeError):
        assert bmp.png

    copy_bmp = bmp.copy()

    # Without `path` argument Bitmap.copy() is creating temporary directory or not.
    assert str(tempfile.tempdir) in str(copy_bmp.grouped_png[0])

    is_tmp_dir = copy_bmp.grouped_png[0].parent
    assert is_tmp_dir.exists()
    assert is_tmp_dir.name.__contains__(copy_bmp.key)
    assert is_tmp_dir.name.__contains__("__copy__")

    with pytest.raises(AttributeError):
        assert bmp.png


#
# CursorAlias Test Cases
#


def test_CursorAlias_with_static_Bitmap(
    static_bitmap: Bitmap,
) -> None:
    """Testing CursorAlias class members value with static bitmap."""
    alias = CursorAlias(static_bitmap)

    assert static_bitmap.key in alias.prefix
    assert alias.prefix in str(alias.alias_dir)
    assert str(tempfile.tempdir) in str(alias.alias_dir)
    assert alias.alias_dir.exists() is True
    assert alias.bitmap == static_bitmap

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_with_animated_Bitmap(
    animated_bitmap: Bitmap,
) -> None:
    """Testing CursorAlias class members value with animated bitmap."""
    alias = CursorAlias(animated_bitmap)

    assert animated_bitmap.key in alias.prefix
    assert alias.prefix in str(alias.alias_dir)
    assert str(tempfile.tempdir) in str(alias.alias_dir)
    assert alias.alias_dir.exists() is True
    assert alias.bitmap == animated_bitmap

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_from_bitmap(static_png, hotspot) -> None:
    """Testing CursorAlias ``from_bitmap`` method."""
    directory: Path

    with CursorAlias.from_bitmap(static_png, hotspot) as ca:
        assert isinstance(ca, CursorAlias)
        assert ca.bitmap is not None
        assert ca.alias_dir is not None
        assert ca.alias_dir.exists() is True
        assert ca.garbage_dirs == []
        directory = ca.alias_dir

    assert directory.exists() is False or list(directory.iterdir()) == []

    with CursorAlias.from_bitmap(static_png, hotspot) as ca1:
        with pytest.raises(AttributeError) as excinfo:
            assert ca1.alias_file is not None
        assert (
            str(excinfo.value) == "'CursorAlias' object has no attribute 'alias_file'"
        )
        ca1.create((10, 10))
        assert ca1.alias_file is not None


def test_static_CursorAlias_str(static_bitmap):
    """Testing CursorAlias ``__str__`` datamethod."""
    alias = CursorAlias(static_bitmap)
    assert (
        alias.__str__()
        == f"CursorAlias(bitmap={static_bitmap!s}, prefix={alias.prefix}, alias_dir={alias.alias_dir}, alias_file=None, garbage_dirs=[])"
    )
    alias.create((10, 10))
    assert (
        alias.__str__()
        == f"CursorAlias(bitmap={static_bitmap!s}, prefix={alias.prefix}, alias_dir={alias.alias_dir}, alias_file={alias.alias_file}, garbage_dirs=[])"
    )

    shutil.rmtree(alias.alias_dir)


def test_static_CursorAlias_repr(static_bitmap):
    """Testing CursorAlias ``__repr__`` datamethod."""
    alias = CursorAlias(static_bitmap)
    assert (
        alias.__repr__()
        == f"{{ 'bitmap':{static_bitmap!r}, 'prefix':{alias.prefix}, 'alias_dir':{alias.alias_dir}, 'alias_file':None, 'garbage_dirs':[] }}"
    )
    alias.create((10, 10))
    assert (
        alias.__repr__()
        == f"{{ 'bitmap':{static_bitmap!r}, 'prefix':{alias.prefix}, 'alias_dir':{alias.alias_dir}, 'alias_file':{alias.alias_file}, 'garbage_dirs':[] }}"
    )
    shutil.rmtree(alias.alias_dir)


@pytest.mark.parametrize(
    "mock_sizes",
    [
        2,
        [2],
        "test",
        ["test", "test"],
    ],
)
def test_CursorAlias_create_type_error_exception(mock_sizes, static_bitmap) -> None:
    """Testing CursorAlias create method ``TypeError`` exception."""
    alias = CursorAlias(static_bitmap)
    with pytest.raises(TypeError) as excinfo:
        assert alias.create(sizes=mock_sizes)
    assert (
        str(excinfo.value)
        == "argument 'sizes' should be Tuple[int, int] type or List[Tuple[int, int]]."
    )
    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_create_with_static_bitmap_and_single_size(
    static_bitmap, static_png
) -> None:
    """Testing CursorAlias create method with single pixel size and static bitmap."""
    alias = CursorAlias(static_bitmap)

    assert len(sorted(alias.alias_dir.iterdir())) == 0
    alias.create((10, 10), delay=999999)

    for file in alias.alias_dir.iterdir():
        if file.is_dir():
            alias_png = list(file.iterdir())[0]
            assert static_png.name == alias_png.name
            i = Image.open(alias_png)
            assert i.size == (10, 10)
            i.close()
        else:
            assert file.stem == static_bitmap.key

            with file.open("r") as f:
                assert f.readlines() == ["10 0 0 10x10/test-0.png"]

    files = [f.name for f in alias.alias_dir.glob("**/*")]
    assert sorted(files) == sorted(["10x10", "test-0.alias", "test-0.png"])

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_create_with_static_bitmap_and_multiple_size(static_png) -> None:
    """Testing CursorAlias create method with multiple pixel size and static bitmap."""
    static_bitmap = Bitmap(static_png, (9, 13))
    mock_sizes = [(10, 10), (15, 15), (16, 16)]
    alias = CursorAlias(static_bitmap)

    assert len(sorted(alias.alias_dir.iterdir())) == 0
    alias.create(mock_sizes, delay=99999)

    for file in alias.alias_dir.iterdir():
        if file.is_dir():
            alias_png = list(file.iterdir())[0]
            assert static_png.name == alias_png.name
            i = Image.open(alias_png)
            assert i.size in mock_sizes
            i.close()
        else:
            assert file.stem == static_bitmap.key

            with file.open("r") as f:
                assert f.readlines() == [
                    "10 4 6 10x10/test-0.png\n",
                    "15 7 10 15x15/test-0.png\n",
                    "16 7 10 16x16/test-0.png",
                ]

    files = [f.name for f in alias.alias_dir.glob("**/*")]
    assert sorted(files) == sorted(
        [
            "10x10",
            "15x15",
            "16x16",
            "test-0.alias",
            "test-0.png",  # Because it's generate 3 size of png in individual directory.
            "test-0.png",
            "test-0.png",
        ]
    )
    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_create_with_animated_bitmap_and_single_size(image_dir) -> None:
    """Testing CursorAlias create method with single pixel size and animated bitmap."""
    animated_png = create_test_image(image_dir, 4)
    animated_bitmap = Bitmap(animated_png, (13, 6))
    alias = CursorAlias(animated_bitmap)

    assert len(sorted(alias.alias_dir.iterdir())) == 0
    alias.create((10, 10), delay=999999)

    def as_list(frames: List[Path]) -> List[str]:
        return sorted(map(lambda x: x.stem, frames))

    for file in alias.alias_dir.iterdir():
        if file.is_dir():
            frames = list(file.iterdir())
            assert as_list(frames) == as_list(animated_png)
        else:
            assert file.stem == animated_bitmap.key

            with file.open("r") as f:
                assert f.readlines() == [
                    "10 6 3 10x10/test-0.png 999999\n",
                    "10 6 3 10x10/test-1.png 999999\n",
                    "10 6 3 10x10/test-2.png 999999\n",
                    "10 6 3 10x10/test-3.png 999999",
                ]

    files = []
    for f in alias.alias_dir.glob("**/*"):
        files.append(f.name)

    assert sorted(files) == sorted(
        ["10x10", "test-0.png", "test-1.png", "test-2.png", "test-3.png", "test.alias"]
    )

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_create_with_animated_bitmap_and_multiple_size(image_dir) -> None:
    """Testing CursorAlias create method with multiple pixel size and animated bitmap."""
    animated_png = create_test_image(image_dir, 4)
    animated_bitmap = Bitmap(animated_png, (4, 2))
    alias = CursorAlias(animated_bitmap)

    assert len(sorted(alias.alias_dir.iterdir())) == 0

    mock_sizes = [(10, 10), (15, 15), (16, 16)]
    alias.create(mock_sizes, delay=999999)

    def as_list(frames: List[Path]) -> List[str]:
        return sorted(map(lambda x: x.stem, frames))

    for file in alias.alias_dir.iterdir():
        if file.is_dir():
            frames = list(file.iterdir())
            assert as_list(frames) == as_list(animated_png)
        else:
            assert file.stem == animated_bitmap.key

            with file.open("r") as f:
                assert f.readlines() == [
                    "10 2 1 10x10/test-0.png 999999\n",
                    "10 2 1 10x10/test-1.png 999999\n",
                    "10 2 1 10x10/test-2.png 999999\n",
                    "10 2 1 10x10/test-3.png 999999\n",
                    "15 3 2 15x15/test-0.png 999999\n",
                    "15 3 2 15x15/test-1.png 999999\n",
                    "15 3 2 15x15/test-2.png 999999\n",
                    "15 3 2 15x15/test-3.png 999999\n",
                    "16 3 2 16x16/test-0.png 999999\n",
                    "16 3 2 16x16/test-1.png 999999\n",
                    "16 3 2 16x16/test-2.png 999999\n",
                    "16 3 2 16x16/test-3.png 999999",
                ]

    files = []
    for f in alias.alias_dir.glob("**/*"):
        files.append(f.name)

    assert sorted(files) == sorted(
        [
            "10x10",
            "15x15",
            "16x16",
            "test-0.png",
            "test-0.png",
            "test-0.png",
            "test-1.png",
            "test-1.png",
            "test-1.png",
            "test-2.png",
            "test-2.png",
            "test-2.png",
            "test-3.png",
            "test-3.png",
            "test-3.png",
            "test.alias",
        ]
    )

    shutil.rmtree(alias.alias_dir)


alias_not_exists_err = "Alias directory is empty or not exists."


def test_CursorAlias_check_alias(static_bitmap, animated_bitmap) -> None:
    """Testing CursorAlias ``check_alias`` method."""
    alias = CursorAlias(static_bitmap)

    with pytest.raises(FileNotFoundError) as excinfo:
        alias.check_alias()
    assert str(excinfo.value) == alias_not_exists_err

    alias.create((10, 10))
    alias.check_alias()

    animated_alias = CursorAlias(animated_bitmap)
    with pytest.raises(FileNotFoundError) as excinfo:
        animated_alias.check_alias()
    assert str(excinfo.value) == alias_not_exists_err

    animated_alias.create((10, 10))
    animated_alias.check_alias()

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_extension_excpetion(static_bitmap) -> None:
    """Testing CursorAlias extension ``FileNotFoundError``(If alias file not created) exception."""
    alias = CursorAlias(static_bitmap)
    with pytest.raises(FileNotFoundError) as excinfo:
        alias.extension()
        alias.extension(".test")

    assert str(excinfo.value) == alias_not_exists_err

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_extension(static_bitmap) -> None:
    """Testing CursorAlias ``extension`` method."""
    alias = CursorAlias(static_bitmap)
    alias.create((10, 10))
    assert alias.alias_file.suffix == ".alias"
    assert alias.extension() == ".alias"
    alias.extension(".test")
    assert alias.alias_file.suffix == ".test"
    assert alias.extension() == ".test"

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_copy_alias_not_found_exception(static_bitmap) -> None:
    """Testing CursorAlias copy method ``FileNotFoundError`` (alias file not created) exception."""
    alias = CursorAlias(static_bitmap)
    with pytest.raises(FileNotFoundError) as excinfo:
        alias.copy()
    assert str(excinfo.value) == alias_not_exists_err

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_copy_path_not_directory_exception(
    static_bitmap, test_file
) -> None:
    """Testing CursorAlias copy method ``NotADirectoryError`` (provided path is not a directory) exception."""
    alias = CursorAlias(static_bitmap)
    alias.create((10, 10))
    with pytest.raises(NotADirectoryError) as excinfo:
        alias.copy(test_file)
    assert str(excinfo.value) == f"path '{test_file.absolute()}' is not a directory"

    shutil.rmtree(alias.alias_dir)


# helper
def file_tree(alias: CursorAlias) -> List[str]:
    return sorted(map(lambda x: x.name, alias.alias_dir.glob("**/*")))


def check_alias_copy(
    original_alias: CursorAlias,
    copy_of_alias: CursorAlias,
    param_dst: Optional[str] = None,
) -> None:
    if param_dst:
        assert param_dst in str(copy_of_alias.alias_dir.absolute())
    else:
        assert str(tempfile.tempdir) in str(copy_of_alias.alias_dir.absolute())

    assert copy_of_alias.alias_dir.exists() is True
    assert copy_of_alias.alias_file.exists() is True

    assert copy_of_alias.alias_file.read_text() == original_alias.alias_file.read_text()
    assert file_tree(copy_of_alias) == file_tree(original_alias)


# tests continue...
def test_CursorAlias_copy_with_static_bitmap_without_args(static_bitmap) -> None:
    """Testing CursorAlias copy method with static bitmap without any arguments."""
    alias = CursorAlias(static_bitmap)
    alias.create((10, 10))
    copy_of_alias = alias.copy()

    check_alias_copy(alias, copy_of_alias)

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_copy_with_animated_bitmap_without_args(animated_bitmap) -> None:
    """Testing CursorAlias copy method with animated bitmap without any arguments."""
    alias = CursorAlias(animated_bitmap)
    alias.create((10, 10))
    copy_of_alias = alias.copy()

    check_alias_copy(alias, copy_of_alias)

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_copy_with_static_bitmap_with_args(animated_bitmap) -> None:
    """Testing CursorAlias copy method with static bitmap with any arguments."""
    alias = CursorAlias(animated_bitmap)
    alias.create((10, 10))
    param_dst = Path(tempfile.mkdtemp())
    copy_of_alias = alias.copy(param_dst)

    check_alias_copy(alias, copy_of_alias, param_dst=str(param_dst.absolute()))

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_copy_with_animated_bitmap_with_args(animated_bitmap) -> None:
    """Testing CursorAlias copy method with animated bitmap with any arguments."""
    alias = CursorAlias(animated_bitmap)
    alias.create((10, 10))
    param_dst = Path(tempfile.mkdtemp())
    copy_of_alias = alias.copy(param_dst)

    check_alias_copy(alias, copy_of_alias, param_dst=str(param_dst.absolute()))

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_rename_with_static_bitmap(static_bitmap) -> None:
    """Testing CursorAlias rename method with static bitmap."""
    alias = CursorAlias(static_bitmap)
    alias.create((10, 10))

    old_alias = alias
    alias.rename("test_key")

    assert alias.prefix == "test_key__alias"
    assert (
        sorted(filter(lambda x: x.is_file is True, old_alias.alias_dir.glob("*/**")))
        == []
    )

    assert file_tree(alias) == ["10x10", "test_key.alias", "test_key.png"]

    with alias.alias_file.open("r") as f:
        assert f.readlines() == ["10 0 0 10x10/test_key.png"]

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_rename_with_animated_bitmap(image_dir) -> None:
    """Testing CursorAlias rename method with animated bitmap."""
    animated_bitmap = Bitmap(create_test_image(image_dir, 4), (0, 0))
    alias = CursorAlias(animated_bitmap)
    alias.create((10, 10))

    old_alias = alias
    alias.rename("test_key")

    assert alias.prefix == "test_key__alias"
    assert (
        sorted(filter(lambda x: x.is_file is True, old_alias.alias_dir.glob("*/**")))
        == []
    )

    assert file_tree(alias) == [
        "10x10",
        "test_key-0.png",
        "test_key-1.png",
        "test_key-2.png",
        "test_key-3.png",
        "test_key.alias",
    ]

    with alias.alias_file.open("r") as f:
        assert f.readlines() == [
            "10 0 0 10x10/test_key-0.png 10\n",
            "10 0 0 10x10/test_key-1.png 10\n",
            "10 0 0 10x10/test_key-2.png 10\n",
            "10 0 0 10x10/test_key-3.png 10",
        ]

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_reproduce_exception(static_bitmap) -> None:
    """Testing CursorAlias reproduce method ``FileNotFoundError`` (If cursor alias not created) exception."""
    alias = CursorAlias(static_bitmap)

    with pytest.raises(FileNotFoundError) as excinfo:
        alias.reproduce()
    assert str(excinfo.value) == alias_not_exists_err

    shutil.rmtree(alias.alias_dir)


def test_CursorAlias_reproduce(static_png, hotspot) -> None:
    """Testing CursorAlias reproduce method with static bitmap."""
    testing_dirs: List[Path]
    with CursorAlias.from_bitmap(static_png, hotspot) as alias:
        alias.create((10, 10))

        assert alias.garbage_dirs == []
        reproduced_alias = alias.reproduce(
            size=(24, 24), canvas_size=(32, 32), delay=44
        )
        testing_dirs = alias.garbage_dirs
        assert f"{alias.prefix}__garbage_bmps__" in alias.garbage_dirs[0].name
        assert file_tree(reproduced_alias) == ["32x32", "test-0.alias", "test-0.png"]

    assert (
        sorted(filter(lambda x: x.is_file is True, testing_dirs[0].glob("*/**"))) == []
    )
