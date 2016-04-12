#! /usr/bin/env python
# -*- coding:utf-8 -*-
# lagrange.py
# 实现拉格朗日插值，并应用解题

import numpy as np

def lagrange(X, Y, x):
    '''
    X 是一个list， 包含全部的 x0, x1, .. xn
    Y 是一个list， 包含全部的 y0, y1, .. yn
    x 是待求点的横坐标

    return y 待求点的值（纵坐标）
    '''
    y = 0
    n = len(X)
    for i in range(n):
        l = 1.0
        for j in range(n):
            if j != i:
                l *= (x - X[j]) / (X[i] - X[j])
        y += Y[i] * l

    return y


def test(n = 10):
    '''
    对[-5,5]作等距分划xi=-5+ih,h=10/n,i=0,1,...,n,
    并对Runge给出的函数 y = 1 / (1 + x * x)
    作Lagrange插值, 取n=10,20.
    计算插值多项式 Pn(x) 在 x=4.8处的误差,并作分析。
    '''
    print 'n = %d 时' % n
    h = 10.0 / n
    X = np.arange(-5, 5, h).tolist()
    X.append(5)
    Y = [(1.0 / (1 + x * x)) for x in X]

    x = 4.8

    right = 1.0 / (1 + x * x)
    l = lagrange(X, Y, x)

    error = l - right
    if error < 0:
        error = -error

    print 'Lagrange 插值结果为', l
    print '精确结果为 ', right
    print '绝对误差为 ', error


if __name__ == '__main__':
    test(10)
    test(20)

