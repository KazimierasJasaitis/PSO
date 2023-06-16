import pso
import image_gen

n_pieces = 5  # Can be any integer between 2 and 8
folder_path = "C:/Users/Lenovo/Desktop/Kursinis Darbas/Stock Cutting Problem using PSO algorithm/testing/0" + n_pieces + "/"
image_path = folder_path + "image.png"


paper_width = 100
paper_height = 100
w = 0.7
c1 = 1
c2 = 2

for test_n in 10:
    image_folder = folder_path + test_n + "/"
    image_gen.cut_image(image_path, image_folder, n_pieces)
    image_sizes = pso.get_image_dimensions_from_folder(image_folder)
    N = len(image_sizes)
    dimensions = 3 * N
    bounds = (0, 100)  # replace with your actual bounds
    paper_size = (paper_width, paper_height)
    pso_object = pso.PSO(population_size=500, dimensions=dimensions, image_sizes=image_sizes, paper_size=paper_size, bounds=bounds, iterations=1000, w=w, c1=c1, c2=c2)
    best_position = pso_object.run()
    print(pso_object.gbest_fitness)
    # Reshape the best position to a 2D array
    best_position_2d = best_position.reshape(-1, 3)

    # Print each image's position and scale factor
    for i, (x, y, scale) in enumerate(best_position_2d):
        print(f"Image {i+1}: x = {x}, y = {y}, scale = {scale}")

    with open("output.txt", "w") as file:
        positions = best_position.reshape(-1, 3)
        for i, (x, y, scale) in enumerate(positions):
            file.write(f"Image {i}: x = {x}, y = {y}, scale = {scale}\n")

