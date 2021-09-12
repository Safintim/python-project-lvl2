from gendiff.formatters import ADDED, REMOVED, UNCHANGED, UPDATED, to_plain
from gendiff.formatters.plain import (
    ADDED_PATTERN,
    REMOVED_PATTERN,
    UPDATED_PATTERN,
    add_line_to,
    get_current_path,
)


def test_get_current_path():
    assert get_current_path("", "common") == "common"
    assert get_current_path("common", "group") == "common.group"
    assert get_current_path("common.setting", "rk") == "common.setting.rk"


def test_add_line_to():
    lines = []
    path, value, new_value = "root", "Root value", "new value"

    assert add_line_to(
        lines,
        status=REMOVED,
        path="root",
        value="Root value",
        new_value=None,
    )
    assert lines[0] == REMOVED_PATTERN.format(path, to_plain(value))

    assert add_line_to(
        lines,
        status=ADDED,
        path="root",
        value="Root value",
        new_value=None,
    )
    assert lines[1] == ADDED_PATTERN.format(path, to_plain(value))

    assert add_line_to(
        lines,
        status=UPDATED,
        path="root",
        value="Root value",
        new_value=new_value,
    )
    print(lines[2])
    assert lines[2] == UPDATED_PATTERN.format(
        path, to_plain(value), to_plain(new_value)
    )

    assert (
        add_line_to(
            lines,
            status=UNCHANGED,
            path="root",
            value="Root value",
            new_value=new_value,
        )
        is False
    )
    assert len(lines) == 3
