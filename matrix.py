# encoding=UTF-8

def clean_product(x):
    if x == 0:
        return 0
    if x > 0:
        decimal = x % 1
        return int(x) if (decimal) <= 1e-6 else int(x)+1 if (1-decimal) <= 1e-6 else x
    else:
        x = abs(x)
        decimal = x % 1
        return -int(x) if (decimal) <= 1e-6 else -(int(x)+1) if (1-decimal) <= 1e-6 else -x

def copy_list(lst):
    """just to deep copy a list
    """
    new_list = []
    for i in lst:
        if type(i) == list:
            i = copy_list(i)
        new_list.append(i)
    return new_list


class MATRIX():
    def __init__(self, *args, cls="matrix"):
        assert cls == 'matrix'
        assert len(args[0]) >= 1, "matrix must has lenth and width"
        rowLenth = len(args[0][0])
        for row in args[0]:
            assert rowLenth == len(row) and type(row) == list

        self.row     = len(args[0])
        self.column  = len(args[0][0])
        self.rows    = copy_list(args[0])
        self.columns = [[self.get(r, c) for r in range(self.row)] for c in range(self.column)]
        self.type    = [self.row, self.column]
        self.cls     = 'matrix'

    def get(self, x, y):
            return self.rows[x][y]

    def p(self, end=''):
        lenth_list = []
        for j in range(self.column):
            lenth_list.append( max( [ len(str(i)) for i in self.columns[j] ]) )

        for i in range(self.row):
            print("(", end='')
            for j in range(self.column):
                print(str(self.get(i, j)).rjust(lenth_list[j]), end='')
                print(', ' if j != self.column-1 else ')\n', end='')
        print(end, end='')

    def kth(self, k):
        new_matr = [ [clean_product(k * i) for i in j] for j in self.rows]
        return MATRIX(new_matr)


    def pow(self, n):
        if n == 0:
            return identity_matrix(self.row)
        x = copy_matrix(self)
        for i in range(n-1):
            matr = mul_matrix(self, x)
        return matr


    def add(self, m2):
        """return a new matrix for the sake of mutability of list.
        """
        assert is_matrix(m2) and self.type == m2.type
        new_matr = [ [self.get(i, j) + m2.get(i, j) for j in range(self.column)] for i in range(self.row)]
        return MATRIX(new_matr)  # already checked, safe array!

    def tran(self):
        return MATRIX(self.columns)

    def cofactor(self, row, column):
        assert self.row == self.column, "只有方阵才有代数余子式"
        new_matr = [ [self.get(i, j) for j in range(self.column) if j != column] for i in range(self.row) if i != row]
        return MATRIX(new_matr)

    def adjoint_matrix(self):
        assert self.row == self.column, "只有方阵才有伴随矩阵"
        rows_list = [[ self.cofactor(i, j).determinant() * pow(-1, i+j) for j in range(self.column) ] for i in range(self.row)]
        return MATRIX(rows_list).tran()

    def reverse_matrix(self):
        assert self.determinant() != 0, "只有方阵才有代数余子式"
        return self.adjoint_matrix().kth( 1/self.determinant())

    def determinant(self):
        assert self.row == self.column, "只有方阵才有行列式"
        if self.row == 1:
            return self.get(0, 0)

        return sum([ self.get(0, i) * self.cofactor(0, i).determinant() * pow(-1, i) for i in range(self.column) ])

    def swap_row(self, x, y, oper=False):
        E = identity_matrix(self.row, x, y)
        return (mul_matrix(E, self), E) if oper else mul_matrix(E, self)

    def swap_column(self, x, y, oper=False):
        transfered = self.tran()
        E = identity_matrix(transfered.row, x, y)
        return (mul_matrix(E, transfered).tran(), E) if oper else mul_matrix(E, transfered).tran()

    def add_row(self, k, x, y, oper=False):
        E_rows = []
        for i in range(self.row):
            if i == y:
                E_rows.append(make_E_row(self.row, k, x))
                continue
            E_rows.append(make_E_row(self.row, 0, i))
        E = MATRIX(E_rows).add(identity_matrix(self.row))
        return (mul_matrix(E, self), E) if oper else mul_matrix(E, self)

    def rref(self, display=False):
        matr = copy_matrix(self)
        min_semi = min(matr.row, matr.column)
        if display: matr.p(end="\n")

        for column in range(min_semi):
            for row in range(matr.row):
                if column == row:continue

                if matr.get(column, column) == 0:
                    k = None
                    for k in range(column+1, matr.row):
                        matr = matr.swap_row(column, k)
                        if matr.get(column, column) != 0: break
                    if  k is None: continue

                matr = matr.add_row(-(matr.get(row, column)/matr.get(column, column)), column, row)
                if display: matr.p(end='' if (column == min_semi-1 and row == matr.row-2) else '\n')

            for column in range(min_semi):
                if matr.get(column, column) != 0 or matr.get(column, column) != 1:
                    matr = matr.add_row((1/matr.get(column, column)) - 1, column, column)
        return matr

