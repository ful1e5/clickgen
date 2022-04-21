from typing import List


def str_to_list(s: str) -> List[str]:
    str_l = s.split(",")
    results = [s.strip() for s in str_l]
    return list(filter(None, results))
