from gendiff.formatters import to_json, to_plain


def test_to_json():
    assert to_json(1) == '1'
    assert to_json('string') == 'string'
    assert to_json(None) == 'null'
    assert to_json(True) == 'true'
    assert to_json([1, 2, 3, 4]) == '[1, 2, 3, 4]'


def test_to_plain():
    assert to_plain(1) == '1'
    assert to_plain('string') == "'string'"
    assert to_plain(None) == 'null'
    assert to_plain(True) == 'true'
    assert to_plain([1, 2, 3, 4]) == '[1, 2, 3, 4]'
    assert to_plain({'key': 'value'}) == '[complex value]'
