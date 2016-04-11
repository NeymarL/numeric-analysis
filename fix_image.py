#! /usr/bin/env python
# -*- coding:utf-8 -*-
# fix_image.py
# 图像修复、降噪

#from scipy import signal
import numpy as np
import matplotlib.pylab as plt

def compute_ita(X, ld = 1, u):
    '''
    计算每个点的噪声参数ita
    '''
    ita = np.zeros(X.shape)
    (m, n) = X.shape
    T = (2 * ld + 1) ^ 2

    for i in range(ld, m - ld + 1):
        for j in range(ld, n - ld + 1):
            w = X[i - ld : i + ld + 1, j - ld : j + ld + 1]
            A = w.reshape(-1).sort()
            if(X[i,j] <= A[u] or X[i,j] >= A[T - u + 1]):
                ita[i, j] = 1

    return ita