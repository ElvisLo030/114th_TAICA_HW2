import numpy as np

def generate_circular_surface(num_bumps=8, min_dist=5.0,
                              domain=(-8, 8), start_point=None):
    centers, widths = [], []
    attempts = 0
    max_attempts = num_bumps * 200  

    while len(centers) < num_bumps and attempts < max_attempts:
        attempts += 1
        candidate = np.random.uniform(domain[0], domain[1], size=2)
        cand_w = np.random.uniform(1.0, 1.8)

        ok = True
        for c, w in zip(centers, widths):
            if np.linalg.norm(candidate - c) < (cand_w*0.8 + w*0.8 + min_dist):
                ok = False
                break
        if start_point is not None and np.linalg.norm(candidate - np.array(start_point)) < (cand_w + min_dist):
            ok = False

        if ok:
            centers.append(candidate)
            widths.append(cand_w)

    centers = np.array(centers)
    widths = np.array(widths)
    amplitudes = np.linspace(1.0, 4.3, num_bumps)

    def surface(x, y):
        val = np.zeros_like(x, dtype=float)
        for (cx, cy), a, w in zip(centers, amplitudes, widths):
            bump = a * np.exp(-((x - cx)**2 + (y - cy)**2) / (2 * w**2))
            val += bump
        return val

    return surface, centers, widths, amplitudes