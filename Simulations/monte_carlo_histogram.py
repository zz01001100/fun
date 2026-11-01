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
plt.hist(numbers, bins=30, weights=weights)
plt.title('Normal distribution')
plt.xlabel('Observation')
plt.ylabel('Probability')
plt.show()