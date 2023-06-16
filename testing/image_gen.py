import os
import random
from PIL import Image
import math


def cut_image(image_path, output_folder, n_pieces):
    # Ensure that n is between 2 and 8
    if n_pieces < 2 or n_pieces > 8:
        raise ValueError("n_pieces should be between 2 and 8.")

    # Load the image
    image = Image.open(image_path)
    width, height = image.size

    # Store the cutting coordinates
    horizontal_cuts = [0, height]
    vertical_cuts = [0, width]

    # Calculate the number of horizontal and vertical cuts needed
    n_horizontal_cuts = int(math.sqrt(n_pieces))
    n_vertical_cuts = (n_pieces - 1) // n_horizontal_cuts + 1

    # Select random points for horizontal cuts
    horizontal_cuts += random.sample(range(1, height - 1), n_horizontal_cuts - 1)
    # Select random points for vertical cuts
    vertical_cuts += random.sample(range(1, width - 1), n_vertical_cuts - 1)

    # Sort the lists
    horizontal_cuts.sort()
    vertical_cuts.sort()

    # Cut the image into pieces and save
    piece_counter = 1
    for i in range(1, len(horizontal_cuts)):
        for j in range(1, len(vertical_cuts)):
            if piece_counter > n_pieces:
                break
            left = vertical_cuts[j - 1]
            upper = horizontal_cuts[i - 1]
            right = vertical_cuts[j]
            lower = horizontal_cuts[i]
            cropped_image = image.crop((left, upper, right, lower))
            cropped_image.save(os.path.join(output_folder, f'0{piece_counter}.png'))
            piece_counter += 1

if __name__ == "__main__":
    # Example usage:
    image_path = 'C:/Users/Lenovo/Desktop/Kursinis Darbas/Stock Cutting Problem using PSO algorithm/images/image.png'
    output_folder = 'C:/Users/Lenovo/Desktop/Kursinis Darbas/Stock Cutting Problem using PSO algorithm/images/'
    n_pieces = 5  # Can be any integer between 2 and 8

    cut_image(image_path, output_folder, n_pieces)
