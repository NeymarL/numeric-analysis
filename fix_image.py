#! /usr/bin/env python
# -*- coding:utf-8 -*-
# fix_image.py
# 图像修复、降噪

#from scipy import signal
import numpy as np
import matplotlib.pylab as plt

def fix_image(X, ld, u, Q1, Q2):
    '''
    计算每个点的受腐蚀程度, 并返回修复后的图像
    X   ndarray 像素矩阵
    ld  int     邻域方窗大小 (2 * ld + 1) ^ 2
    u   int     确定ita的阈值
    Q1  number  腐蚀程度下限
    Q2  number  腐蚀程度上限

    返回值
    New ndarray 修复后的像素矩阵
    '''
    ita = np.zeros(X.shape)
    Lambda = np.zeros(X.shape)
    New = X.copy()
    (m, n) = X.shape
    T = (2 * ld + 1) * (2 * ld + 1)

    for i in range(ld, m - ld + 1):
        for j in range(ld, n - ld + 1):
            w = X[i - ld : i + ld + 1, j - ld : j + ld + 1]
            A = w.reshape(-1)
            A.sort()
            delta = A - X[i, j]
            omiga = delta.sum()
            kesai = 0
            if(X[i,j] <= A[u] or X[i,j] >= A[T - u + 1]):
                ita[i, j] = 1
                kesai = omiga / (T - 1)

            if kesai <= Q1:
                Lambda[i, j] = 0
            elif kesai > Q1 and kesai <= Q2:
                Lambda[i, j] = (kesai - Q1) * 1.0 / (Q2 - Q1)
            else:
                Lambda[i, j] = 1

            New[i, j] = (1 - Lambda[i, j]) * X[i, j] +\
                Lambda[i, j] * A[(T - 1) / 2 - 1]

    return New

def test():
    img = plt.imread('Sublime_text_256x256x32_Fotor.png')
    for i in range(img.shape[2]):
        img[:, :, i] = fix_image(img[:, :, i], 1, 3, 15, 30)

    return img

if __name__ == '__main__':
    img = test()


