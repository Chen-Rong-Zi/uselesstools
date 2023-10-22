# encoding=UTF-8

def is_matrix(matrix):
    return matrix[1] == 'matrix' and type(matrix) == tuple and len(matrix) == 2 

def make_matrix(*args):
    row, column = (args[0], args[0]) if len(args) == 1 else (args[0], args[1])
    rows_list = []
    for i in range(row):
        rows_list.append([int(input(f"[{i+1},{j+1}]: ")) for j in range(column)])
    return matrix(rows_list)

def matrix(*args, Type='matrix'):
    assert Type == 'matrix'
    assert len(args[0]) >= 1, "matrix must has lenth and width"
    rowLenth = len(args[0][0])
    for row in args[0]:
        assert rowLenth == len(row) and type(row) == list
    return args + ('matrix',)

def print_matrix(matrix):
    assert is_matrix(matrix), "must be a matrix"

    lenth_list = []
    for j in range(matrix_column(matrix)):
        lenth_list.append( max( [ len(str(i)) for i in columns(matrix)[j] ] ) )

    for i in rows(matrix):
        print("(", end='')
        for j in range(len(i)):
            print(str(i[j]).rjust(lenth_list[j]), end=", " if j != len(i)-1 else ')\n')

def matrix_type(matrix):
    assert is_matrix(matrix), "must be a matrix" 
    return len(matrix[0]), len(matrix[0][0])

def rows(matrix):
    assert is_matrix(matrix), "must be a matrix"
    return matrix[0]

def columns(matrix):
    assert is_matrix(matrix), "must be a matrix"
    matrix_rows = rows(matrix)      # basically the rows of matrix is matrix itself
    columns_list = []
    for column in range(matrix_column(matrix)):
        columns_list.append([ matrix_rows[i][column] for i in range(matrix_row(matrix)) ])
    return columns_list # already checked, safe array!

def matrix_row(matrix):
    assert is_matrix(matrix), "must be a matrix"
    return matrix_type(matrix)[0]

def matrix_column(matrix):
    assert is_matrix(matrix), "must be a matrix"
    return matrix_type(matrix)[1]

def copy_matrix(m):
    return matrix([copy_list(i) for i in rows(m)])

def copy_list(lst):
    """just to deep copy a list
    """
    return [i for i in lst]

def mul_matrix(m1, m2):
    assert is_matrix(m1) and is_matrix(m2)
    assert matrix_column(m1) == matrix_row(m2), "不合法的矩阵乘法"

    def multiply_helper(list1, list2):
        assert len(list1) == len(list2)
        product = 0
        for i in range(len(list1)):
            product += list1[i] * list2[i]
        return five_place(product)

    result = []
    for i in range(matrix_row(m1)):
        row_list = []
        list1 = copy_list(rows(m1)[i])                               # for the whole row
        for j in range(matrix_column(m2)):
            list2 = copy_list(columns(m2)[j])                        # for the whole column
            row_list.append(multiply_helper(list1, list2))
        result.append(row_list)
    return matrix(result)

def kth_matrix(m, k):
    assert is_matrix(m) and k != 0, 'must be a matrix and k must not be 0'
    original_rows = rows(m)
    new_rows = []
    for j in range(matrix_row(m)):
        new_rows.append([five_place(k * i) for i in original_rows[j]])
    return matrix(new_rows)

def pow_matrix(m, n):
    x = copy_matrix(m)
    for i in range(n-1):
        m = mul_matrix(m, x)
    return m

def add_matrix(m1, m2):
    """return a new matrix for the sake of mutability of list.
    """
    assert is_matrix(m1) and is_matrix(m2) and matrix_type(m1) == matrix_type(m2)
    newRows = []
    column = matrix_column(m1)
    for i in range(matrix_row(m1)):
        newRows.append([rows(m1)[i][j] + rows(m2)[i][j] for j in range(column)])
    return matrix(newRows)  # already checked, safe array!

def transfer(matr):
    assert is_matrix(matr)
    return matrix(columns(matr))

def adjoint_matrix(matr):
    assert matrix_row(matr) == matrix_column(matr), "只有方阵才有伴随矩阵"
    rows_list = []
    for i in range(matrix_row(matr)):
        row = []
        for j in range(matrix_column(matr)):
            row.append(determinant(cofactor(matr, i, j)) * pow(-1, i+j))
        rows_list.append(row)
    return transfer(matrix(rows_list))

def reverse_matrix(matr):
    return kth_matrix(adjoint_matrix(matr), 1/determinant(matr))

def cofactor(matr, row, column):
    assert is_matrix(matr), "must be a matrix"
    assert matrix_row(matr) == matrix_column(matr), "只有方阵才有代数余子式"

    row_list = []
    for i in range(matrix_row(matr)):
        if i == row: continue
        origin_rows = rows(matr)
        row_list.append([origin_rows[i][j] for j in range(matrix_column(matr)) if j != column])
    return matrix(row_list)

def determinant(matr):
    assert is_matrix(matr), "must be a matrix"
    assert matrix_row(matr) == matrix_column(matr), "只有方阵才有行列式"

    if matrix_row(matr) == 1:
        return rows(matr)[0][0]

    original_rows = rows(matr)
    if matrix_row(matr) == 2:
        return original_rows[0][0] * original_rows[1][1] - original_rows[0][1] * original_rows[1][0]

    result = 0
    for i in range(matrix_column(matr)):
        result += original_rows[0][i] * determinant(cofactor(matr, 0, i)) * pow(-1, i)
    return result

def zero_matrix(*args):
    assert len(args) >= 1, "matrix must have rows and columns"
    if len(args) == 1:
        row, column = args[0], args[0]
    else:
        row, column = args[0], args[1]
    lst = [0 for i in range(column)]
    return matrix([copy_list(lst) for i in range(row)])

def identity_matrix(n, x=1, y=1):
    zero_rows = rows(zero_matrix(n))
    for i in range(n):
        if i == x-1:
            zero_rows[i][i] = 0
            zero_rows[i][y-1] = 1
            continue
        elif i == y-1:
            zero_rows[i][i] = 0
            zero_rows[i][x-1] = 1
            continue
        else:
            zero_rows[i][i] = 1

        zero_rows[i][i] = 1
    return matrix(zero_rows)

def swap_row(matr, x, y):
    assert is_matrix(matr), "must be a matrix"
    E = identity_matrix(matrix_row(matr), x, y)
    return mul_matrix(E, matr)

def swap_column(matr, x, y):
    assert is_matrix(matr), "must be a matrix"
    tran = transfer(matr)
    E = identity_matrix(matrix_row(tran), x, y)
    return transfer(mul_matrix(E, tran))

def five_place(x):
    return int(x * 1e4) / 1e4
# test
list1 = [1, 0]
list2 = [2, 3]
list3 = [4, 5]
list4 = [2, 1]
list5 = [4, 3]
a = matrix([list1, list2, list3])
b = matrix([list4, list5])
add      = add_matrix
adjoint  = adjoint_matrix
det      = determinant
make     = make_matrix
mul      = mul_matrix
powm     = pow_matrix
p        = print_matrix
swcolumn = swap_column
swrow    = swap_row
tran     = transfer
E_matr   = identity_matrix
reverse  = reverse_matrix
kth      = kth_matrix
