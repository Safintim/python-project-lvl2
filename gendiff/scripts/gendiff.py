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

    if namespace.format == 'stylish':
        format_ = stylish
    else:
        format_ = plain

    print(
        generate_diff(
            namespace.first_file,
            namespace.second_file,
            format_,
        )
    )


if __name__ == '__main__':
    main()
