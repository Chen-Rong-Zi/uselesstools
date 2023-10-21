def main():
    test = []
    test = [i for i in range(10)]
    return test

test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
test  = main()
print(test)
test.append(10)
main()
print(test)
