---
title: "模拟信号的采样过程"
date: "2024-01-06" # 格式为 YYYY-MM-DD
categories: DmZi
tags:
  - 探究报告
  - 实践
  - 手册
summary: "模拟信号采样得到序列信号的行为分析"
author: "KhVeMx"
---

# 模拟信号的采样过程

## 模拟信号采样得到序列

本文只考虑单频正弦信号的分析，
$$
x(t) = A\cos(2\pi f_a t+\varphi) = A\cos(\omega_at+\varphi)
$$

其中下标$(_a)$代表是模拟量。

模拟信号等时间间距采样生成序列：
$$
\begin{aligned}
    x[n] = x(nT_s) &= A\cos(2\pi f_a T_s n+\varphi) \\
    &= A\cos(\Omega n +\varphi)
\end{aligned}
$$

得到关系
$$
\Omega = 2\pi f_a T_s\ = \omega_a T_s , \ f_a = \frac{\Omega}{2\pi} \cdot f_s
$$

其中序列角频率$\Omega$、模拟频率$f_a$、采样间隔$T_s$、采样频率$f_s$

上式可以快速的记忆为**序列角频率所代表的实际模拟频率与采样频率成正比；采样频率越高，序列角频率表示的模拟频率越大。**

<br></br>

## 混叠与信息丢失

不同频率的$f_a$是否可能对应相同的$\Omega$呢。作下式
$$
x_1(t) = A\cos \left[ 2\pi (f_a + \Delta f_a) t + \varphi \right]
$$

对其采样
$$
\begin{aligned}
    x_1[n] &= A\cos \left[ 2\pi (f_a + \Delta f_a) T_s n + \varphi \right] \\
    &= A\cos ( \Omega n + 2\pi \Delta f_a T_s n + \varphi )
\end{aligned}
$$

只要
$$
2\pi \Delta f_a T_s n = k\cdot 2\pi n, \ k\in \mathbb{Z}
$$
$$
\Delta f_a T_s = k, \ \Delta f_a = kf_s, \ k\in \mathbb{Z}
$$

显然，和原始模拟频率相差采样频率间隔的模拟信号，也会给相同序列圆频率$\Omega$贡献成分。

这来自于序列频率的周期性
$$
\Delta\Omega = k \cdot 2\pi
$$

我们现在有这样的信念：采样得到的序列的频率并不与实际的频率一一对应，而是一系列等间距频率成分的总和，间距是采样频率。以上的结论在数字信号处理中被处理为：`时域采样定理`
$$
X_d(e^{j\Omega}) = \frac{1}{T_s} \sum_k X_a\left(j(\omega_a+k\omega_s) \right)
$$

<br></br>

## 采样定理与抗混叠

系列角频率的周期性，是以$2\pi$为周期。所以可以关注区间$[-\pi, \pi]$，并且可知$[\pi,2\pi]$中的行为与$[-\pi,0]$完全相同。


因为三角函数是可分解为正负两个频率，所以实际上对于现实信号频率$f_a$只有在$\displaystyle \Omega = \frac{2\pi f_a}{f_s}\in[0,\pi]$中才有可能一一对应。

当$f_a = f_s$时，$\Omega = 2\pi$。当$f_a = f_s/2$时，$\Omega = \pi$。

所以就要求了，当信号所有的频率成分只存在于一半采样频率之内时，其中的模拟信号频率与序列的圆频率一一对应。

即
$$
X_a\left(j(\omega_a+k\omega_s) \right) = 0, \ k \not ={0}, \ k \in \mathbb{Z}
$$

<br></br>

## 仿真验证

``` python
import numpy as np
import matplotlib.pyplot as plt

def x(t, f_a):
    return np.sin(2 * np.pi * f_a * t)
```

定义一个可调频率$f_a$的正弦三角模拟信号。

``` python
def samplePlot(T, f_a):
    n = np.arange(0, 101, 1)
    X = x(n * T , f_a)
    plt.figure()
    plt.plot(n, X)
    plt.title('x[n] with f = ' + str(f_a) + '  T = ' + str(T))
    plt.xlabel('n')

def wavePlot(dt, f_a):
    t = np.arange(0, 1, dt)
    X = x(t, f_a)
    plt.figure()
    plt.plot(t, X)
    plt.title('x(t) with f = ' + str(f_a))
    plt.xlabel('t')
```

定义采样函数和模拟波形展示函数。采样函数需要输入采样时间间隔。

``` python
samplePlot(0.01, 2)
samplePlot(0.01, 98)
samplePlot(0.01, 102)
samplePlot(0.01, 198)

# wavePlot(0.0001, 2)
# wavePlot(0.0001, 98)
# wavePlot(0.0001, 102)
# wavePlot(0.0001, 198)

plt.show()
```

然后画出2、100-2、2+100、100-2+100频率的正弦信号在100Hz的采样率下得到的序列。

![](./picture/blog/DmZi_模拟信号的采样过程_1.png)

![](./picture/blog/DmZi_模拟信号的采样过程_2.png)

![](./picture/blog/DmZi_模拟信号的采样过程_3.png)

![](./picture/blog/DmZi_模拟信号的采样过程_4.png)


从上图可以看出如下的事实：

> 102Hz 与 2Hz 最终采样得到的序列相同

> 98Hz 与 198Hz 最终采样得到的序列相同

> 98Hz 理论上与 -2Hz 采样结果相同，既与2Hz序列**相位相反**

从而验证了本专题的所有理论
