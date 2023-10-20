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

def matrix_rows(matrix):
    assert is_matrix(matrix)
    return matrix[0]

def matrix_row(matrix):
    assert is_matrix(matrix)
    return matrix_type(matrix)[0]

def matrix_column(matrix):
    assert is_matrix(matrix)
    return matrix_type(matrix)[1]

def copy_list(lst):
    """just to deep copy a list
    """
    return [i for i in lst]

def multiply_helper(list1, list2):
    assert len(list1) == len(list2)
    product = 0
    for i in range(len(list1)):
        product += list1[i] * list2[i]
    return product

def mul_matrix(m1, m2):
    assert is_matrix(m1) and is_matrix(m2)
    assert matrix_column(m1) == matrix_row(m2)

    result = []
    for i in range(matrix_row(m1)):
        row_list = []
        list1 = copy_list(matrix_rows(m1)[i])
        for j in range(matrix_column(m2)):
            list2 = [matrix_rows(m2)[k][j] for k in range(matrix_row(m2))]
#             print(f"list1 = {list1}, list2 = {list2}, multiply_helper(list1, list2) == {multiply_helper(list1, list2)}")
            row_list.append(multiply_helper(list1, list2))
        result += [row_list]
    return matrix(result, 'matrix')

def add_matrix(m1, m2):
    """return a new matrix for the sake of mutability of list.
    """
    assert is_matrix(m1) and is_matrix(m2) and matrix_type(m1) == matrix_type(m2)
    newRows = []
    for i in range(len(m1[0])):
        newRows.append([m1[0][i][j] + m2[0][i][j] for j in range(len(m1[0][0]))])
    return matrix([i for i in newRows], 'matrix')

# test
list1 = [1, 1, 1]
list2 = [1, 3, 2]
list3 = [1, 3, 4]
a = matrix([list1, list2, list3], 'matrix')
b = matrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]], 'matrix')

