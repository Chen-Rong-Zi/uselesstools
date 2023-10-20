# encoding=UTF-8

def is_matrix(matrix):
    assert type(matrix) == tuple
    return matrix[1] == 'matrix'

def matrix(*args):
    assert args[1] == 'matrix'
    rowLenth = len(args[0][0])
    for row in args[0]:
        assert rowLenth == len(row) and type(row) == list

    return args

def print_matrix(matrix):
    assert is_matrix(matrix)
    for i in matrix[0]:
        for j in i:
            print(j, end="\t")
        print()

def matrix_type(matrix):
    assert is_matrix(matrix)
    return len(matrix[0]), len(matrix[0][0])

def matrix_row(matrix):
    assert is_matrix(matrix)
    return matrix_type(mul_matrix)[0]

def matrix_column(matrix):
    assert is_matrix(matrix)
    return matrix_type(mul_matrix)[1]

def mul_matrix(matrix1, matrix2):
    assert is_matrix(matrix1) and is_matrix(matrix2)
    assert matrix_column(matrix1) == matrix_row(matrix2)


def add_matrix(matrix1, matrix2):
    """return a new matrix for the sake of mutability of list.
    """
    assert is_matrix(matrix1) and is_matrix(matrix2) and matrix_type(matrix1) == matrix_type(matrix2)
    newRows = []
    for i in range(len(matrix1[0])):
        newRows.append([matrix1[0][i][j] + matrix2[0][i][j] for j in range(len(matrix1[0][0]))])
    return matrix([i for i in newRows], 'matrix')

# test
list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
list2 = [2 * i for i in list1]
a = matrix([list1, list2], 'matrix')

