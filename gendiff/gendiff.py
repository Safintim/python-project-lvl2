import itertools

from gendiff.parser import parse_file

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


def mark_as_deleted(dict_, key, value):
    if isinstance(value, dict):
        value = get_dict_diff(value, value)
    dict_[key] = {'status': DELETED, 'value': value}


def mark_as_added(dict_, key, value):
    if isinstance(value, dict):
        value = get_dict_diff(value, value)
    dict_[key] = {'status': ADDED, 'value': value}


def mark_as_unchanged_for_complex_value(dict_, key, value1, value2):
    dict_[key] = {
        'status': UNCHANGED,
        'value': get_dict_diff(value1, value2),
    }


def mark_as_unchanged(dict_, key, value):
    dict_[key] = {'status': UNCHANGED, 'value': value}


def mark_as_changed(dict_, key, value1, value2):
    if isinstance(value1, dict):
        value1 = get_dict_diff(value1, value1)
    if isinstance(value2, dict):
        value2 = get_dict_diff(value2, value2)
    dict_[key] = {
        'status': CHANGED,
        'value': value1,
        'new_value': value2,
    }


def get_dict_diff(first_dict, second_dict):
    keys = first_dict.keys() | second_dict.keys()
    diff = {}
    for key in keys:
        value1 = first_dict.get(key)
        value2 = second_dict.get(key)
        if key not in second_dict:
            mark_as_deleted(diff, key, value1)
        elif key not in first_dict:
            mark_as_added(diff, key, value2)
        elif isinstance(value1, dict) and isinstance(value2, dict):
            mark_as_unchanged_for_complex_value(diff, key, value1, value2)
        elif value1 == value2:
            mark_as_unchanged(diff, key, value1)
        else:
            mark_as_changed(diff, key, value1, value2)
    return diff


def to_json(value):
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    return str(value)


def stylish(tree, replacer=' ', spaces_count=2):
    def iter_(current_tree, depth):
        nested_ident_count = depth + spaces_count
        nested_ident = replacer * nested_ident_count
        current_ident = replacer * depth
        lines = []
        for key, diff in sorted(current_tree.items()):
            status_char = DIFF_TYPE_CHAR[diff.get('status')]
            val = diff.get('value')

            if isinstance(val, dict):
                val = iter_(val, nested_ident_count + 2)
            else:
                val = to_json(val)

            lines.append(f'{nested_ident}{status_char} {key}: {val}')

            if diff.get('status') == CHANGED:
                status_char = DIFF_TYPE_CHAR[ADDED]
                val = to_json(diff.get('new_value'))
                lines.append(f'{nested_ident}{status_char} {key}: {val}')

        result = itertools.chain('{', lines, [current_ident + '}'])
        return '\n'.join(result)
    return iter_(tree, 0)


def generate_diff(file_path1, file_path2, formatter=stylish):
    json1 = parse_file(file_path1)
    json2 = parse_file(file_path2)

    diff = get_dict_diff(json1, json2)
    return formatter(diff)
