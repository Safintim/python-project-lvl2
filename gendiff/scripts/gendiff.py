import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Generate diff'
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', default='json', help='set format of output')
    print(parser.parse_args())


if __name__ == '__main__':
    main()
