import numpy as np

def random_search(loss_fn, start_points, field_size, steps=300):
    starts = np.array(start_points, dtype=float).copy()
    paths = []
    for start in starts:
        x, y = start
        best_gpa = loss_fn(x, y)
        path = [(x, y, best_gpa, x, y, best_gpa)]
        for _ in range(steps):
            rx = np.random.uniform(field_size[0], field_size[1])
            ry = np.random.uniform(field_size[0], field_size[1])
            gpa = loss_fn(rx, ry)
            if gpa > best_gpa:
                x, y, best_gpa = rx, ry, gpa
            path.append((rx, ry, gpa, x, y, best_gpa))
        paths.append(path)
    return paths