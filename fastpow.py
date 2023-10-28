from matrix import make, mul, p, matrix, powm

def fib_pow(n):
    fib = matrix([[0], [1]])
    factor = matrix([[0, 1], [1, 1]])
    if n == 0:
        return fib(0, 0)
    elif n == 1:
        return fib(1, 0)
    for i in range(n):
        fib = mul(factor, fib)
    return fib

def matrix_fastpow(matr, n):
    assert n >= 1, "matrix_fastpow only possible when n >= 1!"
    if n == 1:
        return matr
    elif n % 2 == 0:
        return matrix_fastpow(powm(matr, 2), n/2)
    else:
        return mul(matr, matrix_fastpow(matr, n-1))
