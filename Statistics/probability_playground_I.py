
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.stats import multivariate_normal, norm

# Initial parameters
mu_x, mu_y = 0.1, -0.2
sigma_x, sigma_y = 0.3**0.5, 1.0
rho = 0.7
x0, y0 = 0.7, 1.5

fig = plt.figure(figsize=(12, 8))
fig.suptitle("Bivariate Distribution Playground")

ax = fig.add_axes([0.08, 0.30, 0.48, 0.55])
ax_top = fig.add_axes([0.08, 0.76, 0.48, 0.12], sharex=ax)
ax_right = fig.add_axes([0.58, 0.30, 0.12, 0.55], sharey=ax)
ax_cx = fig.add_axes([0.75, 0.58, 0.21, 0.25])
ax_cy = fig.add_axes([0.75, 0.29, 0.21, 0.25])
ax_info = fig.add_axes([0.58, 0.04, 0.39, 0.18])
ax_info.axis("off")

# Sliders
slider_specs = [
    ("mux", "mu X", -2, 2, mu_x),
    ("muy", "mu Y", -2, 2, mu_y),
    ("sx", "SD X", 0.2, 2, sigma_x),
    ("sy", "SD Y", 0.2, 2, sigma_y),
    ("rho", "Correlation", -0.98, 0.98, rho),
    ("x0", "Condition x0", -3, 3, x0),
    ("y0", "Condition y0", -3, 3, y0),
]

sliders = {}
for i, (key, label, lo, hi, initial) in enumerate(slider_specs):
    a = fig.add_axes([0.12, 0.235 - i * 0.029, 0.35, 0.015])
    sliders[key] = Slider(a, label, lo, hi, valinit=initial)

def update(_=None):
    mux = sliders["mux"].val
    muy = sliders["muy"].val
    sx = sliders["sx"].val
    sy = sliders["sy"].val
    r = sliders["rho"].val
    x0 = sliders["x0"].val
    y0 = sliders["y0"].val

    cov_xy = r * sx * sy
    cov = np.array([
        [sx**2, cov_xy],
        [cov_xy, sy**2]
    ])

    distribution = multivariate_normal(
        mean=[mux, muy], cov=cov
    )

    xs = np.linspace(mux - 4*sx - 1, mux + 4*sx + 1, 180)
    ys = np.linspace(muy - 4*sy - 1, muy + 4*sy + 1, 180)
    X, Y = np.meshgrid(xs, ys)
    Z = distribution.pdf(np.dstack((X, Y)))

    px = norm.pdf(xs, mux, sx)
    py = norm.pdf(ys, muy, sy)

    # Conditional distributions
    cx_mean = mux + r * sx/sy * (y0 - muy)
    cx_sd = sx * np.sqrt(1-r**2)

    cy_mean = muy + r * sy/sx * (x0 - mux)
    cy_sd = sy * np.sqrt(1-r**2)

    # Joint density
    ax.clear()
    ax.contourf(X, Y, Z, levels=20, cmap="viridis")
    ax.contour(X, Y, Z, levels=10, colors="white",
               linewidths=0.5)
    ax.axvline(x0, color="orange", linestyle="--")
    ax.axhline(y0, color="magenta", linestyle="--")
    ax.set(xlabel="X", ylabel="Y", title="Joint density")

    # Marginal densities
    ax_top.clear()
    ax_top.plot(xs, px, color="black")
    ax_top.set_title("Marginal density of X", fontsize=9)

    ax_right.clear()
    ax_right.plot(py, ys, color="red")
    ax_right.set_title("Marginal Y", fontsize=9)

    # Conditional X | Y=y0 versus marginal X
    ax_cx.clear()
    ax_cx.plot(xs, norm.pdf(xs, cx_mean, cx_sd),
               label="Conditional X | Y=y0")
    ax_cx.plot(xs, px, "k--", label="Marginal X")
    ax_cx.set_title("Conditional vs marginal X", fontsize=9)
    ax_cx.legend(fontsize=7)

    # Conditional Y | X=x0 versus marginal Y
    ax_cy.clear()
    ax_cy.plot(ys, norm.pdf(ys, cy_mean, cy_sd),
               label="Conditional Y | X=x0")
    ax_cy.plot(ys, py, "r--", label="Marginal Y")
    ax_cy.set_title("Conditional vs marginal Y", fontsize=9)
    ax_cy.legend(fontsize=7)

    info = (
        f"E[X] = {mux:.3f}     E[Y] = {muy:.3f}\n"
        f"Var(X) = {sx**2:.3f}   Var(Y) = {sy**2:.3f}\n"
        f"Cov(X,Y) = {cov_xy:.3f}   Corr(X,Y) = {r:.3f}\n"
        f"E[X | Y={y0:.2f}] = {cx_mean:.3f}\n"
        f"Var(X | Y) = {cx_sd**2:.3f}\n"
        f"E[Y | X={x0:.2f}] = {cy_mean:.3f}\n"
        f"Var(Y | X) = {cy_sd**2:.3f}\n"
        f"Independent? {'YES' if abs(r) < 1e-6 else 'NO'}"
    )
    ax_info.clear()
    ax_info.axis("off")
    ax_info.text(0, 1, info, va="top", family="monospace")

    fig.canvas.draw_idle()

for slider in sliders.values():
    slider.on_changed(update)

update()
plt.show()
