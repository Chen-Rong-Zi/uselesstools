# encoding=UTF-8
from math import gcd
from fractions import Fraction
del Fraction.__repr__
Fraction.__repr__ = Fraction.__str__

class Matrix:
    def __init__(self, *args, cls="matrix"):
        assert cls == 'matrix'
        assert len(args[0]) >= 1, "matrix must has lenth and width"
        rowLenth = len(args[0][0])
        for row in args[0]:
            assert rowLenth == len(row) and type(row) == list

        self.row     = len(args[0])
        self.column  = len(args[0][0])
        self.rows    = copy_list(args[0])
        self.columns = [ [self.get(r, c) for r in range(self.row)] for c in range(self.column) ]
        self.type    = [self.row, self.column]
        self.cls     = 'matrix'

    def __repr__(self, end=''):
        matrix_string = ''
        lenth_list = []
        for j in range(self.column):
            lenth_list.append( max( [ len(str(i)) for i in self.columns[j] ]) )

        for i in range(self.row):
            matrix_string += "("
            for j in range(self.column):
                max_lenth_in_a_column = lenth_list[j]
                value                = self.get(i, j)
                seperator             = ', '
                trailing              = ')\n' if i != self.row - 1 else ')'
                matrix_string += str(value).rjust(max_lenth_in_a_column)       # numbers in matrix
                matrix_string += seperator if j != self.column-1 else trailing  # prefix and sufix in matrix
        matrix_string += end
        return matrix_string

    def __str__(self):
        return self.__repr__()

    def __add__(self, m2):
        """return a new matrix for the sake of mutability of list.
        """
        assert is_matrix(m2) and self.type == m2.type
        new_matr = [ [self.get(i, j) + m2.get(i, j) for j in range(self.column)] for i in range(self.row)]
        return Matrix(new_matr)  # already checked, safe array!

    def __mul__(self, m2):
        assert is_matrix(self) and is_matrix(m2), "only matrx can be applied mul_matrix to!"
        assert self.column == m2.row, "不合法的矩阵乘法"

        def list_mul(list1, list2):
            assert len(list1) == len(list2)
            product = sum([(list1[i] * list2[i]).limit_denominator() for i in range(len(list1)) ])
            return product

        return Matrix([ [list_mul(r, c) for c in m2.columns] for r in self.rows])

    def __pow__(self, n):
        assert self.row == self.column, "invalid matrix pow!"
        if n == 0:
            return identity_matrix(self.row)
        matr = copy_matrix(self)
        for i in range(n-1):
            matr = matr * self
        return matr

    def __call__(self, x, y):
        return self.get(x-1, y-1)

    def __getitem__(self, x, y):
        return self.get(x-1, y-1)

    def __getitem__(self, x_y):
        return self.get(x_y[0]-1, x_y[1]-1)

    def get(self, x, y):
            return self.rows[x][y]

    def kth(self, k):
        new_matr = [ [k * i for i in j] for j in self.rows]
        return Matrix(new_matr)


    def tran(self):
        return Matrix(self.columns)

    def cofactor(self, row, column):
        assert self.row == self.column, "只有方阵才有代数余子式"
        new_matr = [ [self.get(i, j) for j in range(self.column) if j != column] for i in range(self.row) if i != row]
        return Matrix(new_matr)

    def adjoint_matrix(self):
        assert self.row == self.column, "只有方阵才有伴随矩阵"
        rows_list = [[ self.cofactor(i, j).determinant() * pow(-1, i+j) for j in range(self.column) ] for i in range(self.row)]
        return Matrix(rows_list).tran()

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
        E = Matrix(E_rows) + identity_matrix(self.row)
        new_matr     = E * self
        self.row     = new_matr.row
        self.column  = new_matr.column
        self.rows    = new_matr.rows
        self.columns = new_matr.columns
        self.type    = new_matr.type
        self.cls     = self.cls
        return E if oper else None

    def rref(self, display=False):
        matr     = copy_matrix(self)
        min_semi = min(matr.row, matr.column)
        if display: print(matr, end='\n\n')

        for column in range(min_semi):
            for row in range(matr.row):
                if column == row:continue

                if matr.get(column, column) == 0:
                    k = None
                    for k in range(column+1, matr.row):
                        matr = matr.swap_row(column, k)                                         # matr.get(column, column) for pivot_varible value
                        if matr.get(column, column) != 0: break
                    if  k is None or matr.get(column, column) == 0: continue

                matr.add_row(-(matr.get(row, column)/matr.get(column, column)), column, row)    # matr.get(row, column) for free_varible value
                if display: print(matr, end='\n\n')

            # make every pivot variable equal to 1
            for column in range(min_semi):
                if matr.get(column, column) != 0 and matr.get(column, column) != 1:
                    matr.add_row((1/matr.get(column, column)) - 1, column, column)
        return matr

