import itertools


DELETED = 'deleted'
ADDED = 'added'
CHANGED = 'changed'
UNCHANGED = 'unchanged'
DIFF_TYPE_CHAR = {
    DELETED: '-',
    ADDED: '+',
    CHANGED: '-',
    UNCHANGED: ' ',
}


def plain():
    pass


def to_json(value):
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    return str(value)


def stylish(tree, replacer=' ', spaces_count=2):
    base_indent = 2

    def iter_(current_tree, depth):
        nested_indent_count = depth + spaces_count
        nested_indent = replacer * nested_indent_count
        current_indent = replacer * depth
        lines = []
        for key, diff in sorted(current_tree.items()):
            status_char = DIFF_TYPE_CHAR.get(diff.get('status'))
            val = diff.get('value')

            if isinstance(val, dict):
                val = iter_(val, nested_indent_count + base_indent)
            else:
                val = to_json(val)

            lines.append(f'{nested_indent}{status_char} {key}: {val}')

            if diff.get('status') == CHANGED:
                status_char = DIFF_TYPE_CHAR.get(ADDED)
                val = to_json(diff.get('new_value'))
                lines.append(f'{nested_indent}{status_char} {key}: {val}')

        result = itertools.chain('{', lines, [current_indent + '}'])
        return '\n'.join(result)
    return iter_(tree, 0)
