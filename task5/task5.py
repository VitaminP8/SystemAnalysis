import json
import numpy as np


def get_matrix(filepath: str):
    with open(filepath, 'r') as file:
        clusters = json.load(file)

    clusters = [c if isinstance(c, list) else [c] for c in clusters]
    n = sum(len(cluster) for cluster in clusters)

    matrix = [[1] * n for _ in range(n)]

    # print(clusters)

    worse = []
    for cluster in clusters:
        for worse_element in worse:
            for element in cluster:
                matrix[element - 1][worse_element - 1] = 0
                # print(element-1, worse_element-1)
        for element in cluster:
            worse.append(int(element))

    return np.array(matrix)


def find_clusters(matrix, est1, est2):
    conflict_core = []

    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if matrix[i][j] == 0 and matrix[j][i] == 0:  # Если оба элемента противоречат друг другу
                conflict_pair = sorted([i + 1, j + 1])
                if conflict_pair not in conflict_core:
                    conflict_core.append(conflict_pair)

    final_result = [pair[0] if len(pair) == 1 else pair for pair in conflict_core]
    return str(final_result)

    # cluster_dict = {}
    # rows, cols = len(matrix), len(matrix[0])
    # processed_rows = set()
    #
    # for i in range(rows):
    #     if i + 1 in processed_rows:
    #         continue
    #
    #     current_cluster = [i + 1]
    #     cluster_dict[i + 1] = current_cluster
    #
    #     for j in range(i + 1, cols):
    #         if matrix[i][j] == 0:
    #             current_cluster.append(j + 1)
    #             processed_rows.add(j + 1)
    #
    # merged_clusters = []
    # for key in cluster_dict:
    #     if not merged_clusters:
    #         merged_clusters.append(cluster_dict[key])
    #         continue
    #
    #     for idx, cluster in enumerate(merged_clusters):
    #         sum_est1_cluster = np.sum(est1[cluster[0] - 1])
    #         sum_est2_cluster = np.sum(est2[cluster[0] - 1])
    #         sum_est1_key = np.sum(est1[key - 1])
    #         sum_est2_key = np.sum(est2[key - 1])
    #
    #         if sum_est1_cluster == sum_est1_key and sum_est2_cluster == sum_est2_key:
    #             merged_clusters[idx].extend(cluster_dict[key])
    #             break
    #         elif sum_est1_cluster < sum_est1_key or sum_est2_cluster < sum_est2_key:
    #             merged_clusters = merged_clusters[:idx] + cluster_dict[key] + merged_clusters[idx:]
    #             break
    #     else:
    #         merged_clusters.append(cluster_dict[key])
    #
    # final_clusters = [cluster[0] if len(cluster) == 1 else cluster for cluster in merged_clusters]
    # return str(final_clusters)


def main(file_path1, file_path2):
    matrix1 = get_matrix(file_path1)
    matrix2 = get_matrix(file_path2)

    # Создаем пересечение и объединение матриц
    matrix_and = np.multiply(matrix1, matrix2)
    matrix_and_t = np.multiply(np.transpose(matrix1), np.transpose(matrix2))
    matrix_or = np.maximum(matrix_and, matrix_and_t)

    clusters = find_clusters(matrix_or, matrix1, matrix2)
    return clusters


if __name__ == '__main__':
    print(main("example1.json", "example2.json"))