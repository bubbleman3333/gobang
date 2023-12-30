import numpy as np

# 例として、3x3の行列を作成
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# 主対角線よりも上に位置する斜めの要素を取得（k=1）
above_diagonal_elements = np.diag(matrix, k=1)

# 主対角線よりも上に位置する斜めの要素に対応するインデックスを取得（k=1）
above_diagonal_indices = np.diag_indices_from(matrix, k=1)

# 結果を表示
print("Above Diagonal Elements:")
print(above_diagonal_elements)
print("\nAbove Diagonal Indices:")
print(above_diagonal_indices)
