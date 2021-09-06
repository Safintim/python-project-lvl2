import collections
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

Diff = collections.namedtuple('Diff', ('type', 'val1', 'val2'))


def get_dict_diff(d1, d2):
    keys = d1.keys() | d2.keys()
    diff = {}
    for key in keys:
        if key not in d2:
            diff[key] = {'status': DELETED, 'value': d1[key]}
        elif key not in d1:
            diff[key] = {'status': ADDED, 'value': d2[key]}
        elif isinstance(d1[key], dict) and isinstance(d2[key], dict):
            diff[key] = {
                'status': UNCHANGED,
                'value': get_dict_diff(d1[key], d2[key]),
            }
        elif d1[key] == d2[key]:
            diff[key] = {'status': UNCHANGED, 'value': d1[key]}
        else:
            diff[key] = {
                'status': CHANGED,
                'value': d1[key],
                'new_value': d2[key],
            }
    return diff


def to_json(value):
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    return str(value)


def format_diff(diff, replacer=' ', spaces_count=2):
    ident = replacer * spaces_count

    lines = []
    for key, diff in sorted(diff.items()):
        type_ = DIFF_TYPE_CHAR[diff['status']]
        if not isinstance(diff['value'], dict):
            val = to_json(diff['value'])
            lines.append(f'{ident}{type_} {key}: {val}')
            if diff['status'] == CHANGED:
                type_ = DIFF_TYPE_CHAR[ADDED]
                val = to_json(diff['new_value'])
                lines.append(f'{ident}{type_} {key}: {val}')

    result = itertools.chain('{', lines, '}')
    return '\n'.join(result)


def generate_diff(file_path1, file_path2):
    json1 = parse_file(file_path1)
    json2 = parse_file(file_path2)

    diff = get_dict_diff(json1, json2)
    return format_diff(diff)
