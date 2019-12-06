# coding=utf-8 
M = 8
from .Table import DC_Chroma_Huffman, DC_Luminance_Huffman
from .Table import AC_Chroma_Huffman, AC_Luminance_Huffman

def RLE(temp, src): # AC游长编码
    zero_cnt = 0
    for i in range(1, M*M):
        if src[i] != 0:# 遇到了不为0的数（则增加一个数对）
            temp.append((zero_cnt, src[i]))
            zero_cnt = 0
        elif i == M*M-1: # 到块末尾了还是0也要增加一个数对
            temp.append((zero_cnt, src[i]))
        else:
            zero_cnt += 1 # 遇到0就计数器+1
        if zero_cnt > 15: #jpeg使用一个字节的高4位表示连续0的个数，即最多15个
            temp.append((15, 0))
            zero_cnt = 0

def DC_and_AC_encode(matrix, length):
    result = []
    for i in range(length):
        temp = []
        #DC-DPCM encode
        if i == 0: #第一个块的DC分量的编码是自己
            temp.append((0, matrix[i][0]))
        else:  # 后续的DC分量的编码是与前一个的差值
            temp.append((0, matrix[i][0] - matrix[i - 1][0]))
        #AC-RLE encode
        RLE(temp, matrix[i])
        result.append(temp)
    return result

def DC_and_AC_decode(matrix, length):
    result = []
    for i in range(length):
        temp = []
        for j in range(len(matrix[i])):# 枚举每一个数对
            for k in range(matrix[i][j][0]):  #先加入RUNLENGTH个0
                temp.append(0)
            if i > 0 and j == 0: # 每个块的第一个数对是DC分量，恢复DC分量
                temp.append(matrix[i][j][1] + result[i-1][0])
            else:# 恢复AC分量
                temp.append(matrix[i][j][1])
        result.append(temp)
    return result

def Dec2Bin(num): # 十进制转化二进制
    i = 0
    bin_num = 0
    num = abs(num)
    while num != 0:
        temp = num % 2
        num = num // 2
        bin_num = bin_num + temp*(10**i)
        i += 1
    return bin_num

def Bin2Dec(num): # 二进制转十进制
    Dec_num = 0
    i = 0
    while num != 0:
        temp = num % 10
        num = num // 10
        Dec_num = Dec_num + temp*(2**i)
        i += 1
    return Dec_num

def VLI(num):
    Bin_num = str(Dec2Bin(num))
    VLI_num = ''
    if num < 0:
        for i in range(len(Bin_num)):
            if Bin_num[i] == '0':
                VLI_num = VLI_num + '1'
            elif Bin_num[i] == '1':
                VLI_num = VLI_num + '0'
    else:
        VLI_num = Bin_num
    VLI_num_len = len(VLI_num)
    if num == 0:
        VLI_num_len = 0
        VLI_num = ''
    return (VLI_num_len, VLI_num)

def De_VLI(VLI_num):
    # 第一个数字为0说明是负数
    if VLI_num[0] == '0':
        temp = ''
        for i in range(len(VLI_num)):
            if VLI_num[i] == '1':
                temp += '0'
            elif VLI_num[i] == '0':
                temp += '1'
        return -Bin2Dec(int(temp))
    else:
        return Bin2Dec(int(VLI_num))

def Entropy_encode(matrix, length, DC_AC):
    result = []
    for k in range(length):
        tot_len = 0  # 用来统计已经编码掉的数，总共64个数，比如AC的游长编码得到一个数对(3,2)这里是3+1=4个数。
        (DC_VLI_len, DC_VLI_code) = VLI(matrix[k][0][1]) # 求出DC的VLI数对
        DC_Huffman_code = ''
        if DC_AC == 0: # 查表得DC 的Huffman编码
            DC_Huffman_code = DC_Luminance_Huffman[DC_VLI_len]
        else:
            DC_Huffman_code = DC_Chroma_Huffman[DC_VLI_len]
        entropy = DC_Huffman_code + DC_VLI_code  # 拼接得到熵编码
        tot_len += 1
        for i in range(1, len(matrix[k])):
            (AC_VLI_len, AC_VLI_code) = VLI(matrix[k][i][1]) # 求出AC的VLI数对
            AC_Huffman_code = ''
            if tot_len + matrix[k][i][0] + 1 == 64 and matrix[k][i][1] == 0:  # 判断是否是最后一个数对
                if DC_AC == 0:
                    AC_Huffman_code = AC_Luminance_Huffman[(15, 0)]
                else:
                    AC_Huffman_code = AC_Chroma_Huffman[(15, 0)]
                tot_len += 16
            else: #不是最后一个数对
                if DC_AC == 0:
                    AC_Huffman_code = AC_Luminance_Huffman[(matrix[k][i][0], AC_VLI_len)]
                else:
                    AC_Huffman_code = AC_Chroma_Huffman[(matrix[k][i][0], AC_VLI_len)]
                tot_len += matrix[k][i][0] + 1
            entropy += AC_Huffman_code + AC_VLI_code
        result.append(entropy)
    return result

def Entropy_decode(matrix, length, DC_AC):
    result = []
    for i in range(length):
        j, tot_len, isFirst, str_temp, temp = 0, 0, 0, '', []
        while j < len(matrix[i]):
            str_temp += matrix[i][j]
            j += 1
            if DC_AC == 0: # 0 为亮度 1 为色度
                if isFirst == 0: # 第一个用DC Huffman表
                    items = DC_Luminance_Huffman.items()
                elif isFirst == 1: # 否则用AC Huffman表
                    items = AC_Luminance_Huffman.items()
            elif DC_AC == 1:
                if isFirst == 0: # 第一个用DC Huffman表
                    items = DC_Chroma_Huffman.items()
                elif isFirst == 1: # 否则用AC Huffman表
                    items = AC_Chroma_Huffman.items()
            for (k, v) in items:
                if v == str_temp:
                    str_temp = ''
                    if isFirst == 0: # DC的VLI变回整数
                        VLI_str = ''
                        for z in range(k):
                            VLI_str += matrix[i][j]
                            j += 1
                        if VLI_str == '':
                            temp.append((0, 0))
                        else:
                            temp.append((0, De_VLI(VLI_str)))
                        tot_len += 1
                    elif isFirst == 1: # AC的VLI变回整数,此时k为(RUNLENGTH,AC_VLI_len)
                        VLI_str = ''
                        for z in range(k[1]):
                            VLI_str += matrix[i][j]
                            j += 1
                        if VLI_str == '':
                            if tot_len + k[0] + 1 > 64:
                                temp.append((64 - tot_len - 1, 0))
                            else:
                                temp.append((k[0], 0))
                        else:
                            temp.append((k[0], De_VLI(VLI_str)))
                        tot_len += k[0] + 1
                    isFirst = 1
                    break
        result.append(temp)
    return result
