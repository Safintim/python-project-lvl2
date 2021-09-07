import argparse

from gendiff.formatters import stylish, plain
from gendiff.gendiff import generate_diff


def main():
    parser = argparse.ArgumentParser(
        description='Generate diff'
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f', '--format',
        default='stylish',
        help='set format of output',
    )
    namespace = parser.parse_args()
    print(
        generate_diff(
            file_path1=namespace.first_file,
            file_path2=namespace.second_file,
            format=namespace.forma,
        )
    )


if __name__ == '__main__':
    main()
