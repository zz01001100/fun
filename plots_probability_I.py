import seaborn as sns
import matplotlib.pyplot as plt

sns.__version__ # check version, need 0.11.0 or greater
penguins = sns.load_dataset("penguins")

# Use JointGrid directly to draw a custom plot
g = sns.JointGrid(data=penguins, x="bill_length_mm", y="bill_depth_mm", space=0, ratio=15)
g.plot_joint(sns.scatterplot,  alpha=.6, legend=False)
g.plot_marginals(sns.rugplot, height=1,  alpha=.6)
sns.displot(data=penguins, x="bill_length_mm", kind="hist")
sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm", kind="hist")
sns.pairplot(penguins, kind="kde")
sns.pairplot(penguins, hue="species");

plt.show()