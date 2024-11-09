import numpy as np
import pandas as pd


def calculate_entropy(probabilities):
    total_entropy = -np.sum(probabilities * np.log2(probabilities, where=(probabilities > 0)))
    return total_entropy


def read_csvfile(filename):
    data = pd.read_csv(filename, index_col=0)
    purchases = data.values
    return purchases


def main():
    purchases = read_csvfile('example.csv')
    total_purchases = purchases.sum()

    # Вероятности для A (возрастные группы) и B (товары)
    P_A = purchases.sum(axis=1) / total_purchases
    P_B = purchases.sum(axis=0) / total_purchases
    P_AB = purchases / total_purchases

    # Вычисление энтропии H(AB)
    H_AB = calculate_entropy(P_AB)

    # Вычисление энтропии H(A)
    H_A = calculate_entropy(P_A)

    # Вычисление энтропии H(B)
    H_B = calculate_entropy(P_B)

    # Условная энтропия H(B|A) и информация I(A, B)
    Ha_B = H_AB - H_A
    I_AB = H_B - Ha_B

    # Округление до второго знака
    results = [round(float(val), 2) for val in [H_AB, H_A, H_B, Ha_B, I_AB]]
    return results


if __name__ == "__main__":
    print(main())
