import numpy as np
from PIL import Image
import os

folder_path = "C:/Users/Lenovo/Desktop/Kursinis Darbas/Stock Cutting Problem using PSO algorithm/images/"
def get_image_dimensions_from_folder(folder_path):
    image_sizes = []
    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            with Image.open(os.path.join(folder_path, filename)) as img:
                width, height = img.size
                image_sizes.append((width, height))
    return image_sizes

class Particle:
    def __init__(self, dimensions, bounds):
        self.position = np.random.uniform(bounds[0], bounds[1], dimensions)
        self.velocity = np.random.uniform(-1, 1, dimensions)
        self.pbest_position = self.position
        self.pbest_fitness = float('inf')

    def compute_fitness(self, image_sizes, paper_size, scaling_penalty_factor, overlap_penalty_factor):
        fitness = 100

        # Initialize the total area of the paper
        total_area = paper_size[0] * paper_size[1]
        # Initialize the sum of image areas
        sum_image_areas = 0
        # Initialize the total resizing deviation
        total_resizing_deviation = 0
        # Initialize the area of overlapping
        overlapping_area = 0
        # Reshape the position vector for easier manipulation
        positions = self.position.reshape(-1, 3)
        # Compute the average scale
        avg_scale = sum(scale for _, _, scale in positions) / len(positions)

        for i, (x, y, scale) in enumerate(positions):

            width, height = image_sizes[i]

            if (scale <= 0):
                fitness += (abs(scale) * 100) ** 2
            if (x < 0 or paper_size[0] <= 0):
                fitness += abs(x) ** 2
            if (y < 0 or paper_size[1] <= 0):
                fitness += abs(y) ** 2
            if (scale < 0 or x < 0 or y < 0):
                continue

            # Calculate the new dimensions of the image after resizing
            new_width = width * scale
            new_height = height * scale

            # Add to the sum of image areas
            sum_image_areas += new_width * new_height

            # Calculate the resizing deviation
            resizing_deviation = (abs(scale - avg_scale)*10) ** 2  # Using square of the deviation from the average scale

            # Add to the total resizing deviation
            total_resizing_deviation += resizing_deviation

            # Check for overlaps with other images and out of boundary
            for j, (x2, y2, scale2) in enumerate(positions):
                if i != j:
                    width2, height2 = image_sizes[j]
                    new_width2 = width2 * scale2
                    new_height2 = height2 * scale2

                    # Check for overlapping
                    dx = min(x + new_width, x2 + new_width2) - max(x, x2)
                    dy = min(y + new_height, y2 + new_height2) - max(y, y2)
                    if dx > 0 and dy > 0:
                        overlapping_area += abs(dx * dy)

                    # Check for out of boundary
                    if (x + new_width > paper_size[0] or y + new_height > paper_size[1]):
                        out_of_bounds_area = new_width * new_height
                        fitness += abs(out_of_bounds_area) * 100

        if (scale > 0 or x >= 0 or y >= 0):
            uncovered_area = abs(total_area - sum_image_areas + overlapping_area)
            # Compute the fitness
            fitness += uncovered_area + scaling_penalty_factor * total_resizing_deviation + overlap_penalty_factor * overlapping_area

        

        return fitness



    def update_velocity(self, gbest_position, w, c1, c2):
        r1 = np.random.uniform(0, 1, len(self.position))
        r2 = np.random.uniform(0, 1, len(self.position))
        cognitive_velocity = c1 * r1 * (self.pbest_position - self.position)
        social_velocity = c2 * r2 * (gbest_position - self.position)
        self.velocity = w * self.velocity + cognitive_velocity + social_velocity

    def update_position(self, bounds, image_sizes, paper_size):
        new_position = self.position + self.velocity
        # Reshape the position vector for easier manipulation
        positions = new_position.reshape(-1, 3)
        corrected_velocity = self.velocity.reshape(-1, 3)

        # for i, (x, y, scale) in enumerate(positions):
        #     width, height = image_sizes[i]

        #     # Make sure scale is positive
        #     scale = max(0.1, abs(scale))

        #     # Calculate the new dimensions of the image after resizing
        #     new_width = width * scale
        #     new_height = height * scale

        #     # Calculate maximum allowable scale
        #     max_scale_x = paper_size[0] / width
        #     max_scale_y = paper_size[1] / height
        #     max_scale = min(max_scale_x, max_scale_y)

        #     # Check and correct scale if it's too large
        #     scale_old = scale
        #     scale = min(scale, max_scale)
        #     if scale_old != scale:
        #         corrected_velocity[i, 2] = 0
        #         new_width = width * scale
        #         new_height = height * scale

        #     # Correct position if the image is out of the boundary
        #     x_old = x
        #     y_old = y
        #     x = max(0, min(x, paper_size[0] - new_width))
        #     y = max(0, min(y, paper_size[1] - new_height))

        #     # If position was corrected, set velocity in that dimension to 0
        #     if x_old != x:
        #         corrected_velocity[i, 0] = 0
        #     if y_old != y:
        #         corrected_velocity[i, 1] = 0

        #     # Update the position in the position vector
        #     positions[i] = [x, y, scale]

        # Update the position vector and velocity
        self.position = positions.flatten()
        self.velocity = corrected_velocity.flatten()



class PSO:
    def __init__(self, population_size, dimensions, bounds, iterations):
        self.population_size = population_size
        self.dimensions = dimensions
        self.bounds = bounds
        self.iterations = iterations
        self.gbest_position = np.zeros(dimensions)
        self.gbest_fitness = float('inf')
        self.population = [Particle(dimensions, bounds) for _ in range(population_size)]

    def run(self):
        print("Start of run method")  # Debug print
        for _ in range(self.iterations):
            for particle in self.population:
                fitness = particle.compute_fitness(image_sizes, paper_size, scaling_penalty_factor=10, overlap_penalty_factor=5)
                if fitness < particle.pbest_fitness:
                    particle.pbest_fitness = fitness
                    particle.pbest_position = particle.position

                if fitness < self.gbest_fitness:
                    self.gbest_fitness = fitness
                    self.gbest_position = particle.position

            for particle in self.population:
                particle.update_velocity(self.gbest_position, w=0.5, c1=1, c2=2)
                particle.update_position(bounds, image_sizes, paper_size)
        print("End of run method")  # Debug print
        return self.gbest_position  # This line returns the best position

paper_width = 100
paper_height = 100
image_sizes = get_image_dimensions_from_folder(folder_path)
N = len(image_sizes)
dimensions = 3 * N
bounds = (0, 100)  # replace with your actual bounds
paper_size = (paper_width, paper_height)
pso = PSO(population_size=500, dimensions=dimensions, bounds=bounds, iterations=1000)
best_position = pso.run()
print(pso.gbest_fitness)
# Reshape the best position to a 2D array
best_position_2d = best_position.reshape(-1, 3)

# Print each image's position and scale factor
for i, (x, y, scale) in enumerate(best_position_2d):
    print(f"Image {i+1}: x = {x}, y = {y}, scale = {scale}")

with open("output.txt", "w") as file:
    positions = best_position.reshape(-1, 3)
    for i, (x, y, scale) in enumerate(positions):
        file.write(f"Image {i}: x = {x}, y = {y}, scale = {scale}\n")