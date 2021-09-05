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
            diff[key] = Diff(DELETED, d1[key], None)
        elif key not in d1:
            diff[key] = Diff(ADDED, d2[key], None)
        elif d1[key] == d2[key]:
            diff[key] = Diff(UNCHANGED, d1[key], None)
        else:
            diff[key] = Diff(CHANGED, d1[key], d2[key])
    return diff


def to_json(value):
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, (str, int)):
        return str(value)


def format_diff(diff, replacer=' ', spaces_count=2):
    ident = replacer * spaces_count

    lines = []
    for key, diff in sorted(diff.items()):
        type_ = DIFF_TYPE_CHAR[diff.type]
        val = to_json(diff.val1)
        lines.append(f'{ident}{type_} {key}: {val}')
        if diff.type == CHANGED:
            type_ = DIFF_TYPE_CHAR[ADDED]
            val = to_json(diff.val2)
            lines.append(f'{ident}{type_} {key}: {val}')

    result = itertools.chain('{', lines, '}')
    return '\n'.join(result)


def generate_diff(file_path1, file_path2):
    json1 = parse_file(file_path1)
    json2 = parse_file(file_path2)

    diff = get_dict_diff(json1, json2)
    return format_diff(diff)
