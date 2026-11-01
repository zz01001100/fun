import numpy as np
import matplotlib.pyplot as plt

# Define Parameters
start_price = 100
n_days = 1825
price_path = np.array([start_price])

# Simulate random walk
for i in range(n_days):
    single_num = np.random.choice([1, -1])
    random_walk = price_path[-1] + single_num
    price_path = np.append(price_path, random_walk)

# Plot results
plt.plot(price_path)
plt.title('A Random Walk')
plt.xlabel('Time Period')
plt.ylabel('Price')
plt.show()

# 4. Define random walk as a function

def simulate_walk(start_price, n_days):
    price_path = np.array([start_price])
    for i in range(n_days):
        single_num = np.random.choice([1, -1])
        random_walk = price_path[-1] + single_num
        price_path = np.append(price_path, random_walk)
    return price_path

# 5. Simulate 10 independent paths and plot them

simulations = []

for i in range(10):
    result = simulate_walk(start_price, n_days)
    simulations.append(result)

# Plot all 10 paths on one chart
for i in simulations:
    plt.plot(i)

plt.title("10 Random Walks")
plt.xlabel("Time Period")
plt.ylabel("Price")
plt.show()

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)

ax0.plot(simulations[0])
ax0.set_title("Simulation 1")
ax0.set_xlabel("Time Period")
ax0.set_ylabel("Price")

ax1.plot(simulations[1])
ax1.set_title("Simulation 2")
ax1.set_xlabel("Time Period")
ax1.set_ylabel("Price")

ax2.plot(simulations[2])
ax2.set_title("Simulation 3")
ax2.set_xlabel("Time Period")
ax2.set_ylabel("Price")

ax3.plot(simulations[3])
ax3.set_title("Simulation 4")
ax3.set_xlabel("Time Period")
ax3.set_ylabel("Price")

fig.suptitle("Random Walk Simulations")

plt.tight_layout()
plt.show()

# 6. Calculate the weight of paths that finish above the starting price.
proportion = sum(path[-1] > 100 for path in simulations) / len(simulations)
print(proportion)