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
        
    def compute_fitness(self, image_sizes, paper_size, scaling_penalty_factor=10, boundary_penalty_factor=10, overlap_penalty_factor=10):
        # Initialize the total area of the paper
        total_area = paper_size[0] * paper_size[1]

        # Initialize fitness to 0
        fitness = 0

        # Initialize the sum of image areas
        sum_image_areas = 0

        # Initialize the total resizing deviation
        total_resizing_deviation = 0

        # Initialize the area of overlapping
        overlapping_area = 0

        # Initialize the boundary penalty
        boundary_penalty = 0

        # Initialize the scale penalty
        scale_penalty = 0

        # Calculate average scale
        positions = self.position.reshape(-1, 3)
        avg_scale = np.mean([scale for _, _, scale in positions])

        for i, (x, y, scale) in enumerate(positions):
            width, height = image_sizes[i]

            # Penalize negative or too small scales
            if scale <= 0.1:
                scale_penalty += 1 - scale if scale < 1 else scale - 1
            
            # Calculate the new dimensions of the image after resizing
            new_width = width * abs(scale)  # taking absolute value of scale
            new_height = height * abs(scale)  # taking absolute value of scale

            # Add to the sum of image areas
            sum_image_areas += new_width * new_height

            # Calculate the resizing deviation
            resizing_deviation = (abs(scale) - avg_scale) ** 2
            total_resizing_deviation += resizing_deviation

            # Check for overlaps with other images and out of boundary
            for j, (x2, y2, scale2) in enumerate(positions):
                if i != j:
                    width2, height2 = image_sizes[j]
                    new_width2 = width2 * abs(scale2)  # taking absolute value of scale
                    new_height2 = height2 * abs(scale2)  # taking absolute value of scale

                    # Check for overlapping
                    if (x < x2 + new_width2 and x + new_width > x2 and
                        y < y2 + new_height2 and y + new_height > y2):
                        overlapping_area += (min(x + new_width, x2 + new_width2) - max(x, x2)) * \
                                            (min(y + new_height, y2 + new_height2) - max(y, y2))

                    # Check for out of boundary
                    if (x + new_width > paper_size[0] or y + new_height > paper_size[1] or x < 0 or y < 0):
                        excess_area = max(0, x + new_width - paper_size[0]) * new_height + \
                                    max(0, y + new_height - paper_size[1]) * new_width + \
                                    max(0, -x) * new_height + \
                                    max(0, -y) * new_width
                        boundary_penalty += excess_area

        # Compute the covered area ratio
        covered_area_ratio = min(sum_image_areas / total_area, 1)

        # Add penalties to fitness
        fitness += scaling_penalty_factor * total_resizing_deviation
        fitness += boundary_penalty_factor * boundary_penalty
        fitness += overlap_penalty_factor * overlapping_area
        fitness += scaling_penalty_factor * scale_penalty

        # Reward for covering the paper (subtracts from the penalties)
        fitness -= covered_area_ratio  # This value is between 0 and 1

        return fitness



    
    def update_position(self):
        self.position = self.position + self.velocity

    def update_velocity(self, gbest_position, w, c1, c2):
        r1 = np.random.uniform(0, 1, len(self.position))
        r2 = np.random.uniform(0, 1, len(self.position))
        cognitive_velocity = c1 * r1 * (self.pbest_position - self.position)
        social_velocity = c2 * r2 * (gbest_position - self.position)
        self.velocity = w * self.velocity + cognitive_velocity + social_velocity

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
                particle.update_position()
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