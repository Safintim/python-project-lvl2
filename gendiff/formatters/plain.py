from .common import REMOVED, UPDATED, ADDED, to_plain


ADDED_PATTERN = 'Property \'{}\' was added with value: {}'
REMOVED_PATTERN = 'Property \'{}\' was removed'
UPDATED_PATTERN = 'Property \'{}\' was updated. From {} to {}'


PATTERN_BY_STATUS = {
    ADDED: ADDED_PATTERN,
    REMOVED: REMOVED_PATTERN,
    UPDATED: UPDATED_PATTERN,
}


def get_current_path(path, new_key):
    if not path:
        return new_key
    return f'{path}.{new_key}'


def add_line_to(lines, *, status, path, value, new_value):
    pattern = PATTERN_BY_STATUS.get(status)
    if pattern is None:
        return False
    value_plain = to_plain(value)
    new_value_plain = to_plain(new_value)
    lines.append(pattern.format(path, value_plain, new_value_plain))
    return True


def plain(tree):
    def iter_(current_tree, path=''):
        lines = []
        for key, diff in sorted(current_tree.items()):
            status = diff.get('status')
            value = diff.get('value')
            new_value = diff.get('new_value')
            current_path = get_current_path(path, key)
            is_added = add_line_to(
                lines,
                status=status,
                path=current_path,
                value=value,
                new_value=new_value
            )
            if not is_added and isinstance(value, dict):
                lines.extend(iter_(value, current_path))

        return lines

    lines = iter_(tree)
    return '\n'.join(lines)
