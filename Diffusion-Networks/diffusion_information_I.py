# SETUP ----------------------------------------------------------------
import networkx as nx
import matplotlib.pyplot as plt
import random

N, P, STEPS, RUNS = 100, 0.25, 20, 30
random.seed(42)

# NETWORKS -------------------------------------------------------------
networks = [
    nx.erdos_renyi_graph(N, 0.05, seed=42),
    nx.barabasi_albert_graph(N, 3, seed=42)
]
names = ["Random network", "Highly connected nodes"]

# SHOW NETWORKS --------------------------------------------------------
plt.figure(figsize=(10, 4))
for i in range(2):
    plt.subplot(1, 2, i + 1)
    nx.draw(networks[i], node_size=15, node_color="black")
    plt.title(names[i])
plt.show()

# SIMULATE INFORMATION SPREAD ------------------------------------------
results, times = [[], []], [[], []]

for run in range(RUNS):
    for i in range(2):
        informed = {min(networks[i], key=networks[i].degree)} # Diese Zeile bestimmt den Startknoten, also die Person, die die Information zuerst erhält:
        history = [1 / N]

        for step in range(STEPS):
            new = set(informed)
            for person in informed:
                for neighbor in networks[i].neighbors(person):
                    if neighbor not in informed and random.random() < P:
                        new.add(neighbor)
            informed = new
            history.append(len(informed) / N)

        results[i].append(history)
        reached = [t for t, share in enumerate(history) if share >= 0.5]
        if reached:
            times[i].append(reached[0])

# AVERAGE AND PLOT -----------------------------------------------------
for i in range(2):
    average = [sum(run[t] for run in results[i]) / RUNS
               for t in range(STEPS + 1)]
    plt.plot(average, label=names[i])

plt.xlabel("Time step")
plt.ylabel("Share informed")
plt.title("Information diffusion (30 simulations)")
plt.legend()
plt.grid()
plt.show()

# RESULTS --------------------------------------------------------------
for i in range(2):
    print(names[i])
    print("Reached 50%:", len(times[i]), "of", RUNS)
    if times[i]:
        print("Average time to 50%:", round(sum(times[i]) / len(times[i]), 2))
