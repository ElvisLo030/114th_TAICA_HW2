import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.animation import FuncAnimation

def visualize(loss_fn, paths_dict, centers, widths, amplitudes, field_size,
              title="Optimization Animation", filename="optimization.gif"):
    x_vals = np.linspace(field_size[0]*1.2, field_size[1]*1.2, 400)
    y_vals = np.linspace(field_size[0]*1.2, field_size[1]*1.2, 400)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = loss_fn(X, Y)
    max_index = np.unravel_index(np.argmax(Z), Z.shape)
    x_opt, y_opt = X[max_index], Y[max_index]
    z_opt = Z[max_index]

    fig, ax = plt.subplots(figsize=(10, 8))
    contour = ax.contourf(X, Y, Z, levels=40, cmap="plasma", alpha=0.85)
    ax.plot(x_opt, y_opt, 'c*', markersize=15,
            label=f"Global Max ({z_opt:.2f})")
    fig.colorbar(contour, ax=ax, label="Value")
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.set_xlim(field_size[0]*1.2, field_size[1]*1.2)
    ax.set_ylim(field_size[0]*1.2, field_size[1]*1.2)

    for i, ((cx, cy), w) in enumerate(zip(centers, widths)):
        planet, alpha = generate_cartoon_planet_patch(size=120, seed=i)
        extent = [cx - w, cx + w, cy - w, cy + w]
        ax.imshow(planet, extent=extent, origin="lower", alpha=alpha, zorder=10)
        ax.text(cx, cy, f"GPA {amplitudes[i]:.1f}",
                ha="center", va="center",
                color="white", fontsize=9, weight="bold", zorder=15)

    plots = {}
    max_len = 0
    for name, path in paths_dict.items():
        if isinstance(path[0][0], (list, tuple)) or isinstance(path[0], list):
            particle_plots = []
            for i, p in enumerate(path):
                ufo_parts = make_ufo(scale=0.3, seed=i)
                for part in ufo_parts:
                    ax.add_patch(part)
                line, = ax.plot([], [], "--", lw=1.0, alpha=0.7, zorder=12)
                particle_plots.append({"path": p, "ufo": ufo_parts, "line": line})
                max_len = max(max_len, len(p))
            plots[name] = particle_plots
        else:
            ufo_parts = make_ufo(scale=0.3, seed=0)
            for part in ufo_parts:
                ax.add_patch(part)
            line, = ax.plot([], [], "--", lw=1.0, alpha=0.7, zorder=12)
            plots[name] = {"path": path, "ufo": ufo_parts, "line": line}
            max_len = max(max_len, len(path))

    ax.legend(loc="upper right")

    text = ax.text(
        0.02, 0.95, "", transform=ax.transAxes,
        fontsize=12, verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.7, zorder=50)
    )

    def init():
        artists = []
        for entry in plots.values():
            if isinstance(entry, list):
                for p in entry:
                    p["line"].set_data([], [])
                    for part in p["ufo"]:
                        part.center = (0, 0)
                    artists.append(p["line"])
                    artists.extend(p["ufo"])
            else:
                entry["line"].set_data([], [])
                for part in entry["ufo"]:
                    part.center = (0, 0)
                artists.append(entry["line"])
                artists.extend(entry["ufo"])
        text.set_text("")
        return artists + [text]

    def update(frame):
        txt_lines = []
        artists = []
        for name, entry in plots.items():
            if isinstance(entry, list):
                best_val = -np.inf
                for p in entry:
                    path = p["path"]
                    if frame < len(path):
                        step = path[frame]
                    else:
                        step = path[-1]
                    x, y, val = step[0], step[1], step[2]
                    p["line"].set_data(*zip(*[(s[0], s[1]) for s in path[:frame+1]]))
                    body, dome = p["ufo"]
                    body.center = (x, y)
                    dome.center = (x, y + 0.35*0.3)
                    artists.append(p["line"])
                    artists += [body, dome]
                    best_val = max(best_val, val)
                txt_lines.append(f"{name}: {best_val:.2f}")
            else:
                path = entry["path"]
                if frame < len(path):
                    step = path[frame]
                else:
                    step = path[-1]
                if len(step) == 3:
                    x, y, val = step
                else:
                    x, y = step
                    val = loss_fn(x, y)
                entry["line"].set_data(*zip(*[(s[0], s[1]) if len(s) == 3 else s for s in path[:frame+1]]))
                body, dome = entry["ufo"]
                body.center = (x, y)
                dome.center = (x, y + 0.35*0.3)
                artists.append(entry["line"])
                artists += [body, dome]
                txt_lines.append(f"{name}: {val:.2f}")
        text.set_text("\n".join(txt_lines))
        return artists + [text]

    ani = FuncAnimation(fig, update, frames=max_len, init_func=init,
                        blit=True, interval=200, repeat=False)

    ani.save(filename, writer="pillow", fps=2)
    print(f"Animation saved as {filename}")
    plt.close(fig)
    
def random_color(bright=True):
    hue = np.random.rand()
    sat = 0.6 if bright else 0.4
    val = 0.9 if bright else 0.7
    return colors.hsv_to_rgb([hue, sat, val])

def make_ufo(scale=0.4, seed=None):
    if seed is not None:
        np.random.seed(seed)
    body_color = random_color()
    dome_color = random_color()

    body = Ellipse((0, 0), width=2*scale, height=1*scale,
                   facecolor=body_color, edgecolor="white",
                   linewidth=0.6, zorder=30)
    
    dome = Ellipse((0, 0.2*scale), width=1.5*scale, height=0.7*scale,
                   facecolor="lightblue", edgecolor="white",
                   linewidth=0.5, zorder=31)
    return [body, dome]

def generate_cartoon_planet_patch(size=100, seed=0, edge_jitter=0.15):
    from scipy.ndimage import gaussian_filter
    np.random.seed(seed)
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)

    noise = gaussian_filter(np.random.rand(size, size), sigma=8)
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    radial_offset = 1 + (noise - 0.5) * edge_jitter
    irregular_mask = R <= radial_offset

    base_noise = np.random.rand(size, size)
    smooth_noise = gaussian_filter(base_noise, sigma=12)
    smooth_noise = (smooth_noise - smooth_noise.min()) / (smooth_noise.max() - smooth_noise.min())

    hue1 = np.random.rand()
    hue2 = (hue1 + np.random.uniform(0.33, 0.66)) % 1.0
    sat, val = 0.7, 0.85
    color1 = colors.hsv_to_rgb([hue1, sat, val])
    color2 = colors.hsv_to_rgb([hue2, sat, val])

    planet = np.zeros((size, size, 3))
    planet[smooth_noise >= 0.5] = color1
    planet[smooth_noise < 0.5] = color2

    alpha = irregular_mask.astype(float)
    return planet, alpha