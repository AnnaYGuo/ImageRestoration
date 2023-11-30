import os
import cv2
import numpy as np
import imageio
from pathlib import Path

def normalize_sizes(input_dir):
    sizes = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff')):
                img_path = os.path.join(root, file)
                img = imageio.v2.imread(img_path)
                sizes.append(img.shape[:2])

    min_height = min(sizes, key=lambda x: x[0])[0]
    min_width = min(sizes, key=lambda x: x[1])[1]

    return min_height, min_width

def apply_transformations(image, output_dir, prefix):
    # Gaussian Blur
    for blur_size in [0, 11, 21]:
        if (blur_size != 0): blurred = cv2.GaussianBlur(image, (blur_size, blur_size), 0) 
        else: blurred = image
        # Gaussian Noise
        for var in [0, 27, 45]:
            noisy = blurred + np.random.normal(0, var, blurred.shape)
            # Downscaling
            for scale in [0, 0.25, 0.5]:
                downscaled = cv2.resize(noisy, (int(noisy.shape[1] * (1 - scale)), int(noisy.shape[0] * (1 - scale))))
                cv2.imwrite(os.path.join(output_dir, f"{prefix}_blur_{blur_size}_noise_{var}_downscale_{int(scale * 100)}.jpg"), downscaled)

def main(input_dir, output_dir):
    min_height, min_width = normalize_sizes(input_dir)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif')):
                img_path = os.path.join(root, file)
                if img_path.lower().endswith('.tiff') or img_path.lower().endswith('.tif'):
                    img = imageio.v2.imread(img_path)
                else:
                    img = cv2.imread(img_path)

                # Resize image to the baseline resolution
                img = cv2.resize(img, (min_width, min_height))

                # Create output directory for the current input image
                input_name = Path(img_path).stem
                output_subdir = os.path.join(output_dir, input_name)
                os.makedirs(output_subdir, exist_ok=True)

                # Apply transformations and save output images
                apply_transformations(img, output_subdir, input_name)

if __name__ == "__main__":
    input_directory = "./img_in"
    output_directory = "./img_preprocessed"

    main(input_directory, output_directory)