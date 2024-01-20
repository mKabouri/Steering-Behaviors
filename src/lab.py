import numpy as np

L = (5, 7)
length = np.linalg.norm(L, ord=2)
print(np.linalg.norm(L/length, ord=1))
