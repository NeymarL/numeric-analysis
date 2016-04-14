#! /usr/bin/env python
# -*- coding:utf-8 -*-
# fix_image.py
# 图像修复、降噪


import numpy as np
import matplotlib.pylab as plt
import random as rd


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
    (m, n) = X.shape
    T = (2 * ld + 1) * (2 * ld + 1)
    N = (T + 1) / 2

    for i in range(ld, m - ld):
        for j in range(ld, n - ld):
            w = X[i - ld: i + ld + 1, j - ld: j + ld + 1].copy()
            A = w.reshape(-1)
            A.sort()
            delta = A - X[i, j]
            omiga = delta[0:N].sum()
            kesai = 0

            if(X[i, j] <= A[u] or X[i, j] >= A[T - u + 1]):
                ita[i, j] = 1
                kesai = omiga * 1.0 / (N - 1)
                #print kesai

            if kesai < 0:
                kesai = -kesai

            if kesai <= Q1:
                Lambda[i, j] = 0
            elif kesai > Q1 and kesai <= Q2:
                Lambda[i, j] = (kesai - Q1) * 1.0 / (Q2 - Q1)
            else:
                Lambda[i, j] = 1


            X[i, j] = (1 - Lambda[i, j]) * X[i, j] +\
                Lambda[i, j] * A[(T - 4) / 2]

            '''
            if i == 162 and j == 44:
                print Lambda[i, j], '\t', w, '\n', A[T / 2]
                print 'omiga = ', omiga, '\t', 'kesai = ', kesai
                print 'A[T - u + 1] = ', A[T - u + 1]
                print 'X[i,j] = ', X[i, j]
            '''

    #print Lambda.sum()
    return X

def generate_random_file_name():
    filename = ''
    for i in range(5):
        filename += str(rd.randint(0, 9))

    return filename


def run_fix(ld = 2, u = 8, Q1 = 0.05, Q2 = 0.1, img = ''):
    if not img:
        img = plt.imread('test/Sublime_text.png')
    else:
        img = plt.imread(img)

    if img.max() >= 200:
        img /= 255.0

    #plt.figure()
    #plt.imshow(img)

    #plt.figure()
    new = np.zeros(img.shape)
    for i in range(img.shape[2]):
        new[:, :, i] = fix_image(img[:, :, i], ld, u, Q1, Q2)

    #plt.imshow(new)
    filename = generate_random_file_name()
    plt.imsave('static/temp/' + filename, new)
    return 'static/temp/' + filename

if __name__ == '__main__':
    img = run()

