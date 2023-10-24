# encoding=UTF-8

def is_augment(matr):
    return (hasattr(matr, '__call__') and (matr("cls") == "Augment") or matr('cls') == 'A')

def is_matrix(matr):
    return (hasattr(matr, '__call__') and matr("cls") == 'matrix') or (hasattr(matr, '__call__') and (matr("cls") == "Augment") or matr('cls') == 'A')

def make_matrix(*args):
    row, column = (args[0], args[0]) if len(args) == 1 else (args[0], args[1])
    rows_list = []
    for i in range(row):
        rows_list.append([int(input(f"[{i+1},{j+1}]: ")) for j in range(column)])
    return matrix(rows_list)

def matrix(*args, cls='matrix'):
    if cls == "matrix":
        assert cls == 'matrix'
        assert len(args[0]) >= 1, "matrix must has lenth and width"
        rowLenth = len(args[0][0])
        for row in args[0]:
            assert rowLenth == len(row) and type(row) == list

        def matrix_function(x, y='noparameter', cls=cls):
            if x == 'cls':
                return cls
            if x == 'row':
                return len(args[0])
            if x == 'column':
                return len(args[0][0])
            if y == 'noparameter':
                return args[0][x]
            assert x >= 0 and y >= 0, "x, y must at least 0"
            return args[0][x][y]

        return matrix_function

    if cls == "Augment" or cls == 'A':
        assert len(args) == 2 and is_matrix(args[0]) and is_matrix(args[1]), "only matrix can be added up to argument matrix"
        row_list = []
        for i in range(args[0]('row')):
            row_list.append(args[0](i) + args[1](i))
        augment = matrix(row_list)

        def augment_function(x, y='noparameter', cls=cls):
            if x == 'a':
                return args[0]
            if x == 'b':
                return args[1]
            if x == 'cls':
                return cls
            if x == 'row':
                return args[0]('row')
            if x == 'column':
                return args[0]('column')
            if y == 'noparameter':
                return augment(x)
            assert x >= 0 and y >= 0, "x, y must at least 0"
            return augment(x, y)
        return augment_function

def print_matrix(matr, end=''):
    assert is_matrix(matr) or is_augment(matr), "must be a matrix"

    lenth_list = []
    for j in range(len(matr(0))):
        lenth_list.append( max( [ len(str(i)) for i in [matr(k, j) for k in range(matr('row'))] ] ) )

    for i in rows(matr):
        print("(", end='')
        for j in range(len(i)):
            print(str(i[j]).rjust(lenth_list[j]), end=(" ⏐ " if j == matr('row') else ", ") if j != len(i)-1 else ')\n')
    print(end, end='')

def matrix_type(matrix):
    assert is_matrix(matrix), "must be a matrix" 
    return matrix('row'), matrix('column')

def matrix_row(matr):
    assert is_matrix(matr), "must be a matrix"
    return matr('row')

def matrix_column(matr):
    assert is_matrix(matr), "must be a matrix"
    return matr('column')

def rows(matr):
    assert is_matrix(matr) or is_augment(matr), "must be a matrix"
    rows_list = []
    for i in range(matr('row')):
        rows_list.append(copy_list(matr(i)))
    return rows_list

def columns(matr):
    assert is_matrix(matr) or is_augment(matr), "must be a matrix"
    columns_list = []
    for column in range(matr('column')):
        columns_list.append([ matr(i, column) for i in range(matr('row')) ])
    return columns_list # already checked, safe array!

def copy_matrix(m):
    return matrix([copy_list(i) for i in rows(m)])

def copy_list(lst):
    """just to deep copy a list
    """
    return [i for i in lst]

def mul_matrix(m1, m2):
    assert is_matrix(m1) and is_matrix(m2)
    assert m1('column') == m2('row'), "不合法的矩阵乘法"

    def multiply_helper(list1, list2):
        assert len(list1) == len(list2)
        product = 0
        for i in range(len(list1)):
            product += list1[i] * list2[i]
        return clean_product(product)

    result = []
    for i in range(m1('row')):
        row_list = []
        list1 = m1(i)                               # for the whole row
        for j in range(m2('column')):
            list2 = columns(m2)[j]                        # for the whole column
            row_list.append(multiply_helper(list1, list2))
        result.append(row_list)
    return matrix(result)

def kth_matrix(matr, k):
    assert is_matrix(matr) and k != 0, 'must be a matrix and k must not be 0'
    original_rows = rows(matr)
    new_rows = []
    for j in range(matr('row')):
        new_rows.append([clean_product(k * i) for i in matr(j)])
    return matrix(new_rows)

def pow_matrix(matr, n):
    x = copy_matrix(matr)
    for i in range(n-1):
        matr = mul_matrix(matr, x)
    return matr

def add_matrix(m1, m2):
    """return a new matrix for the sake of mutability of list.
    """
    assert is_matrix(m1) and is_matrix(m2) and matrix_type(m1) == matrix_type(m2)
    new_rows = []
    for i in range(m1('row')):
        new_rows.append([m1(i, j) + m2(i, j) for j in range(m1('column'))])
    return matrix(new_rows)  # already checked, safe array!

def transfer(matr):
    assert is_matrix(matr)
    return matrix(columns(matr))

