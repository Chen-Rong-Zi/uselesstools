# encoding=UTF-8

def is_matrix(matrix):
    assert type(matrix) == tuple
    return matrix[1] == 'matrix'

def matrix(*args, Type='matrix'):
    assert Type == 'matrix'
    rowLenth = len(args[0][0])
    for row in args[0]:
        assert rowLenth == len(row) and type(row) == list
    return args + ('matrix',)

def print_matrix(matrix):
    assert is_matrix(matrix)
    for i in matrix[0]:
        for j in i:
            print(j, end="\t")
        print()

def matrix_type(matrix):
    assert is_matrix(matrix) 
    return len(matrix[0]), len(matrix[0][0])
def rows(matrix):
    assert is_matrix(matrix)
    return matrix[0]

def columns(matrix):
    assert is_matrix(matrix)
    matrix_rows = rows(matrix)      # basically the rows of matrix is matrix itself
    columns_list = []
    for column in range(len(matrix_rows[0])):
        columns_list += [[matrix_rows[i][column] for i in range(len(matrix_rows))]]
    return columns_list

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

def mul_matrix(m1, m2):
    assert is_matrix(m1) and is_matrix(m2)
    assert matrix_column(m1) == matrix_row(m2)

    def multiply_helper(list1, list2):
        assert len(list1) == len(list2)
        product = 0
        for i in range(len(list1)):
            product += list1[i] * list2[i]
        return product

    result = []
    for i in range(matrix_row(m1)):
        row_list = []
        list1 = copy_list(rows(m1)[i])                               # for the whole row
        for j in range(matrix_column(m2)):
            list2 = copy_list(columns(m2)[j])                        # for the whole column
            row_list.append(multiply_helper(list1, list2))
        result += [row_list]
    return matrix(result)

def add_matrix(m1, m2):
    """return a new matrix for the sake of mutability of list.
    """
    assert is_matrix(m1) and is_matrix(m2) and matrix_type(m1) == matrix_type(m2)
    newRows = []
    for i in range(len(m1[0])):
        newRows.append([m1[0][i][j] + m2[0][i][j] for j in range(len(m1[0][0]))])
    return matrix([i for i in newRows])

def transfer(matr):
    assert is_matrix(matr)
    return matrix(columns(matr))
# test
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = [1, 3, 4]
a = matrix([list1, list2])
b = matrix([[7, 8], [9, 10], [11, 12]])

