import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng(seed=42)

numbers = rng.normal(0, 1, size=1000)
weights = np.ones_like(numbers) / len(numbers) # This is the only line I don't understand yet.


print(numbers.mean())
print(numbers.std())
print(numbers.var())

proportion = np.mean(numbers > 1)
print(proportion)

import matplotlib.pyplot as plt

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)
ax0.hist(numbers, bins=10, weights=weights)
ax1.hist(numbers, bins=20, weights=weights)
ax2.hist(numbers, bins=30, weights=weights)
ax3.hist(numbers, bins=40, weights=weights)
plt.show()