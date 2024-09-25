import argparse
import csv


def task(path, row, col):
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        matrix = list(reader)
        return matrix[row-1][col-1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    parser.add_argument('-r', '--row', type=int)
    parser.add_argument('-c', '--column', type=int)
    args = parser.parse_args()
    answer = task(args.filepath, args.row, args.column)
    print(answer)


if __name__ == '__main__':
    main()