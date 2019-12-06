# coding=utf-8 

"""
fill: 将原图像长宽用0补齐到16的倍数
re_fill: fill的反操作
"""

def fill(img, size):
    """
    fill: 将原图像长宽用0补齐到16的倍数
    """
    newsize = [0, 0]
    new_img = [[], [], []]
    # 先计算填充后的长和宽分别是多少
    newsize[0] = size[0] + 16 - size[0]%16 if size[0] % 16 != 0 else size[0] 
    newsize[1] = size[1] + 16 - size[1]%16 if size[1] % 16 != 0 else size[1]

    for k in range(3): # 分别枚举Y、U、V
        for i in range(newsize[0]):  # 枚举填充后的图像的每个像素点(i,j)
            for j in range(newsize[1]):
                if i < size[0] and j < size[1]: #(i,j)处于原图范围内，就用原图的数值
                    new_img[k].append(img[k][i * size[1] + j]) 
                else: # (i,j)在原图范围外就补0
                    new_img[k].append(0)

    return new_img[0], new_img[1], new_img[2], newsize

def re_fill(matrix, size, newsize):
    """
    解除填充
    保留填充后的图像中原图的部分，去掉补0的部分
    """
    ori_img = [[], [], []]
    print(size, newsize, len(matrix))
    for k in range(3):
        for i in range(0, newsize[0]):
            for j in range(0, newsize[1]):
                if i < size[0] and j < size[1]: # (i,j)是原图范围内的才保留
                    ori_img[k].append(matrix[k][i * newsize[1] + j])
    return ori_img