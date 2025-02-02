# test_cron.py
import pytest
from parser.cron_parser import parse_cron, format_output


TEST_CASES = [
    (
        "*/15 0 1,15 * 1-5 /usr/bin/find",
        {
            'minute': [0, 15, 30, 45],
            'hour': [0],
            'day of month': [1, 15],
            'month': list(range(1, 13)),
            'day of week': [1, 2, 3, 4, 5],
            'command': '/usr/bin/find'
        }
    ),
    (
        "0 9 * * 0 /backup.sh",
        {
            'minute': [0],
            'hour': [9],
            'day of month': list(range(1, 32)),
            'month': list(range(1, 13)),
            'day of week': [0],
            'command': '/backup.sh'
        }
    )
]

@pytest.mark.parametrize("input_str,expected", TEST_CASES)
def test_parser(input_str, expected):
    result = parse_cron(input_str)
    for field in expected:
        assert result[field] == expected[field]

def test_formatting():
    result = parse_cron("*/5 0 * * 3 /task")
    output = format_output(result)
    assert "minute        0 5 10 15 20 25 30 35 40 45 50 55" in output
    assert "command       /task" in output

def test_invalid_input():
    with pytest.raises(ValueError):
        parse_cron("*/15 0 1,15 * /usr/bin/find")  # Missing day of week
    with pytest.raises(ValueError):
        parse_cron("*/15 0 1,15 * 1-5")  # Missing command