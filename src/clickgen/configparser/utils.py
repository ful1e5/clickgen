from typing import List


def str_to_list(s: str) -> List[str]:
    str_l = s.split(",")
    return [s.strip() for s in str_l]
