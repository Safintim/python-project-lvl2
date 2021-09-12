from gendiff.formatters import ADDED, REMOVED, UPDATED, UNCHANGED
from gendiff.formatters.plain import (
    get_current_path,
    add_line_to,
    REMOVED_PATTERN,
    ADDED_PATTERN,
    UPDATED_PATTERN
)


def test_get_current_path():
    assert get_current_path('', 'common') == 'common'
    assert get_current_path('common', 'group') == 'common.group'
    assert get_current_path('common.setting', 'rk') == 'common.setting.rk'


def test_add_line_to():
    lines = []
    path, value, new_value = 'root', 'Root value', 'new value'

    assert add_line_to(
        lines,
        status=REMOVED,
        path='root',
        value='Root value',
        new_value=None,
    )
    assert REMOVED_PATTERN.format(path, value)

    assert add_line_to(
        lines,
        status=ADDED,
        path='root',
        value='Root value',
        new_value=None,
    )
    assert ADDED_PATTERN.format(path, value)

    assert add_line_to(
        lines,
        status=UPDATED,
        path='root',
        value='Root value',
        new_value=new_value,
    )
    assert UPDATED_PATTERN.format(path, value, new_value)

    assert add_line_to(
        lines,
        status=UNCHANGED,
        path='root',
        value='Root value',
        new_value=new_value,
    ) is False
