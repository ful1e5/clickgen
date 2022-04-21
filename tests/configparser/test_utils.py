import pytest

from clickgen.configparser.utils import str_to_list


@pytest.mark.parametrize(
    "test_input",
    [
        "a,b,c",
        "a,b,   c",
        "a, b,c ",
        "a,b,c ,",
        "a,,,b,c ,",
    ],
)
def test_str_to_list(test_input):
    assert str_to_list(test_input) == ["a", "b", "c"]
