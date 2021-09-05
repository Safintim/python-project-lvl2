from gendiff.gendiff import (
    Diff,
    DELETED, ADDED, CHANGED, UNCHANGED,
    generate_diff,
    get_dict_diff,
    to_json,
)
from tests.plugins import read, get_fixture_path, get_input



# expected_data = {"nested": [], "plain": []}
plain_data = read(
    get_fixture_path('expected/plain.txt')
).rstrip().split('\n\n\n')


def test_generate_diff_json():
    file_path1 = get_input('file1_1.json')
    file_path2 = get_input('file2_1.json')
    result = generate_diff(file_path1, file_path2)
    assert result == plain_data[0]


def test_generate_diff_json_all_changed():
    file_path1 = get_input('file1_1.json')
    file_path2 = get_input('file2_2.json')
    result = generate_diff(file_path1, file_path2)
    assert result == plain_data[1]


def test_generate_diff_yaml():
    file_path1 = get_input('file1_1.yaml', format='yaml')
    file_path2 = get_input('file2_1.yml', format='yaml')
    result = generate_diff(file_path1, file_path2)
    assert result == plain_data[0]


def test_generate_diff_yaml_all_changed():
    file_path1 = get_input('file1_1.yaml', format='yaml')
    file_path2 = get_input('file2_2.yaml', format='yaml')
    result = generate_diff(file_path1, file_path2)
    assert result == plain_data[1]


def test_to_json():
    assert to_json(1) == '1'
    assert to_json('string') == 'string'
    assert to_json(None) == 'null'
    assert to_json(True) == 'true'


def test_get_dict_diff_with_empty():
    assert get_dict_diff({}, {'one': 1}) == {'one': Diff(ADDED, 1, None)}
    assert get_dict_diff({'one': 1}, {}) == {'one': Diff(DELETED, 1, None)}


def test_get_dict_diff():
    assert get_dict_diff(
        {'one': 1, 'two': 2, 'fourth': 4}, {'one': 2, 'three': 3, 'fourth': 4}
    ) == {
        'one': Diff(CHANGED, 1, 2),
        'two': Diff(DELETED, 2, None),
        'three': Diff(ADDED, 3, None),
        'fourth': Diff(UNCHANGED, 4, None),
    }
