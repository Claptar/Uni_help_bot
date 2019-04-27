import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


dataset = pd.read_excel('data.xlsx', header=None)
dataset.head()
d = np.array(dataset)
x = d[:, 0]
y = d[:, 1]
plt.plot(x, y, 'ro')
plt.show()
