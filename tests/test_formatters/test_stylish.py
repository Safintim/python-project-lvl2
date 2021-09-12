from gendiff.formatters import ADDED, CHAR_BY_DIFF, to_json
from gendiff.formatters.stylish import add_line_to, PATTERN_LINE


def test_add_line_to():
    lines = []

    params = {
        'indent': ' ',
        'status': ADDED,
        'key': 'key',
        'value': 'val'
    }
    add_line_to(lines, **params)
    expected = PATTERN_LINE.format(
        params['indent'],
        CHAR_BY_DIFF.get(ADDED),
        params['key'],
        to_json(params['value']),
    )
    assert lines[0] == expected
