import itertools


DELETED = 'removed'
ADDED = 'added'
CHANGED = 'updated'
UNCHANGED = 'unchanged'
DIFF_TYPE_CHAR = {
    DELETED: '-',
    ADDED: '+',
    CHANGED: '-',
    UNCHANGED: ' ',
}


def get_current_path(path, new_key):
    if not path:
        return new_key
    return f'{path}.{new_key}'


def plain(tree):
    def iter_(current_tree, path=''):
        lines = []
        for key, diff in sorted(current_tree.items()):
            status = diff.get('status')
            value = diff.get('value')
            current_path = get_current_path(path, key)
            if status == ADDED:
                if isinstance(value, dict):
                    value = '[complex value]'
                else:
                    value = to_plain(value)
                lines.append(f'Property \'{current_path}\' was added with value: {value}')
            elif status == DELETED:
                lines.append(f'Property \'{current_path}\' was removed')
            elif status == CHANGED:
                new_value = diff.get('new_value')
                if isinstance(value, dict):
                    value = '[complex value]'
                else:
                    value = to_plain(value)
                if isinstance(new_value, dict):
                    new_value = '[complex value]'
                else:
                    new_value = to_plain(new_value)
                lines.append(f'Property \'{current_path}\' was updated. From {value} to {new_value}')
            else:
                if isinstance(value, dict):
                    lines.extend(iter_(value, current_path))
        return lines

    lines = iter_(tree)
    return '\n'.join(lines)


def to_plain(value):
    if isinstance(value, str):
        return f'\'{value}\''
    return to_json(value)


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
