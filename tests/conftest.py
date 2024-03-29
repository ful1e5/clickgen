import io
from pathlib import Path
from typing import List, Tuple

import pytest
from PIL.Image import Image, open

from clickgen.cursors import CursorFrame, CursorImage


@pytest.fixture
def samples_dir() -> Path:
    return Path(__file__).parents[1] / "samples"


@pytest.fixture
def blob(samples_dir) -> bytes:
    pointer_png = samples_dir / "pngs/pointer.png"
    return pointer_png.read_bytes()


@pytest.fixture
def blobs(blob) -> List[bytes]:
    return [blob, blob]


@pytest.fixture
def dummy_blob(samples_dir) -> bytes:
    txt = samples_dir / "sample.toml"
    return txt.read_bytes()


@pytest.fixture
def dummy_blobs(dummy_blob) -> List[bytes]:
    return [dummy_blob, dummy_blob]


@pytest.fixture
def image(blob) -> Image:
    return open(io.BytesIO(blob))


@pytest.fixture
def hotspot() -> Tuple[int, int]:
    return (100, 105)


@pytest.fixture
def nominal() -> int:
    return 24


@pytest.fixture
def cursor_image(image, hotspot, nominal) -> CursorImage:
    return CursorImage(image, hotspot, nominal)


@pytest.fixture
def images(cursor_image) -> List[CursorImage]:
    return [cursor_image, cursor_image, cursor_image]


@pytest.fixture
def sizes() -> List[int]:
    return [12, 12, 24]


@pytest.fixture
def delay() -> int:
    return 5


@pytest.fixture
def cursor_frame(images, delay) -> CursorFrame:
    return CursorFrame(images, delay)


@pytest.fixture
def theme_name() -> str:
    return "test"


@pytest.fixture
def comment() -> str:
    return "comment"


@pytest.fixture
def website() -> str:
    return "https://www.example.com"


@pytest.fixture(scope="session")
def x11_tmp_dir(tmpdir_factory) -> Path:
    return Path(tmpdir_factory.mktemp("x11_tmp"))


@pytest.fixture(scope="session")
def win_cur_tmp_dir(tmpdir_factory) -> Path:
    p = Path(tmpdir_factory.mktemp("x11_tmp"))
    for f in ["test1", "test2", "test3"]:
        cfile = p / f"{f}.cur"
        cfile.write_text("test win cursors")
    return p


@pytest.fixture(scope="session")
def win_ani_tmp_dir(tmpdir_factory) -> Path:
    p = Path(tmpdir_factory.mktemp("x11_tmp"))
    for f in ["test1", "test2", "test3"]:
        cfile = p / f"{f}.ani"
        cfile.write_text("test win cursors")
    return p
