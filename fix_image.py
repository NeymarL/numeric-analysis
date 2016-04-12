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
    N = (T + 1) / 2

    for i in range(ld, m - ld):
        for j in range(ld, n - ld):
            w = X[i - ld: i + ld + 1, j - ld: j + ld + 1]
            A = w.reshape(-1)
            A.sort()
            delta = A - X[i, j]
            omiga = delta[0:N].sum()
            kesai = 0
            if(X[i, j] <= A[u] or X[i, j] >= A[T - u + 1]):
                ita[i, j] = 1
                kesai = omiga / (T - 1)

            if kesai <= Q1:
                Lambda[i, j] = 0
            elif kesai > Q1 and kesai <= Q2:
                Lambda[i, j] = (kesai - Q1) * 1.0 / (Q2 - Q1)
            else:
                Lambda[i, j] = 1


            New[i, j] = (1 - Lambda[i, j]) * X[i, j] +\
                Lambda[i, j] * A[T / 2]

    print Lambda.sum()
    return 255 - New

'''
def add_gaussian(img):
    param = 30
    # 灰阶范围
    grayscale = 256
    w = img.shape[1]
    h = img.shape[0]
    newimg = np.zeros((h, w, 3), np.uint8)

    for x in xrange(0, h):
        for y in xrange(0, w, 2):
            r1 = np.random.random_sample()
            r2 = np.random.random_sample()
            z1 = param*np.cos(2*np.pi*r2)*np.sqrt((-2)*np.log(r1))
            z2 = param*np.sin(2*np.pi*r2)*np.sqrt((-2)*np.log(r1))

            newimg[x, y, 0] = fxy_val_0
            newimg[x, y, 1] = fxy_val_1
            newimg[x, y, 2] = fxy_val_2
            newimg[x, y+1, 0] = fxy1_val_0
            newimg[x, y+1, 1] = fxy1_val_1
            newimg[x, y+1, 2] = fxy1_val_2

    return newimg
'''

def test(ld = 1, u = 2, Q1 = 15, Q2 = 30):
    img = plt.imread('pic.jpg')

    #gaussian = add_gaussian(img)
    #plt.figure()
    #plt.imshow(gassian)
    new = np.zeros(img.shape)
    for i in range(img.shape[2]):
        new[:, :, i] = fix_image(img[:, :, i], ld, u, Q1, Q2)

    print (new - img).mean()

    return new

if __name__ == '__main__':
    img = test()

