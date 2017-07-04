import pprint
pp = pprint.PrettyPrinter(indent=1, width=40)


def gj_Solve(A, b, decPts=4, epsilon=1.0e-16):
    if len(A) != len(b):
        return None
    Ab = augmentMatrix(A, b)
    for c in range(len(A)):
        maxabs = max(abs(el) for el in transpose(Ab)[c][c:])
        if maxabs < epsilon:
            return None
        else:
            try:
                max_row = transpose(Ab)[c].index(maxabs)
                scale = 1. / maxabs
            except ValueError:
                max_row = transpose(A)[c].index(-1 * maxabs)
                scale = -1. / maxabs
            if c != max_row:
                swapRows(Ab, c, max_row)
            if Ab[c][c] != 1:
                scaleRow(Ab, c, scale)
                matxRound(Ab, decPts)
            if sum(transpose(Ab)[c]) != 1:
                for r in range(len(A)):
                    if r != c and Ab[r][c] != 0:
                        addScaledRow(Ab, r, c, -Ab[r][c])
                        matxRound(Ab, decPts)
    matxRound(Ab, decPts)
    X = []
    for rows in range(len(X)):
        X.append([])
        X[rows][0] = Ab[rows][-1]
    return X


def matxRound(M, decPts=4):
    for i in range(len(M)):
        for j in range(len(M[0])):
            M[i][j] = round(M[i][j], decPts)


def swapRows(M, r1, r2):
    t = M[r1]
    M[r1] = M[r2]
    M[r2] = t


def scaleRow(M, r, scale):
    if scale == 0:
        raise ValueError
    for i in range(len(M[r])):
        M[r][i] *= scale


def addScaledRow(M, r1, r2, scale):
    for i in range(len(M[r1])):
        M[r1][i] += M[r2][i] * scale


def augmentMatrix(A, b):
    c = []
    for i in range(len(A)):
        c.append([])
        for j in range(len(A[0])):
            c[i].append(A[i][j])
    for row in range(len(A)):
        c[row].append(b[row][0])
    return c


def transpose(M):
    a = []
    for i in range(len(M[0])):
        a.append([])
        for j in range(len(M)):
            a[i].append(M[j][i])
    return a


def matxMultiply(A, B):
    if len(A[0]) != len(B):
        return None
    else:
        multy = []
        B = transpose(B)
        for i in range(len(A)):
            multy.append([])
            for j in range(len(B)):
                t = sum([x * y for x, y in zip(A[i], B[j])])
                multy[i].append(t)
    return multy


A = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
b = [[2], [4], [8]]
print gj_Solve(A, b)
