# coding=utf-8 

def sample(matrix, size):
    """
    二次采样，只针对U和V
    """
    temp = []
    for X in range(0, size[0] // 2): # 枚举每个2*2小矩形
        for Y in range(0, size[1] // 2):
            idx = X * 2 * size[1] + Y * 2 # 算出该小矩形左上角的索引
            temp.append(matrix[idx])  # 保留该值
    return temp

def Inverse_sample(matrix, size):
    """
    解除采样
    将原先每个2*2的小矩形的4个单元都填入原左上角的那个值
    """
    temp = []
    for X in range(0, size[0]):
        for i in range(0, 2): # X为采样后的矩形的行数，对于一个值要连续填充两行，用i来枚举
            for Y in range(0, size[1]): # 枚举一行中的每一列
                idx = X * size[1] + Y  # 原左上角的值在采样后的矩阵里的索引
                temp.append(matrix[idx])  #填充两次达到填充了相邻两列的目的
                temp.append(matrix[idx])
    return temp