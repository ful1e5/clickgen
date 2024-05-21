from _typeshed import Incomplete
from clickgen.cursors import CursorFrame as CursorFrame

MAGIC: bytes
ICO_TYPE_CUR: int
ICON_DIR: Incomplete
ICON_DIR_ENTRY: Incomplete

def to_cur(frame: CursorFrame) -> bytes: ...

SIGNATURE: bytes
ANI_TYPE: bytes
HEADER_CHUNK: bytes
LIST_CHUNK: bytes
SEQ_CHUNK: bytes
RATE_CHUNK: bytes
FRAME_TYPE: bytes
ICON_CHUNK: bytes
RIFF_HEADER: Incomplete
CHUNK_HEADER: Incomplete
ANIH_HEADER: Incomplete
UNSIGNED: Incomplete
SEQUENCE_FLAG: int
ICON_FLAG: int

def get_ani_cur_list(frames: list[CursorFrame]) -> bytes: ...
def get_ani_rate_chunk(frames: list[CursorFrame]) -> bytes: ...
def to_ani(frames: list[CursorFrame]) -> bytes: ...
def to_win(frames: list[CursorFrame]) -> tuple[str, bytes]: ...
