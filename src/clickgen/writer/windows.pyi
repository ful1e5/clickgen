from typing import Any, List, Tuple
from wxcursors.cursors import CursorFrame as CursorFrame

MAGIC: bytes
ICO_TYPE_CUR: int
ICON_DIR: Any
ICON_DIR_ENTRY: Any

def to_cur(frame: CursorFrame) -> bytes: ...

SIGNATURE: bytes
ANI_TYPE: bytes
HEADER_CHUNK: bytes
LIST_CHUNK: bytes
SEQ_CHUNK: bytes
RATE_CHUNK: bytes
FRAME_TYPE: bytes
ICON_CHUNK: bytes
RIFF_HEADER: Any
CHUNK_HEADER: Any
ANIH_HEADER: Any
UNSIGNED: Any
SEQUENCE_FLAG: int
ICON_FLAG: int

def get_ani_cur_list(frames: List[CursorFrame]) -> bytes: ...
def get_ani_rate_chunk(frames: List[CursorFrame]) -> bytes: ...
def to_ani(frames: List[CursorFrame]) -> bytes: ...
def to_win(frames: List[CursorFrame]) -> Tuple[str, bytes]: ...
