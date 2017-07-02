
def gj_Solve(A, b, decPts=4, epsilon=1.0e-16):
    if len(A) != len(b):
        return None
    Ab = augmentMatrix(A, b)
    for c in range(len(A[0])):
        if max(abs(el) for el in transpose(A)[c]) == 0:
            return None
        else:
            swap(Ab,)


def swapRows(M, r1, r2):
    t = M[r1]
    M[r1] = M[r2]
    M[r2] = t


def scaleRow(M, r, scale):
    if scale == 0:
        assertRaises(ValueError)
    for i in range(len(M[r])):
        M[r][i] *= scale


def addScaledRow(M, r1, r2, scale):
    for i in range(len(M[r1])):
        M[r1][i] += M[r2][i] * scale


def augmentMatrix(A, b):
    for row in range(len(A)):
        A[row].append(b[row][0])
    return A


def transpose(M):
    a = []
    for i in range(len(M[0])):
        a.append([])
        for j in range(len(M)):
            a[i].append(M[j][i])
    return a


def matxMultiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError
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
     [2, 3, 3],
     [1, 2, 5]]
b = [[2], [4]]
c = matxMultiply(A, b)
print c, A