def cofactor(matr, row, column):
    assert is_matrix(matr), "must be a matrix"
    assert matrix_row(matr) == matrix_column(matr), "只有方阵才有代数余子式"

    row_list = []
    for i in range(matr('row')):
        if i == row: continue
        row_list.append([matr(i, j) for j in range(matr('column')) if j != column])
    return matrix(row_list)

def adjoint_matrix(matr):
    assert matrix_row(matr) == matrix_column(matr), "只有方阵才有伴随矩阵"
    rows_list = []
    for i in range(matr('row')):
        new_rows = []
        for j in range(matr('column')):
            row.append(determinant(cofactor(matr, i, j)) * pow(-1, i+j))
        rows_list.append(row)
    return transfer(matrix(rows_list))

def reverse_matrix(matr):
    return kth_matrix(adjoint_matrix(matr), 1/determinant(matr))

def determinant(matr):
    assert is_matrix(matr), "must be a matrix"
    assert matrix_row(matr) == matrix_column(matr), "只有方阵才有行列式"

    if matrix_row(matr) == 1:
        return matr(0, 0)

    if matrix_row(matr) == 2:
        return matr(0, 0) * matr(1, 1) - matr(0, 1) * matr(1, 0)

    result = 0
    for i in range(matrix_column(matr)):
        result += matr(0, i) * determinant(cofactor(matr, 0, i)) * pow(-1, i)
    return result

def zero_matrix(*args):
    assert len(args) >= 1, "matrix must have rows and columns"
    if len(args) == 1:
        row, column = args[0], args[0]
    else:
        row, column = args[0], args[1]
    lst = [0 for i in range(column)]
    return matrix([copy_list(lst) for i in range(row)])

def make_E_row(n, k, b):
    return [(0 if i != b else k) for i in range(n)]

def identity_matrix(n, x=0, y=0):
    rows_list = []
    for i in range(n):
        if i == x:
            rows_list.append(make_E_row(n, 1, y))
        elif i == y:
            rows_list.append(make_E_row(n, 1, x))
        else :
            rows_list.append(make_E_row(n, 1, i))
    return matrix(rows_list)

def swap_row(matr, x, y):
    assert is_matrix(matr), "must be a matrix"
    E = identity_matrix(matrix_row(matr), x, y)
    return mul_matrix(E, matr), E

def swap_column(matr, x, y):
    assert is_matrix(matr), "must be a matrix"
    tran = transfer(matr)
    E = identity_matrix(matrix_row(tran), x, y)
    return transfer(mul_matrix(E, tran)), E

def clean_product(x):
    if x == 0:
        return 0
    if x > 0:
        decimal = x % 1
        return int(x) if (decimal) <= 1e-6 else int(x)+1 if (1-decimal) <= 1e-6 else x
    else:
        decimal = (-x) % 1
        return -int(x) if (decimal) <= 1e-6 else -(int(x)+1) if (1-decimal) <= 1e-6 else -x

def add_row(matr, k, x, y):
    E_rows = []
    for i in range(matr('row')):
        if i == y:
            E_rows.append(make_E_row(matr('row'), k, x))
            continue
        E_rows.append(make_E_row(matr('row'), 0, i))
    E = add_matrix(matrix(E_rows), identity_matrix(matr('row')))
    return mul_matrix(E, matr), E

def rref(matr, display=False, operation=False):
    assert is_matrix(matr), "must be a matrix to be applied rref to!"

    if is_augment(matr):
        a, b = matr('a'), matr('b')
        a, oper_list = rref(a, opers=True)
        for i in oper_list:
            b = mul_matrix(i, b)
        return matrix(a, b, cls="Augment")

    oper_list = []
    lenth = min(matr('row'), matr('column'))
    if display:
        print_matrix(matr, end='\n')

    for i in range(lenth):
        for j in range(matr('row')):
            if i == j:continue

            elif matr(i, i) == 0:
                for k in range(i+1, matr("row")):
                    matr, oper = (swap_row(matr, i, k))
                    oper_list.append(oper)
                    if matr(i, i) != 0: break
                if  k is None or (k == matr("row") - 1): continue

            matr, oper = (add_row(matr, -(matr(j, i)/matr(i, i)), i, j))
            oper_list.append(oper)
            if display:
                print_matrix(matr, '\n')

        for i in range(lenth):
            if matr(i, i) != 0:
                matr, oper = (add_row(matr, (1/matr(i, i)) - 1, i, i))
                oper_list.append(oper)
    return matr if not operation else (matr, oper_list)



# test
row1 = [1, 0]
row2 = [2, 3]
row3 = [4, 5]
row4 = [2, 1]
row5 = [4, 3]
row6 = [1, 0]
row7 = [2, 3]
row8 = [4, 5]
row9 = [2, 1]
row10 = [4, 3]
f = lambda matr: lambda x, y: matr(x-1, y-1)
a = matrix([row6, row7, row8])
b = matrix([row9, row10])
c = matrix([row1, row2, row3])
d = matrix([row4, row5])
add      = add_matrix
adjoint  = adjoint_matrix
det      = determinant
make     = make_matrix
mul      = mul_matrix
powm     = pow_matrix
p        = print_matrix
swcolumn = lambda matr, x, y: swap_column(matr, x+1, y+1)
swrow    = lambda matr, x, y: swap_row(matr, x+1, y+1)
tran     = transfer
E_matr   = identity_matrix
reverse  = reverse_matrix
kth      = kth_matrix

a = tran(a)
d = matrix(a, b, cls="Augment")