class Augment(Matrix):
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

    def __repr__(self, end=''):
        matrix_string = ''
        lenth_list = []
        for j in range(self.column):
            lenth_list.append( max( [ len(str(i)) for i in self.columns[j] ]) )

        for i in range(self.row):
            matrix_string += "("
            for j in range(self.column):
                max_lenth_in_a_column = lenth_list[j]
                value                = self.get(i, j)
                seperator             = ', ' if j != self.x.column-1 else ' ⏐ '
                trailing              = ')\n' if i != self.row - 1 else ')'
                matrix_string += str(value).rjust(max_lenth_in_a_column)       # value in matrix
                matrix_string += seperator if j != self.column-1 else trailing  # prefix and sufix in matrix
        matrix_string += end
        return matrix_string

    def rref(self, display=False):
        show      = lambda matr: display and print(matr, end = '\n\n')
        matr      = Augment(self.x, self.y)
        min_semi  = min(matr.x.row, matr.x.column)
        show(matr)

        for column in range(min_semi):
            for row in range(matr.x.row):
                if column == row:continue

                if matr.get(column, column) == 0:
                    k = None
                    for k in range(column+1, matr.x.row):
                        matr = matr.swap_row(column, k)
                        if matr.get(column, column) != 0: break
                    if  k is None: continue

                scale = -(matr.get(row, column)/matr.get(column, column))
                matr.x.add_row(scale, column, row)
                matr.y.add_row(scale, column, row)
                matr = Augment(matr.x, matr.y)
                show(matr)

            for column in range(min_semi):      # make every pivot variable equal to 1
                if matr.get(column, column) != 0 or matr.get(column, column) != 1:
                    scale = (1/matr.get(column, column)) - 1
                    matr.x.add_row(scale, column, column)
                    matr.y.add_row(scale, column, column)
                    matr = Augment(matr.x, matr.y)
        return matr

def identity_matrix(n, x=0, y=0):
    rows_list = []
    for i in range(n):
        if i == x:
            rows_list.append(make_E_row(n, 1, y))
        elif i == y:
            rows_list.append(make_E_row(n, 1, x))
        else:
            rows_list.append(make_E_row(n, 1, i))
    return Matrix(rows_list)

def is_matrix(matr):
    return hasattr(matr, 'cls')

def is_augment(matr):
    return hasattr(matr, 'cls') and (matr.cls == "Augment")

def make(*args):
    row, column = (args[0], args[0]) if len(args) == 1 else (args[0], args[1])
    rows_list = []
    try:
        for i in range(row):
            rows_list.append([Fraction(input(f"[{i+1},{j+1}]: ")) for j in range(column)])
    except KeyboardInterrupt:
        return print('\nexit, try again!')
    return Matrix(rows_list)

def copy_list(lst):
    """just to deep copy a list
    """
    new_list = []
    for i in lst:
        if type(i) == list:
            i = copy_list(i)
            new_list.append(i)
            continue
        new_list.append(Fraction(i))
    return new_list

def copy_matrix(matr):
    return Matrix([copy_list(i) for i in matr.rows])

def zero_matrix(*args):
    assert len(args) >= 1, "matrix must have rows and columns"
    row, column = (args[0], args[0]) if len(args) == 1 else (args[0], args[1])
    lst = [0 for i in range(column)]
    return Matrix([copy_list(lst) for i in range(row)])

def make_E_row(n, k, b):
    return [(0 if i != b else k) for i in range(n)]

f     = Fraction
row1  = [1, 0]
row2  = [2, 3]
row3  = [4, 5]
row4  = [2, 1]
row5  = [4, 3]
row6  = [1, 2, 3, 2]
row7  = [2, 1, 2, 3]
row8  = [3, 2, 1, 2]
row9  = [2, 3, 2, 3/4]
row10 = [6]
row11 = [8]
row12 = [4]
row13 = [8]
row14 = [2, 1, 1, 0]
a = Matrix([row6, row7, row8, row9]).tran()
b = Matrix([row10, row11, row12, row13])
c = Matrix([row1, row2, row3])
d = Matrix([row4, row5])
c = Augment(a, b)
augment = lambda x, y: Augment(x, y)
