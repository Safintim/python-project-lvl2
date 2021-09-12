from .common import DELETED, CHANGED, ADDED, to_plain


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
                value = to_plain(value)
                lines.append(f'Property \'{current_path}\' was added with value: {value}')
            elif status == DELETED:
                lines.append(f'Property \'{current_path}\' was removed')
            elif status == CHANGED:
                new_value = to_plain(diff.get('new_value'))
                value = to_plain(value)
                lines.append(f'Property \'{current_path}\' was updated. From {value} to {new_value}')
            else:
                if isinstance(value, dict):
                    lines.extend(iter_(value, current_path))
        return lines

    lines = iter_(tree)
    return '\n'.join(lines)
