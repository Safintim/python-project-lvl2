from gendiff import formatters
from gendiff.parser import parse_file


DELETED = 'deleted'
ADDED = 'added'
CHANGED = 'changed'
UNCHANGED = 'unchanged'


def mark_as_deleted(dict_, key, value):
    if isinstance(value, dict):
        value = get_dict_diff(value, value)
    dict_[key] = {'status': formatters.DELETED, 'value': value}


def mark_as_added(dict_, key, value):
    if isinstance(value, dict):
        value = get_dict_diff(value, value)
    dict_[key] = {'status': formatters.ADDED, 'value': value}


def mark_as_unchanged_for_complex_value(dict_, key, value1, value2):
    dict_[key] = {
        'status': formatters.UNCHANGED, 'value': get_dict_diff(value1, value2)
    }


def mark_as_unchanged(dict_, key, value):
    dict_[key] = {'status': formatters.UNCHANGED, 'value': value}


def mark_as_changed(dict_, key, value1, value2):
    if isinstance(value1, dict):
        value1 = get_dict_diff(value1, value1)
    if isinstance(value2, dict):
        value2 = get_dict_diff(value2, value2)
    dict_[key] = {
        'status': formatters.CHANGED, 'value': value1, 'new_value': value2
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


def generate_diff(file_path1, file_path2, formatter=formatters.stylish):
    json1 = parse_file(file_path1)
    json2 = parse_file(file_path2)

    diff = get_dict_diff(json1, json2)
    return formatter(diff)
