import itertools

from .common import ADDED, CHAR_BY_DIFF, UPDATED, to_json

PATTERN_LINE = "{}{} {}: {}"


def add_line_to(lines, *, indent, status, key, value):
    status_char = CHAR_BY_DIFF.get(status)
    val = to_json(value)
    lines.append(PATTERN_LINE.format(indent, status_char, key, val))


def stylish(tree, replacer=" ", spaces_count=2):
    base_indent = 2

    def iter_(current_tree, depth):
        nested_indent_count = depth + spaces_count
        nested_indent = replacer * nested_indent_count
        current_indent = replacer * depth
        lines = []
        for key, diff in sorted(current_tree.items()):
            status = diff.get("status")
            val = diff.get("value")
            new_value = diff.get("new_value")

            if isinstance(val, dict):
                val = iter_(val, nested_indent_count + base_indent)

            if isinstance(new_value, dict):
                new_value = iter_(new_value, nested_indent_count + base_indent)

            add_line_to(
                lines,
                indent=nested_indent,
                status=status,
                key=key,
                value=val,
            )

            if status == UPDATED:
                add_line_to(
                    lines,
                    indent=nested_indent,
                    status=ADDED,
                    key=key,
                    value=new_value,
                )

        result = itertools.chain("{", lines, [current_indent + "}"])
        return "\n".join(result)

    return iter_(tree, 0)
