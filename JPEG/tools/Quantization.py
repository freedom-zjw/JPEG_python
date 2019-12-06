# coding=utf-8 

M = 8
import math
from .Table import Luminance_Quantization_Matrix, Chroma_Quantization_Matrix

def Luminance_Quantization(matrix, M):
    temp = []
    for i in range(0, M*M):
        temp.append(int(round(1.0 * matrix[i] / Luminance_Quantization_Matrix[i])))
    return temp

def De_Luminance_Quantization(matrix, M):
    temp = []
    for i in range(0, M*M):
        temp.append(matrix[i] * Luminance_Quantization_Matrix[i])
    return temp


def Chroma_Quantization(matrix, M):
    temp = []
    for i in range(0, M*M):
        temp.append(int(round(1.0 * matrix[i] / Chroma_Quantization_Matrix[i])))
    return temp

def De_Chroma_Quantization(matrix, M):
    temp = []
    for i in range(0, M*M):
        temp.append(matrix[i] * Chroma_Quantization_Matrix[i])
    return temp

def quantization(matrix, DC_AC):
    quantization_matrix = []
    if DC_AC == 0: # 亮度量化
        quantization_matrix = Luminance_Quantization(matrix, M)
    else: # 色度量化
        quantization_matrix = Chroma_Quantization(matrix, M)
    return quantization_matrix

def Dequantization(matrix, DC_AC):
    Dequantization_matrix = []
    if DC_AC == 0: #亮度反量化
        Dequantization_matrix = De_Luminance_Quantization(matrix, M)
    else:#色度反量化
        Dequantization_matrix = De_Chroma_Quantization(matrix, M)
    return Dequantization_matrix

def Do_Quantization(matrix, N, DC_AC):
    temp = []
    for i in range(0, N):
        temp.append(quantization(matrix[i], DC_AC))
    return temp

def Do_DeQuantization(matrix, N, DC_AC):
    temp = []
    for i in range(0, N):
        temp.append(Dequantization(matrix[i], DC_AC))
    return temp