class AUGMENT(MATRIX):
    def __init__(self, m1, m2):

        self.cls     = 'augment'
        self.x       = copy_matrix(m1)
        self.y       = copy_matrix(m2)

        self.row     = self.x.row
        self.column  = self.x.column + self.y.column
        self.rows    = [self.x.rows[i] + self.y.rows[i] for i in range(self.x.row)]
        self.columns = self.x.columns + self.y.columns
        self.type    = [self.row, self.column]
        self.cls     = 'augment'

    def p(self, end=''):
        lenth_list = []
        for j in range(self.column):
            lenth_list.append( max( [ len(str(i)) for i in self.columns[j] ]) )

        for i in range(self.row):
            print("(", end='')
            for j in range(self.column):
                seperator = ', ' if j != self.x.column-1 else ' ⏐ '
                print(str(self.get(i, j)).rjust(lenth_list[j]), end='')
                print(seperator if j != self.column-1 else ')\n', end='')
        print(end, end='')

    def rref(self, display=False):
        matr     = self
        min_semi = min(matr.x.row, matr.x.column)
        if display: matr.p(end="\n")

        for column in range(min_semi):
            for row in range(matr.x.row):
                if column == row:continue

                if matr.get(column, column) == 0:
                    k = None
                    for k in range(column+1, matr.x.row):
                        matr = matr.swap_row(column, k)
                        if matr.get(column, column) != 0: break
                    if  k is None: continue

                matr = AUGMENT(matr.x.add_row(-(matr.get(row, column)/matr.get(column, column)), column, row), matr.y.add_row(-(matr.get(row, column)/matr.get(column, column)), column, row))
                if display: matr.p(end='' if (column == min_semi-1 and row == matr.x.row-2) else '\n')

            for column in range(min_semi):
                if matr.get(column, column) != 0 or matr.get(column, column) != 1:
                    matr = AUGMENT(matr.x.add_row((1/matr.get(column, column)) - 1, column, column), matr.y.add_row((1/matr.get(column, column)) - 1, column, column))
        return matr


def make_E_row(n, k, b):
    return [(0 if i != b else k) for i in range(n)]


def identity_matrix(n, x=0, y=0):
    rows_list = []
    for i in range(n):
        if i == x:
            rows_list.append(make_E_row(n, 1, y))
        elif i == y:
            rows_list.append(make_E_row(n, 1, x))
        else:
            rows_list.append(make_E_row(n, 1, i))
    return MATRIX(rows_list)


def mul_matrix(m1, m2):
    assert is_matrix(m1) and is_matrix(m2), "only matrx can be applied mul_matrix to!"
    assert m1.column == m2.row, "不合法的矩阵乘法"

    def list_mul(list1, list2):
        assert len(list1) == len(list2)
        product = sum([list1[i] * list2[i] for i in range(len(list1)) ])
        return clean_product(product)

    return MATRIX([ [list_mul(r, c) for c in m2.columns] for r in m1.rows])

def is_matrix(matr):
    return hasattr(matr, 'cls')

def is_augment(matr):
    return hasattr(matr, 'cls') and (matr.cls == "Augment")


def make_matrix(*args):
    row, column = (args[0], args[0]) if len(args) == 1 else (args[0], args[1])
    rows_list = []
    try:
        for i in range(row):
            rows_list.append([int(input(f"[{i+1},{j+1}]: ")) for j in range(column)])
    except KeyboardInterrupt:
        return print('\nexit, try again!')
    return MATRIX(rows_list)

def copy_matrix(matr):
    return MATRIX([copy_list(i) for i in matr.rows])



def zero_matrix(*args):
    assert len(args) >= 1, "matrix must have rows and columns"
    row, column = (args[0], args[0]) if len(args) == 1 else (args[0], args[1])
    lst = [0 for i in range(column)]
    return MATRIX([copy_list(lst) for i in range(row)])

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
row11 = [0, 0, 1, 1]
row12 = [1, 2, 0, -1]
row13 = [1, -1, 1, 1]
row14 = [2, 1, 1, 0]
a = MATRIX([row6, row7, row8]).tran()
b = MATRIX([row9, row10])
c = MATRIX([row1, row2, row3])
d = MATRIX([row4, row5])
c = AUGMENT(a, b)
