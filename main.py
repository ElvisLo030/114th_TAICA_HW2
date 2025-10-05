import numpy as np
from visuals import visualize
from algo_example import random_search
from algo1 import hill_climbing
from algo2 import simulated_annealing
from algo3 import ultimate_algorithm
from landscape import generate_circular_surface

def save_paths_to_file(paths, filename="result1.txt"):
    with open(filename, "w") as f:
        for i, path in enumerate(paths):
            f.write(f"Path {i+1}:\n")
            for point in path:
                f.write("  " + ", ".join(f"{val:.4f}" for val in point) + "\n")
            f.write("\n")
    print(f"Result saved as {filename}")


def main():
    num_bumps = 8
    min_dist = 3.0
    num_spaceship = 10
    field_size = (-8, 8)
    fuel_for_movement = 30
    start_points = [(np.random.uniform(field_size[0]*0.8, field_size[1]*0.8),
                     np.random.uniform(field_size[0]*0.8, field_size[1]*0.8)) for _ in range(num_spaceship)]

    loss_fn, centers, widths, amplitudes = generate_circular_surface(num_bumps, min_dist, field_size)
    
    # --- Example: Single spaceship ---
    num_spaceship = 1
    result = {"Example": random_search(loss_fn, start_points[:num_spaceship], field_size, steps=fuel_for_movement)}
    save_paths_to_file(result["Example"], "example_1.txt")
    visualize(loss_fn, result, centers, widths, amplitudes, field_size, filename="optimizer_example_1.gif")

    # --- Example: Ten spaceships ---
    num_spaceship = 10
    result = {"Example": random_search(loss_fn, start_points[:num_spaceship], field_size, steps=fuel_for_movement)}
    save_paths_to_file(result["Example"], "example_10.txt")
    visualize(loss_fn, result, centers, widths, amplitudes, field_size, filename="optimizer_example_10.gif")

    num_spaceship = 1
    result = {"Hill Climbing": hill_climbing(loss_fn, start_points[:num_spaceship], field_size, steps=fuel_for_movement)}
    save_paths_to_file(result["Hill Climbing"], "result1.txt")
    visualize(loss_fn, result, centers, widths, amplitudes, field_size, filename="optimizer1.gif")

    num_spaceship = 1
    result = {"Simulated Annealing": simulated_annealing(loss_fn, start_points[:num_spaceship], field_size, steps=fuel_for_movement)}
    save_paths_to_file(result["Simulated Annealing"], "result2.txt")
    visualize(loss_fn, result, centers, widths, amplitudes, field_size, filename="optimizer2.gif")

    num_spaceship = 10
    result ={"Ultimate Algorithm": ultimate_algorithm(loss_fn, start_points[:num_spaceship], field_size, steps=fuel_for_movement)}
    save_paths_to_file(result["Ultimate Algorithm"], "result3.txt")
    visualize(loss_fn, result, centers, widths, amplitudes, field_size, filename="optimizer3.gif")
    
    
if __name__ == "__main__":
    main()