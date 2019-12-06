# coding=utf-8 

"""
颜色空间转换
RBG2YUV: RGB -> YUV
YUV2RGB: YUV -> RGB
"""

def RGB2YUV(img):
    """
    RBG2YUV: RGB -> YUV
    根据公式换算，一般来说U,V是有符号的数字，
    但这里通过加上128，使其变为无符号数，
    方便存储和计算
    另外这一步将存储格式从二维转成了一维
    """
    size = img.size
    Y, U, V = [], [], []
    for i in range(size[0]):
        for j in range(size[1]):
            pixel = img.getpixel((i, j))
            Y.append(0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2])
            U.append(-0.1687*pixel[0] - 0.3313*pixel[1] + 0.5*pixel[2] + 128)
            V.append(0.5*pixel[0] - 0.4187*pixel[1] - 0.0813*pixel[2] + 128)
    return Y, U, V

def YUV2RGB(Y, U, V):
    """
    YUV2RGB: YUV -> RGB
    """
    R, G, B = [], [], []
    for i in range(0, len(Y)):
        R.append(Y[i] + 1.402*(V[i] - 128))
        G.append(Y[i] - 0.34414*(U[i] - 128) - 0.71414*(V[i] - 128))
        B.append(Y[i] + 1.772*(U[i] - 128))
    return R, G, B
