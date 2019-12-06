# coding=utf-8 

def partition(matrix, size):
    """
    分块操作
    """
    temp = []
    temp_size = 8 # 分块后的每一块的长和宽均为8
    for i in range(0, size[0] // temp_size):
        for j in range(0, size[1] // temp_size):
            start_idx = i * size[1] * 8 + j * 8 # 枚举每一个8*8块的左上角索引----起点索引
            block = []
            for k in range(0, temp_size):   # 将该块的64个值拿出来存入一个block
                for L in range(0, temp_size):
                    block.append(matrix[start_idx + k * size[1] + L])
            temp.append(block)
    return temp

def merge(matrix, size):
    """
    合并分块
    """
    temp = []
    M = 8
    for i in range(size[0] // M):  # (i,j)为某一个块的索引
        for k in range(0, M):      # (k, L)为 （i,j)这个块中每一个元素的索引
            for j in range(0, size[1] // M):
                for L in range(0, M):   # 按照分块前每一行每一列的顺序枚举元素
                    if i * (size[1] // M) + j >= len(matrix): 
                        continue
                    elif k * M + L >= len(matrix[i * (size[1] // M) + j]):
                        continue
                    temp.append(matrix[i * (size[1] // M) + j][k * M + L])
    return temp