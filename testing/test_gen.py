import pso
import image_gen
import os
import time

n_pieces = 4  # Can be any integer between 2 and 8
folder_path = "C:/Users/Lenovo/Desktop/Kursinis Darbas/Stock Cutting Problem using PSO algorithm/testing/0" + str(n_pieces) + "/"
image_path = folder_path + "image.png"



test_n = 2

paper_width = 100
paper_height = 100
w = 0.7
c1 = 1
c2 = 2


for test_i in range(1,test_n+1):
    start_time = time.time()
    os.makedirs(folder_path + str(test_i))
    image_folder = folder_path + str(test_i) + "/"
    image_gen.cut_image(image_path, image_folder, n_pieces)
    image_sizes = pso.get_image_dimensions_from_folder(image_folder)
    N = len(image_sizes)
    dimensions = 3 * N
    bounds = (0, 100)  # replace with your actual bounds
    paper_size = (paper_width, paper_height)
    pso_object = pso.PSO(population_size=500, dimensions=dimensions, image_sizes=image_sizes, paper_size=paper_size, bounds=bounds, desired_fitness=0.005, w=w, c1=c1, c2=c2)
    best_position = pso_object.run()
    print(pso_object.gbest_fitness)
    # Reshape the best position to a 2D array
    best_position_2d = best_position.reshape(-1, 3)


    end_time = time.time()
    duration = end_time - start_time
    print(f"The loop ran for {duration} seconds")

    for i, (x, y, scale) in enumerate(best_position_2d):
        print(f"Image {i+1}: x = {x}, y = {y}, scale = {scale}")

    with open(image_folder + "output.txt", "w") as file:
        positions = best_position.reshape(-1, 3)
        file.write(image_folder + "\n")
        for i, (x, y, scale) in enumerate(positions):
            file.write(f"Image {i}: x = {x}, y = {y}, scale = {scale}\n")

