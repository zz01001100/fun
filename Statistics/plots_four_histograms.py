"""
File: pplots_four_histograms.py
-------------------
Putting multiple histograms in the same container and computing some location- and dispersion parameters.
"""

import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng(seed=42)

numbers = rng.normal(0, 1, size=1000)
weights = np.ones_like(numbers) / len(numbers)


print(numbers.mean())
print(numbers.std())
print(numbers.var())

proportion = np.mean(numbers > 1)
print(proportion)

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)
ax0.hist(numbers, bins=10, weights=weights)
ax1.hist(numbers, bins=20, weights=weights)
ax2.hist(numbers, bins=30, weights=weights)
ax3.hist(numbers, bins=40, weights=weights)
plt.show()