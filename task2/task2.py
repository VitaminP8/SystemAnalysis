import csv
from collections import defaultdict
import argparse


def read_csvfile(path):
    edges = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            edges.append((row[0], row[1]))

    return edges


def build_tree(path):
    children = defaultdict(list)
    parents = defaultdict(list)

    edges = read_csvfile(path)

    for a, b in edges:
        children[a].append(b)
        parents[b].append(a)

        if a not in parents:
            parents[a] = []
        if b not in children:
            children[b] = []

    return children, parents


def find_root(parents):
    # next() возвращает первый узел графа без родителей
    root = next(node for node in parents if not parents[node])
    return root


def find_relations(children, parents):
    # словарь в котором ключ-узел, а значение-словарь
    relations = {
        node: {
            'r1': set(children[node]),
            'r2': set(parents[node]),
            'r3': set(),
            'r4': set(),
            'r5': set()
        }
        for node in parents
    }

    # вычисляем r4 и r5 (всех предков и братьев)
    root = find_root(parents)
    stack = [root]
    while stack:
        cur_node = stack.pop()
        for child in children[cur_node]:
            relations[child]['r4'].update(relations[cur_node]['r2'])
            relations[child]['r4'].update(relations[cur_node]['r4'])
            relations[child]['r5'].update(relations[cur_node]['r1'] - {child})
            stack.append(child)

    # вычисляем r3 (всех детей)
    terminal_nodes = [node for node in children if not children[node]]
    stack = terminal_nodes
    while stack:
        cur_node = stack.pop()
        for parent in parents[cur_node]:
            relations[parent]['r3'].update(relations[cur_node]['r1'])
            relations[parent]['r3'].update(relations[cur_node]['r3'])
            stack.append(parent)

    return relations


def convert_to_csv_format(relations):
    fields = ['r1', 'r2', 'r3', 'r4', 'r5']
    return '\n'.join([','.join(str(len(relations[node][f])) for f in fields) for node in sorted(relations)])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    args = parser.parse_args()
    children, parents = build_tree(args.filepath)
    relations = find_relations(children, parents)
    print(convert_to_csv_format(relations))


if __name__ == '__main__':
    main()
