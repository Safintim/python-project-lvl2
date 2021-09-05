from gendiff.gendiff import parse_file
from tests.plugins import get_input


def test_parse_file():
    file_path_yaml = get_input('simple.yaml', format='yaml')
    assert parse_file(file_path_yaml) == {'a': 1, 'b': 2}

    file_path_yml = get_input('simple.yml', format='yaml')
    assert parse_file(file_path_yml) == {'a': 1, 'b': 2}

    file_path_json = get_input('simple.json')
    assert parse_file(file_path_json) == {'a': 1, 'b': 2}
