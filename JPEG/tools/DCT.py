# coding=utf-8 

import math
M = 8

def C(u, N):
    return math.sqrt(1.0 / N) if u == 0 else math.sqrt(2.0 / N)

def DCT(matrix):
    DCT_matrix = []
    for u in range(0, M):
        for v in range(0, M):
            tmp = 0
            for i in range(0, M):
                for j in range(0, M):
                    tmp += math.cos((2*i+1)*u*math.pi/(2*M)) * math.cos((2*j+1)*v*math.pi/(2*M)) * matrix[i*M+j]
            DCT_matrix.append(int(round(C(u,M)*C(v,M)*tmp)))
    return DCT_matrix
"""
# IDCT 很耗时间，可以转换成垂直方向和水平方向各一次共两次一维IDCT完成
def oneIDCT(Array, i):
    result = 0
    for u in range(0, M):
        result += math.cos((2*i+1) * u * math.pi / 16) * Array[u] * C(u,M)
    return result
def IDCT(matrix):
    IDCT_temp = list(range(64))
    IDCT_matrix = list(range(64))
    # 列 IDCT
    for i in range(0, M):
        temp = []
        for j in range(0, M):
            temp.append(matrix[i + j * M])
        for j in range(0, M):
            IDCT_temp[i + j * M] = (oneIDCT(temp, j))

    # 行 IDCT
    for i in range(0, M):
        temp = []
        for j in range(0, M):
            temp.append(IDCT_temp[i * M  + j])
        for j in range(0, M):
            IDCT_matrix[i * M + j] = (oneIDCT(temp, j))
    return IDCT_matrix
"""
def IDCT(matrix):
    IDCT_matrix = []
    for i in range(0, M):
        for j in range(0, M):
            tmp = 0
            for u in range(0, M):
                for v in range(0, M):
                    tmp += C(u, M)*C(v, M)*math.cos((2*i+1)*u*math.pi/(2*M)) * math.cos((2*j+1)*v*math.pi/(2*M)) * matrix[u*M+v]
            IDCT_matrix.append(tmp)
    return IDCT_matrix

def Do_DCT(matrix, N):
    temp = []
    for i in range(0, N):
        temp.append(DCT(matrix[i]))
    return temp

def Do_IDCT(matrix, N):
    temp = []
    for i in range(0, N):
        temp.append(IDCT(matrix[i]))
    return temp