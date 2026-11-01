
# SETUP
import networkx as nx
import matplotlib.pyplot as plt
import random

N, GROUPS, P, STEPS, RUNS = 100, 4, 0.25, 50, 30
random.seed(42)

# ONE NETWORK WITH FOUR SUBNETWORKS
network = nx.planted_partition_graph(GROUPS, N // GROUPS, 0.3, 0.01, seed=42)
group_size = N // GROUPS
groups = [list(range(i * group_size, (i + 1) * group_size)) for i in range(GROUPS)]

nx.draw(network, node_color=[node // group_size for node in network],
        node_size=25, cmap=plt.cm.Set1)
plt.show()


# INFORMATION SPREAD
P_BETWEEN = 0.01  # Probability of transmitting between groups
P_WITHIN = 0.25   # Probability of transmitting within a group

results = []

for run in range(RUNS):
    informed = {0}
    history = [[] for _ in range(GROUPS)]

    for step in range(STEPS + 1):
        for i, group in enumerate(groups):
            history[i].append(len(informed.intersection(group)) / len(group))

        new = set(informed)

        for person in informed:
            for neighbor in network.neighbors(person):
                if neighbor not in informed:
                    same_group = person // group_size == neighbor // group_size
                    p = P_WITHIN if same_group else P_BETWEEN

                    if random.random() < p:
                        new.add(neighbor)

        informed = new

    results.append(history)


# AVERAGE SHARE INFORMED IN EACH SUBNETWORK
for i in range(GROUPS):
    average = [
        sum(run[i][t] for run in results) / RUNS
        for t in range(STEPS + 1)
    ]
    plt.plot(average, label=f"Subnet {i + 1}")

plt.xlabel("Time step")
plt.ylabel("Share informed within subnet")
plt.title("Information spread by subnetwork")
plt.legend()
plt.grid()
plt.ylim(0, 1)
plt.show()
