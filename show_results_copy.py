import os
import cv2
import numpy as np
from itertools import product

def load_images(directory, before):
    images = {}
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.tiff')):
            img_path = os.path.join(directory, filename)
            img = cv2.imread(img_path)
            identifier = filename.split('_blur')[0] if not before else filename.split('.')[0]  # Extract the common identifier

            # breakpoint()

            if identifier in images:
                images[identifier].append((filename, img))
            else:
                images[identifier] = [(filename, img)]

    return images

def resize_image(image, target_size):
    return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)

def convert_to_png(original_image):
    _, encoded_image = cv2.imencode('.png', original_image)
    png_image = cv2.imdecode(encoded_image, cv2.IMREAD_UNCHANGED)
    return png_image

def generate_combinations():
    blur_settings = ['0', '1', '2']  # Replace with your desired blur settings
    noise_settings = ['0', '1', '2']  # Replace with your desired noise settings
    downscale_settings = ['0', '1', '2']  # Replace with your desired downscale settings

    return list(product(blur_settings, noise_settings, downscale_settings))

def save_comparison_images(before_images, after_images, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for before_identifier, before_image_list in before_images.items():
        for before_image_info in before_image_list:
            identifier = before_identifier
            after_image_list = after_images.get(identifier, [])

            # Create a grid for the after images
            num_rows = len(after_image_list) + 1  # Add 1 for the original before image
            breakpoint()
            num_cols = len(after_image_list[0][1])  # Assuming all images have the same width

            grid_image = np.zeros((num_rows * after_image_list[0][1].shape[0], num_cols * after_image_list[0][1].shape[1], 3), dtype=np.uint8)

            # Add the original before image to the grid
            resized_before_image = resize_image(before_image_info[1], (num_cols * after_image_list[0][1].shape[1], after_image_list[0][1].shape[0]))
            png_before_image = convert_to_png(resized_before_image)
            grid_image[:before_image_info[1].shape[0], :num_cols * after_image_list[0][1].shape[1]] = png_before_image

            # Add the after images to the grid
            for i, after_image_info in enumerate(after_image_list):
                row_start = (i + 1) * after_image_info[1].shape[0]
                row_end = (i + 2) * after_image_info[1].shape[0]
                col_start = 0
                col_end = after_image_info[1].shape[1]

                grid_image[row_start:row_end, col_start:col_end] = after_image_info[1]

            # Resize the grid to a reasonable size
            grid_image = resize_image(grid_image, (800, 800))

            output_path = os.path.join(output_directory, f"comparison_{before_identifier}_{before_image_info[0]}.png")

            # Save the comparison image in PNG format
            cv2.imwrite(output_path, grid_image)

def main():
    script_directory = os.path.dirname(__file__)
    
    before_directory = os.path.join(script_directory, input("Enter the relative path for preprocessed images: "))
    after_directory = os.path.join(script_directory, input("Enter the relative path for images after machine learning model: "))
    output_directory = os.path.join(script_directory, input("Enter the relative path to save comparison images: "))

    before_images = load_images(before_directory, True)
    after_images = load_images(after_directory, False)

    if not before_images or not after_images:
        print("No images found in the specified directories.")
        return

    combinations = generate_combinations()

    # Create after images for each combination of settings
    for identifier, before_image_list in before_images.items():
        for combination in combinations:
            after_image_list = []
            for blur, noise, downscale in zip(*combination):
                after_image_info = after_images.get(f"{identifier}_blur_{blur}_noise_{noise}_downscale_{downscale}", [])
                if after_image_info:
                    after_image_list.extend(after_image_info)

            save_comparison_images({identifier: before_image_list}, {identifier: after_image_list}, output_directory)

    print("Comparison images saved in the specified output directory as PNG.")

if __name__ == "__main__":
    main()
