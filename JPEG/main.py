# coding=utf-8 

from PIL import Image
import matplotlib.pyplot as plt
from tools.Color_Change import RGB2YUV, YUV2RGB
from tools.Fill import  fill, re_fill
from tools.Sample import sample, Inverse_sample
from tools.Block import partition, merge
from tools.DCT import Do_DCT, Do_IDCT
from tools.Quantization import Do_Quantization, Do_DeQuantization
from tools.Zigzag import zigzag, re_zigzag
from tools.Encode import DC_and_AC_encode, Entropy_encode, DC_and_AC_decode, Entropy_decode

def show(matrix):
    print(matrix[0:20])

def showblock(matrix):
    for i in range(0, 8):
        for j in range(0, 8):
            print(round(matrix[i * 8 + j],2), end="")
            print("  ", end="")
        print("")

def main():
    image_path = "lena.jpg"
    img = Image.open(image_path)
    ori_size = img.size  # 记录原始图片大小，方便解压缩
    print("Ori imgesize:", ori_size)
#--------------------------------------------------------------编码过程
    # 颜色空间转换 RGB -> YUV
    print("Color changing: RGB -> YUV...")
    Y, U, V = RGB2YUV(img)
    show(Y)
    
    
    # 将原图像长宽用0补齐到16的倍数
    print("Filling...")
    Y, U, V, new_size = fill([Y, U, V], ori_size)
    print("New imgesize:", new_size)
    #print("The Y after filling:")
    #show(Y)
    #new_size = 416
    

    # 二次采样 4：1：1
    print("Sampling...")
    U = sample(U, new_size)
    V = sample(V, new_size)
    new_size2 = [new_size[0]//2, new_size[1]//2] #[208, 208]
    print("New imgesize2:", new_size2)
    
    
    # 分块，DCT变换是对8*8子块进行处理，将YUV分成若干 8*8 矩阵
    print("Partitioning...")
    Y_block = partition(Y, new_size)
    U_block = partition(U, new_size2)
    V_block = partition(V, new_size2)
    print("The first block of Y:")
    showblock(Y_block[0])
    

    # DCT 
    print("DCT...")
    Y_block = Do_DCT(Y_block, len(Y_block))
    U_block = Do_DCT(U_block, len(U_block))
    V_block = Do_DCT(V_block, len(V_block))
    print("The first block of Y after DCT:")
    showblock(Y_block[0])
    

    # 量化 0为亮度 1为色度
    print("Quantization...")
    Y_block = Do_Quantization(Y_block, len(Y_block), 0)
    U_block = Do_Quantization(U_block, len(U_block), 1)
    V_block = Do_Quantization(V_block, len(V_block), 1)
    print("The first block of Y after quantization:")
    showblock(Y_block[0])
    

    # Zigzag 
    print("Zigzag sort...")
    Zigzag_order = [0]
    Zigzag_Y_matrix, Zigzag_U_matrix, Zigzag_V_matrix = [], [], []
    for i in range(len(Y_block)):
        Zigzag_Y_matrix.append(zigzag(Y_block[i], Zigzag_order))
    for i in range(len(U_block)):
        Zigzag_U_matrix.append(zigzag(U_block[i], Zigzag_order))
    for i in range(len(V_block)):
        Zigzag_V_matrix.append(zigzag(V_block[i], Zigzag_order))
    print("The first block of Y after Zigzag:")
    print(Zigzag_Y_matrix[0])
    
    # DC and AC encode
    print("DC and AC encoding...")
    Y_encoded = DC_and_AC_encode(Zigzag_Y_matrix, len(Zigzag_Y_matrix))
    U_encoded = DC_and_AC_encode(Zigzag_U_matrix, len(Zigzag_U_matrix))
    V_encoded = DC_and_AC_encode(Zigzag_V_matrix, len(Zigzag_V_matrix))
    #print(len(Y_encoded), len(U_encoded), len(V_encoded))
    print("The first block of Y after DC and AC encode:")
    print(Y_encoded[0])
    

    # 熵编码 0为亮度 1为色度
    print("Entropy encoding...")
    Y_encoded = Entropy_encode(Y_encoded, len(Y_encoded), 0)
    U_encoded = Entropy_encode(U_encoded, len(U_encoded), 1)
    V_encoded = Entropy_encode(V_encoded, len(V_encoded), 1)
    #print(len(Y_encoded), len(U_encoded), len(V_encoded))
    print("The first block of Y after entropy encoding:")
    print(Y_encoded[0])

    ori_tot_bits = ori_size[0] * ori_size[1] * 3 * 8
    now_tot_bits = 0
    for i in range(len(Y_encoded)):
        now_tot_bits += len(Y_encoded[i])
    for i in range(len(U_encoded)):
        now_tot_bits += len(U_encoded[i])
    for i in range(len(V_encoded)):
        now_tot_bits += len(V_encoded[i])
    print("原图总位数：{}".format(ori_tot_bits))
    print("压缩后总位数：{}".format(now_tot_bits))
    print("压缩比：{}".format(ori_tot_bits/now_tot_bits))

#--------------------------------------------------------------解码过程
    # 熵解码 0为亮度 1为色度
    print("Entropy decoding...")
    Y_decoded = Entropy_decode(Y_encoded, len(Y_encoded), 0)
    U_decoded = Entropy_decode(U_encoded, len(U_encoded), 1)
    V_decoded = Entropy_decode(V_encoded, len(V_encoded), 1)
    print(len(Y_decoded), len(U_decoded), len(V_decoded))
    
    # 解码DC编码和AC编码
    print("DC and AC decoding...")
    Zigzag_Y_matrix = DC_and_AC_decode(Y_decoded, len(Y_decoded))
    Zigzag_U_matrix = DC_and_AC_decode(U_decoded, len(U_decoded))
    Zigzag_V_matrix = DC_and_AC_decode(V_decoded, len(V_decoded))
    #print(len(Zigzag_Y_matrix), len(Zigzag_U_matrix), len(Zigzag_V_matrix))
    for i in range(len(Zigzag_Y_matrix)):
        if len(Zigzag_Y_matrix[i])!=64:
            print("Y error", len(Zigzag_Y_matrix[i]))
            return
    for i in range(len(Zigzag_U_matrix)):
        if len(Zigzag_U_matrix[i])!=64:
            print("U error")
            return
    for i in range(len(Zigzag_V_matrix)):
        if len(Zigzag_V_matrix[i])!=64:
            print("V error")
            return
    
    # 还原Zigzag扫描
    print("Reverse Zigzag sort...")
    Y_block, U_block, V_block = [], [], []
    for i in range(len(Zigzag_Y_matrix)):
        Y_block.append(re_zigzag(Zigzag_Y_matrix[i], Zigzag_order))
    for i in range(len(Zigzag_U_matrix)):
        U_block.append(re_zigzag(Zigzag_U_matrix[i], Zigzag_order))
    for i in range(len(Zigzag_V_matrix)):
        V_block.append(re_zigzag(Zigzag_V_matrix[i], Zigzag_order))  
    #print(len(Y_block), len(U_block), len(V_block))
    for i in range(len(Y_block)):
        if len(Y_block[i])!=64:
            print("Y error")
            return
    for i in range(len(U_block)):
        if len(U_block[i])!=64:
            print("U error")
            return
    for i in range(len(V_block)):
        if len(V_block[i])!=64:
            print("V error")
            return
    
    
    # 反量化 0为亮度 1为色度
    print("De Quantization...")
    Y_block = Do_DeQuantization(Y_block, len(Y_block), 0)
    U_block = Do_DeQuantization(U_block, len(U_block), 1)
    V_block = Do_DeQuantization(V_block, len(V_block), 1)
    #print(len(Y_block), len(U_block), len(V_block))
    for i in range(len(Y_block)):
        if len(Y_block[i])!=64:
            print("Y error")
            return
    for i in range(len(U_block)):
        if len(U_block[i])!=64:
            print("U error")
            return
    for i in range(len(V_block)):
        if len(V_block[i])!=64:
            print("V error")
            return
    
    # IDCT 逆DCT
    print("IDCT...")
    Y_block = Do_IDCT(Y_block, len(Y_block))
    U_block = Do_IDCT(U_block, len(U_block))
    V_block = Do_IDCT(V_block, len(V_block))
    #print(len(Y_block), len(U_block), len(V_block))
    for i in range(len(Y_block)):
        if len(Y_block[i])!=64:
            print("Y error")
            return
    for i in range(len(U_block)):
        if len(U_block[i])!=64:
            print("U error")
            return
    for i in range(len(V_block)):
        if len(V_block[i])!=64:
            print("V error")
            return
    
    
    # 块合并
    print("Merge block...")
    Y = merge(Y_block, new_size)
    U = merge(U_block, new_size2)
    V = merge(V_block, new_size2)
    #print(len(Y), len(U), len(V))
    
    # 反采样
    print("Inverse Sampling...")
    U = Inverse_sample(U, new_size2)
    V = Inverse_sample(V, new_size2)
    print("The Y after before Inverse Filling:")
    show(Y)
    
    # 反填充
    print("Inverse Filling...")
    Y, U, V = re_fill([Y, U, V], ori_size, new_size)
    
    # YUV -> RGB
    print("Color changing: YUV->RGB...")
    R, G, B = YUV2RGB(Y, U, V)

    #生成jpeg 图片
    print("Saving jpeg...")
    img = Image.new("RGB", (ori_size[0], ori_size[1]))
    x, y = ori_size[0], ori_size[1]
    for i in range(0, x):
        for j in range(0, x):
            img.putpixel((i, j), (int(R[i*y+j]), int(G[i*y+j]), int(B[i*y+j])))
    
    img.save("lena.jpeg")


def test_entropy():
    Y = [[(0,0),(15,0),(15,-1),(15,0),(14,0)]]
    print(Y)
    Y_en = Entropy_encode(Y, len(Y), 0)
    print("Y_en:")
    print(Y_en)
    Y_de = Entropy_decode(Y_en, len(Y_en), 0)
    print("Y_de:")
    print(Y_de)


if __name__ == '__main__':
    main()
    #test_entropy()