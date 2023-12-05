import os
import cv2
import numpy as np
import imageio
from pathlib import Path
import argparse

blur = None
noise = None
downscale = None
crop = None
input_dir = None
output_dir = None
resolution = None
black_white = None

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
    
     # Get the original width of the image
    original_width = image.shape[1]
    original_height = image.shape[0]

    # Calculate the center of the image
    center_x, center_y = original_width // 2, image.shape[0] // 2

    # Calculate the size of the square (use the smaller dimension)
    small_size = min(original_width, original_height)
    large_size = max(original_width, original_height)

    # Calculate the coordinates for cropping
    small_left = center_x - small_size // 2
    small_top = center_y - small_size // 2
    small_right = center_x + small_size // 2
    small_bottom = center_y + small_size // 2

    pad_top = (large_size - original_height) // 2
    pad_bottom = large_size - original_height - pad_top
    pad_left = (large_size - original_width) // 2
    pad_right = large_size - original_width - pad_left
    
    #print(f"Padding - Top: {pad_top}, Bottom: {pad_bottom}, Left: {pad_left}, Right: {pad_right}")

    
    #black and white
    if(black_white):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Gaussian Blur
    
    for blur_size in blur:
        if (blur_size != 0): 
            num = blur_size - 1 if blur_size % 2 == 0 else blur_size
            blurred = cv2.GaussianBlur(image, (num, num), 0) 
        else: blurred = image
        # Gaussian Noise
        for var in noise:
            noisy = blurred + np.random.normal(0, var, blurred.shape)
            # Crop the image before downscale
                # Crop the image to the square
            if(crop=='inside_square'):
                noisy = noisy[small_top:small_bottom, small_left:small_right]
            elif(crop=='outside_square'):
                # breakpoint()
                noisy = np.pad(noisy, ((pad_top, pad_bottom), (pad_left, pad_right), (0, 0)), mode='constant', constant_values=0)
            if(crop=='inside_square' or crop=='outside_square'):
                if(resolution != False):
                    noisy = cv2.resize(noisy, (int(resolution), int(resolution)))
            # Downscaling
            for scale in downscale:
                downscaled = cv2.resize(noisy, (int(noisy.shape[1] * (scale)), int(noisy.shape[0] * (scale))))
                cv2.imwrite(os.path.join(output_dir, f"{prefix}_blur_{blur_size}_noise_{var}_downscale_{int(scale * 100)}.png"), downscaled)

def main():
    parser = argparse.ArgumentParser(description='Args for preprocessing', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-n', '--noise', nargs='+', type=int, default=[0, 20, 40], dest='noise', help='Apply noise with specified integer levels')
    parser.add_argument('-b', '--blur', nargs='+', type=int, default=[0, 20, 40], dest='blur', help='Apply blur with specified levels')
    parser.add_argument('-d', '--downscale', nargs='+', type=float, default=[1.0, 0.5, 0.25], dest='downscale', help='Downscale image by specified factors')
    crop_choices = ['inside_square', 'outside_square', 'no_crop']
    parser.add_argument('-c', '--crop', choices=crop_choices, default='outside_square', dest='crop', help='Crop image with specified option (choices: inside_square, outside_square, no_crop). outside square will make black bars, and inside square will cut off the longer dimension to make the image square shape')
    parser.add_argument('--input_dir', '-i', default='img_in', help='Input directory')
    parser.add_argument('--output_dir', '-o', default='img_preprocessed', help='Output directory')
    parser.add_argument('-r', '--resolution', default=False, help='Base resolution (Applies if image is cropped to a square using --crop)')
    parser.add_argument('-bw', '--black_white', action='store_true', default = False, help='Processes images in black and white')
    
    args = parser.parse_args()
    global blur 
    blur = args.blur
    global noise
    noise = args.noise
    global downscale
    downscale = args.downscale
    global crop
    crop = args.crop
    global input_dir
    input_dir = args.input_dir
    global output_dir
    output_dir = args.output_dir
    global resolution 
    resolution = args.resolution
    global black_white
    black_white = args.black_white
    print(f"Noise values: {args.noise}\nBlur values: {args.blur}\nDownscale values: {args.downscale}\nCrop option: {args.crop}")

    
    
    min_height, min_width = normalize_sizes(input_dir)
    img_dir = output_dir #+ f"/{prefix}"
    os.makedirs(img_dir, exist_ok=True)
    for filename in os.listdir(img_dir):
        file_path = os.path.join(img_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif')):
                img_path = os.path.join(root, file)
                if img_path.lower().endswith('.tiff') or img_path.lower().endswith('.tif'):
                    img = imageio.v2.imread(img_path)
                else:
                    img = cv2.imread(img_path)

                # Resize image to the baseline resolution
                #img = cv2.resize(img, (min_width, min_height))

                # Create output directory for the current input image
                input_name = Path(img_path).stem
                # output_subdir = os.path.join(output_dir, input_name)
                # os.makedirs(output_subdir, exist_ok=True)

                # Apply transformations and save output images
                
                apply_transformations(img, output_dir, input_name)

if __name__ == "__main__":
    main()