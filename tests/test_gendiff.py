import os

from gendiff.gendiff import generate_diff

import pytest


@pytest.fixture
def files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path1 = os.path.join(current_dir, 'fixtures', 'file1.json')
    file_path2 = os.path.join(current_dir, 'fixtures', 'file2.json')
    return file_path1, file_path2


def test_generate_diff(files):
    file_path1, file_path2 = files
    expected = '''{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}'''

    result = generate_diff(file_path1, file_path2)
    print(result)
    assert result == expected
