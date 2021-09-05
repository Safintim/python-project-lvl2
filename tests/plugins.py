import os


def get_fixture_path(file_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_path)


def get_input(file_path, format='json'):
    return get_fixture_path(os.path.join(f'inputs/{format}/', file_path))


def read(file_path):
    with open(file_path, 'r') as f:
        result = f.read()
    return result
