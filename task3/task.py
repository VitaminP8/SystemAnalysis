import csv
import math
import argparse


def read_csvfile(path):
    matrix = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            matrix.append(list(map(int, row)))
    return matrix


def calculate_entropy(matrix):
    entropy = 0.0

    for row in matrix:
        row_sum = sum(row)
        if row_sum == 0:
            continue
        for value in row:
            if value > 0:
                p_ij = value / row_sum
                entropy += p_ij * math.log2(p_ij)

    return -entropy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    args = parser.parse_args()

    matrix = read_csvfile(args.filepath)
    entropy = calculate_entropy(matrix)
    print(round(entropy, 1))


if __name__ == '__main__':
    main()
