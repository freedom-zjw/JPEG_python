# coding=utf-8
M = 8

def check(i, j):
    return i >=0 and j >=0 and i < M and j < M

def zigzag(matrix, Zigzag_order):
    """
    zigzag扫描
    """
    temp = []
    i, j =0, 0
    direct = 1 # 0 for 左下， 1 for 右上
    temp.append(matrix[0])
    for k in range(0, M * M - 1):
        if direct == 0:
            if check(i+1, j-1): # check是检查是否超出边界
                i, j = i+1, j-1
            elif check(i+1, j):
                i, direct = i+1, 1
            elif check(i, j+1):
                j, direct = j+1, 1
        else:
            if check(i-1, j+1):
                i, j = i-1, j+1
            elif check(i, j+1):
                j, direct = j+1, 0
            elif check(i+1, j):
                i, direct = i+1, 0
        if len(Zigzag_order) != M*M: # Zigzag_order[i]表示扫描后的第i个在扫描前的索引。
            Zigzag_order.append(i * M + j)
        temp.append(matrix[i * M + j])
    return temp

def re_zigzag(matrix, Zigzag_order):
    """
    使用Zigzag_order恢复扫描前的顺序
    """
    temp = list(range(64))
    for i in range(64):
        temp[Zigzag_order[i]] = matrix[i]
    return temp