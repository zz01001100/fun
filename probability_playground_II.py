
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from scipy.stats import multivariate_normal, norm

# ============================================================
# STATISTIK 3 LAB
# Joint distributions | Marginals | Conditionals | Dependence
# ============================================================

plt.rcParams["figure.figsize"] = (13, 8)
fig = plt.figure()
fig.suptitle("Statistik 3 | Bivariate Distribution Laboratory",
             fontsize=16)

# Main plots
ax_joint = fig.add_axes([0.07, 0.34, 0.42, 0.49])
ax_marg = fig.add_axes([0.54, 0.59, 0.18, 0.24])
ax_cond = fig.add_axes([0.76, 0.59, 0.19, 0.24])
ax_sample = fig.add_axes([0.54, 0.34, 0.41, 0.19])
ax_info = fig.add_axes([0.54, 0.04, 0.41, 0.24])
ax_info.axis("off")

# Scenario selector
ax_mode = fig.add_axes([0.07, 0.05, 0.19, 0.22])
ax_mode.set_title("Distribution / experiment", fontsize=10)

modes = [
    "Normal: vary rho",
    "Independent discrete",
    "Dependent, Cov = 0",
    "Draw without replacement",
    "Independent continuous",
]
radio = RadioButtons(ax_mode, modes, active=0)
for label in radio.labels:
    label.set_fontsize(8)

# Parameter sliders
slider_specs = [
    ("mux", "mu X", -2, 2, 0),
    ("muy", "mu Y", -2, 2, 0),
    ("sx", "SD X", 0.3, 2, 1),
    ("sy", "SD Y", 0.3, 2, 1),
    ("rho", "rho", -0.98, 0.98, 0.6),
    ("x0", "Condition x0", -2, 2, 0.8),
    ("y0", "Condition y0", -2, 2, 1),
]

sliders = {}
for i, (key, label, lo, hi, initial) in enumerate(slider_specs):
    a = fig.add_axes([0.30, 0.245 - i * 0.029, 0.19, 0.015])
    sliders[key] = Slider(a, label, lo, hi, valinit=initial)
    sliders[key].label.set_fontsize(8)
    sliders[key].valtext.set_fontsize(8)


def discrete_stats(x, y, P):
    """Exact population moments from a joint probability mass matrix."""
    px = P.sum(axis=1)
    py = P.sum(axis=0)

    ex = np.sum(x * px)
    ey = np.sum(y * py)
    ex2 = np.sum(x**2 * px)
    ey2 = np.sum(y**2 * py)
    exy = np.sum(P * np.outer(x, y))

    vx = ex2 - ex**2
    vy = ey2 - ey**2
    cov = exy - ex * ey
    rho = cov / np.sqrt(vx * vy) if vx * vy > 0 else np.nan

    return px, py, ex, ey, vx, vy, cov, rho


