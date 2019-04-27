import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


dataset = pd.read_excel('data.xlsx', header=None)
dataset.head()
d = np.array(dataset)
x = d[:, 0]
y = d[:, 1]

av_x = np.sum(x)/len(x)
av_y = np.sum(y)/len(y)

sigmas_x = np.sum(x*x)/len(x) - (np.sum(x)/len(x))**2
sigmas_y = np.sum(y*y)/len(y) - (np.sum(y)/len(y))**2
R = np.sum(x*y)/len(x) - av_x*av_y
a = R/sigmas_x
b = av_y - a*av_x
d_a = 2*math.sqrt((sigmas_y/sigmas_x - a**2)/(len(x)-2))
d_b = d_a*math.sqrt(sigmas_x + av_x**2)
x_ = range(0, x[len(x) -1]//1 + 2)
plt.plot(x, y, 'ro', x_, a*x_ + b)
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.grid(True)
plt.show()