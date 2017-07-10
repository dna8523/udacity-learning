def linearRegression(points):
    X, Y = [], []
    for i in range(len(points)):
        Y.append([])
        Y[i].append(points[i][1])
        X.append([])
        X[i].append(points[i][0])
        X[i].append(1)
    b = matxMultiply(transpose(X), Y)
    A = matxMultiply(transpose(X), X)
    return gj_Solve(A, b)