def update(_=None):
    mode = radio.value_selected

    ax_joint.clear()
    ax_marg.clear()
    ax_cond.clear()
    ax_sample.clear()
    ax_info.clear()
    ax_info.axis("off")

    mux = sliders["mux"].val
    muy = sliders["muy"].val
    sx = sliders["sx"].val
    sy = sliders["sy"].val
    rho = sliders["rho"].val
    x0 = sliders["x0"].val
    y0 = sliders["y0"].val

    # --------------------------------------------------------
    # A. CONTINUOUS BIVARIATE NORMAL
    # --------------------------------------------------------
    if mode in ["Normal: vary rho", "Independent continuous"]:
        r = 0 if mode == "Independent continuous" else rho

        cov = np.array([
            [sx**2, r*sx*sy],
            [r*sx*sy, sy**2]
        ])
        rv = multivariate_normal([mux, muy], cov)

        xs = np.linspace(mux - 3.5*sx, mux + 3.5*sx, 180)
        ys = np.linspace(muy - 3.5*sy, muy + 3.5*sy, 180)
        X, Y = np.meshgrid(xs, ys)
        Z = rv.pdf(np.dstack((X, Y)))

        px = norm.pdf(xs, mux, sx)
        py = norm.pdf(ys, muy, sy)

        # Conditional distributions
        cx = mux + r*sx/sy*(y0-muy)
        cy = muy + r*sy/sx*(x0-mux)
        csx = sx*np.sqrt(1-r**2)
        csy = sy*np.sqrt(1-r**2)

        ax_joint.contourf(X, Y, Z, levels=20, cmap="viridis")
        ax_joint.contour(X, Y, Z, levels=8, colors="white",
                         linewidths=0.5)
        ax_joint.axvline(x0, color="orange", ls="--")
        ax_joint.axhline(y0, color="magenta", ls="--")
        ax_joint.set_title("Joint density f(x,y)")
        ax_joint.set_xlabel("X")
        ax_joint.set_ylabel("Y")

        ax_marg.plot(xs, px, color="black", label="Marginal X")
        ax_marg.plot(ys, py, color="crimson", ls="--",
                     label="Marginal Y")
        ax_marg.set_title("Marginal densities", fontsize=9)
        ax_marg.legend(fontsize=7)

        ax_cond.plot(xs, norm.pdf(xs, cx, csx),
                     label="f(X | Y=y0)")
        ax_cond.plot(xs, px, "k--", label="f(X)")
        ax_cond.set_title("Conditional vs marginal X", fontsize=9)
        ax_cond.legend(fontsize=7)

        ax_sample.axis("off")
        ax_sample.text(
            0, 0.95,
            "THEORETICAL DISTRIBUTION\n"
            "No observations are being sampled.\n"
            f"Condition Y = {y0:.2f}: E[X|Y] = {cx:.3f}\n"
            f"Var(X|Y) = {csx**2:.3f}\n"
            f"Condition X = {x0:.2f}: E[Y|X] = {cy:.3f}\n"
            f"Var(Y|X) = {csy**2:.3f}",
            va="top", fontsize=9, family="monospace"
        )

        independent = np.isclose(r, 0)
        info = (
            f"E[X] = {mux:.3f}   E[Y] = {muy:.3f}\n"
            f"Var(X) = {sx**2:.3f}   Var(Y) = {sy**2:.3f}\n"
            f"Cov(X,Y) = {r*sx*sy:.3f}\n"
            f"Corr(X,Y) = {r:.3f}\n"
            f"Independent: {independent}\n\n"
            "For a bivariate normal, rho = 0 iff independent."
        )

    # --------------------------------------------------------
    # B. DISCRETE JOINT DISTRIBUTIONS
    # --------------------------------------------------------
    else:
        if mode == "Independent discrete":
            x = np.array([1, 2, 3])
            y = np.array([1, 2, 3])
            px0 = np.array([0.2, 0.5, 0.3])
            py0 = np.array([0.25, 0.5, 0.25])
            P = np.outer(px0, py0)

        elif mode == "Dependent, Cov = 0":
            # Y = 0 when X = 0; Y = 1 when X = +/-1.
            # Cov(X,Y) = 0, but X and Y are dependent.
            x = np.array([-1, 0, 1])
            y = np.array([0, 1])
            P = np.array([
                [0.25, 0.00],
                [0.50, 0.00],
                [0.00, 0.25],
            ])

        else:
            # First and second draws from {1,...,5}, without replacement
            x = np.arange(1, 6)
            y = np.arange(1, 6)
            P = np.ones((5, 5)) / 20
            np.fill_diagonal(P, 0)

        px, py, ex, ey, vx, vy, cov, r = discrete_stats(x, y, P)

        # Joint probability mass function
        im = ax_joint.imshow(P.T, origin="lower", aspect="auto",
                             cmap="viridis")
        ax_joint.set_xticks(range(len(x)), x)
        ax_joint.set_yticks(range(len(y)), y)
        ax_joint.set_xlabel("X")
        ax_joint.set_ylabel("Y")
        ax_joint.set_title("Joint mass function p(x,y)")
        for i in range(len(x)):
            for j in range(len(y)):
                ax_joint.text(i, j, f"{P[i,j]:.2f}",
                              ha="center", va="center",
                              color="white" if P[i,j] < 0.35 else "black",
                              fontsize=9)

        ax_marg.bar(x, px, alpha=0.8, label="pX")
        ax_marg.set_title("Marginal pX(x)", fontsize=9)
        ax_marg.set_xticks(x)

        # Conditional distribution X | Y = selected y
        j = int(np.argmin(abs(y - y0)))
        if py[j] > 0:
            conditional = P[:, j] / py[j]
        else:
            conditional = np.zeros(len(x))

        ax_cond.bar(x, conditional, alpha=0.8, label="p(X | Y)")
        ax_cond.set_title(f"Conditional X | Y={y[j]}", fontsize=9)
        ax_cond.set_xticks(x)
        ax_cond.set_ylim(0, 1.05)

        # Show empirical sample from the joint distribution
        rng = np.random.default_rng(42)
        pairs = [(x[i], y[j]) for i in range(len(x))
                 for j in range(len(y)) if P[i, j] > 0]
        probs = np.array([P[i, j] for i in range(len(x))
                          for j in range(len(y)) if P[i, j] > 0])
        sample_ids = rng.choice(len(pairs), size=250, p=probs)
        sample = np.array([pairs[k] for k in sample_ids])

        ax_sample.scatter(sample[:, 0], sample[:, 1],
                          alpha=0.25, s=12)
        ax_sample.set_title("250 simulated pairs (sample)", fontsize=9)
        ax_sample.set_xlabel("X")
        ax_sample.set_ylabel("Y")
        ax_sample.grid(alpha=0.2)

        independent = np.allclose(P, np.outer(px, py))
        info = (
            f"E[X] = {ex:.3f}   E[Y] = {ey:.3f}\n"
            f"Var(X) = {vx:.3f}   Var(Y) = {vy:.3f}\n"
            f"Cov(X,Y) = {cov:.3f}\n"
            f"Corr(X,Y) = {r:.3f}\n"
            f"Independent: {independent}\n\n"
            "Independence test: p(x,y) = pX(x) * pY(y)\n"
            "Zero covariance alone does not prove independence."
        )

    ax_info.text(0, 1, info, va="top", fontsize=10,
                 family="monospace")
    fig.canvas.draw_idle()


radio.on_clicked(update)
for s in sliders.values():
    s.on_changed(update)

update()
plt.show()
