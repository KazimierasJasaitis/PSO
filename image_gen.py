import os
import random
from PIL import Image, ImageDraw

def cut_image(image_path, output_folder, n_pieces):
    # Ensure that n is between 2 and 8
    if n_pieces < 2 or n_pieces > 8:
        raise ValueError("n_pieces should be between 2 and 8.")

    # Load the image
    image = Image.open(image_path)
    width, height = image.size

    # Calculate the number of points
    n_points = (n_pieces + 1) // 2

    # Store the cutting coordinates
    horizontal_cuts = [0, height]
    vertical_cuts = [0, width]

    # Choose random points and create orthogonal lines
    for i in range(n_points):
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        if i == 0 or n_pieces % 2 == 0:
            # Add horizontal line
            horizontal_cuts.append(y)
        if i == 0 or n_pieces > 2:
            # Add vertical line
            vertical_cuts.append(x)

    # Sort the coordinates for cutting
    horizontal_cuts.sort()
    vertical_cuts.sort()

    # Cut the image into pieces and save
    for i in range(1, len(horizontal_cuts)):
        for j in range(1, len(vertical_cuts)):
            left = vertical_cuts[j - 1]
            upper = horizontal_cuts[i - 1]
            right = vertical_cuts[j]
            lower = horizontal_cuts[i]
            cropped_image = image.crop((left, upper, right, lower))
            cropped_image.save(os.path.join(output_folder, f'piece_{i}_{j}.png'))

# Example usage:
image_path = 'C:/Users/Lenovo/Desktop/Kursinis Darbas/Stock Cutting Problem using PSO algorithm/images/image.png'
output_folder = 'C:/Users/Lenovo/Desktop/Kursinis Darbas/Stock Cutting Problem using PSO algorithm/images/'
n_pieces = 2  # Can be any integer between 2 and 8

cut_image(image_path, output_folder, n_pieces)
