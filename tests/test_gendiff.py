from gendiff.formatters import DELETED, ADDED, CHANGED, UNCHANGED
from gendiff.gendiff import (
    generate_diff,
    create_diff_tree,
)
from tests.plugins import read, get_fixture_path, get_input


# expected_data = {"nested": [], "plain": []}
stylish_flatten_data = read(
    get_fixture_path('expected/stylish_flatten.txt')
).rstrip().split('\n\n\n')
stylish_nested_data = read(
    get_fixture_path('expected/stylish_nested.txt')
).rstrip().split('\n\n\n')
plain_nested_data = read(
    get_fixture_path('expected/plain_nested.txt')
).rstrip().split('\n\n\n')


def test_generate_diff_stylish_json_flatten():
    file_path1 = get_input('file1_1.json')
    file_path2 = get_input('file2_1.json')
    result = generate_diff(file_path1, file_path2)
    assert result == stylish_flatten_data[0]


def test_generate_diff_stylish_json_flatten_all_changed():
    file_path1 = get_input('file1_1.json')
    file_path2 = get_input('file2_2.json')
    result = generate_diff(file_path1, file_path2)
    assert result == stylish_flatten_data[1]


def test_generate_diff_stylish_json_nested():
    file_path1 = get_input('nested1.json')
    file_path2 = get_input('nested2.json')
    result = generate_diff(file_path1, file_path2, format_name='stylish')
    assert result == stylish_nested_data[0]


def test_generate_diff_plain_json_nested():
    file_path1 = get_input('nested1.json')
    file_path2 = get_input('nested2.json')
    result = generate_diff(file_path1, file_path2, format_name='plain')
    assert result == plain_nested_data[0]


def test_generate_diff_stylish_yaml_flatten():
    file_path1 = get_input('file1_1.yaml', format='yaml')
    file_path2 = get_input('file2_1.yml', format='yaml')
    result = generate_diff(file_path1, file_path2)
    assert result == stylish_flatten_data[0]


def test_generate_diff_stylish_yaml_flatten_all_changed():
    file_path1 = get_input('file1_1.yaml', format='yaml')
    file_path2 = get_input('file2_2.yaml', format='yaml')
    result = generate_diff(file_path1, file_path2)
    assert result == stylish_flatten_data[1]


def test_generate_diff_stylish_yaml_nested():
    file_path1 = get_input('nested1.yaml', format='yaml')
    file_path2 = get_input('nested2.yaml', format='yaml')
    result = generate_diff(file_path1, file_path2, format_name='stylish')
    assert result == stylish_nested_data[0]


def test_get_dict_diff_with_empty():
    assert create_diff_tree({}, {'one': 1}) == {
        'one': {'status': ADDED, 'value': 1, 'new_value': None}
    }
    assert create_diff_tree({'one': 1}, {}) == {
        'one': {'status': DELETED, 'value': 1, 'new_value': None}
    }


def test_get_dict_diff():
    assert create_diff_tree(
        {'one': 1, 'two': 2, 'fourth': 4},
        {'one': 2, 'three': 3, 'fourth': 4}
    ) == {
        'one': {'status': CHANGED, 'value': 1, 'new_value': 2},
        'two': {'status': DELETED, 'value': 2, 'new_value': None},
        'three': {'status': ADDED, 'value': 3, 'new_value': None},
        'fourth': {'status': UNCHANGED, 'value': 4, 'new_value': None},
    }


def test_get_dict_diff_nested():
    nested1 = {
        'common': {
            'setting1': 'Value 1',
        },
        'group1': {
            'baz': 'bas',
            'nest': {
                'key': 'value',
                'key2': 'value'
            }
        }
    }
    nested2 = {
        'common': {
            'setting1': 'Value 100',
        },
        'group1': {
            'nest': {
                'key': 'value',
                'key2': None,
                'key3': '1'
            },
            'meta': 10
        },
        'group2': {
            'sdf': 123
        }
    }
    expected = {
        'common': {
            'status': UNCHANGED,
            'value': {
                'setting1': {
                    'status': CHANGED,
                    'value': 'Value 1',
                    'new_value': 'Value 100'
                }
            },
            'new_value': None
        },
        'group1': {
            'status': UNCHANGED,
            'value': {
                'baz': {
                    'status': DELETED,
                    'value': 'bas',
                    'new_value': None,
                },
                'nest': {
                    'status': UNCHANGED,
                    'value': {
                        'key': {
                            'status': UNCHANGED,
                            'value': 'value',
                            'new_value': None
                        },
                        'key2': {
                            'status': CHANGED,
                            'value': 'value',
                            'new_value': None,

                        },
                        'key3': {
                            'status': ADDED,
                            'value': '1',
                            'new_value': None
                        }
                    },
                    'new_value': None
                },
                'meta': {
                    'status': ADDED,
                    'value': 10,
                    'new_value': None
                }
            },
            'new_value': None
        },
        'group2': {
            'status': ADDED,
            'value': {
                'sdf': {
                    'status': UNCHANGED,
                    'value': 123,
                    'new_value': None
                }
            },
            'new_value': None
        }
    }
    assert create_diff_tree(nested1, nested2) == expected
