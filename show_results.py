import os
import cv2
import numpy as np
from itertools import product
import matplotlib.pyplot as plt

def load_images(directory, before):
    images = {}
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.tiff', '.tif')):
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
    return cv2.resize(image, target_size[::-1], interpolation=cv2.INTER_AREA)

def convert_to_png(original_image):
    _, encoded_image = cv2.imencode('.png', original_image)
    png_image = cv2.imdecode(encoded_image, cv2.IMREAD_UNCHANGED)
    return png_image

def save_images_in_grid(images, grid_size, output_path, top_image=None, row_headers=None, col_headers=None):
    """
    Save a list of OpenCV images in a grid with a central top image above the grid and headers along rows and columns.

    Parameters:
    - images: List of OpenCV images (NumPy arrays) for the grid.
    - grid_size: Tuple (rows, cols) specifying the grid layout.
    - output_path: Output file path for the saved image.
    - top_image: Single OpenCV image (NumPy array) to be displayed centered above the grid.
    - row_headers: List of row headers.
    - col_headers: List of column headers.
    """
    rows, cols = grid_size
    total_images = len(images)

    # Ensure the number of provided images matches the grid size
    if total_images != (rows * cols):
        raise ValueError("Number of images does not match the grid size.")

    # Get the dimensions of a single image
    image_height, image_width, _ = images[0].shape

    # Calculate the size of the grid
    grid_width = image_width * cols
    grid_height = image_height * rows

    # Calculate the size of the combined image
    combined_width = grid_width
    combined_height = grid_height + top_image.shape[0] if top_image is not None else grid_height

    # Adjust the combined width if row headers are present
    if row_headers is not None:
        max_row_header_width = 0
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.7
        font_thickness = 2
        for header in row_headers:
            text_size = cv2.getTextSize(header, font, font_scale, font_thickness)[0]
            max_row_header_width = max(max_row_header_width, text_size[0])
        combined_width += max_row_header_width + 10

    # Create an empty combined image
    combined_image = np.zeros((combined_height, combined_width, 3), dtype=np.uint8)

    # Add the top image centered above the grid
    if top_image is not None:
        top_start_x = (combined_width - top_image.shape[1]) // 2
        top_start_y = 0
        combined_image[top_start_y:top_start_y + top_image.shape[0], top_start_x:top_start_x + top_image.shape[1], :] = top_image

    # Populate the grid with images
    for i in range(rows):
        for j in range(cols):
            image_index = i * cols + j
            combined_image[
                top_image.shape[0] + i * image_height: top_image.shape[0] + (i + 1) * image_height,
                (max_row_header_width if row_headers else 0) + j * image_width: (max_row_header_width if row_headers else 0) + (j + 1) * image_width,
                :
            ] = images[image_index]

    # Add row headers
    if row_headers is not None:
        row_padding = 5  # Adjust the row padding as needed
        row_highlight_color = (0, 0, 0)  # Black color for the row highlight
        for i, header in enumerate(row_headers):
            text_x = 10 + row_padding
            text_y = top_image.shape[0] + i * image_height + int((image_height + font_scale) // 2)

            # Draw a filled rectangle as the row highlight
            text_size = cv2.getTextSize(header, font, font_scale, font_thickness)[0]
            rect_start = (text_x - row_padding, text_y - int(text_size[1] / 2) - row_padding)
            rect_end = (text_x + text_size[0] + 2 * row_padding, text_y + int(text_size[1] / 2) + row_padding)
            cv2.rectangle(combined_image, rect_start, rect_end, row_highlight_color, thickness=cv2.FILLED)

            # Draw the row header text
            cv2.putText(combined_image, header, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    # Add column headers
    if col_headers is not None:
        col_padding = 5  # Adjust the column padding as needed
        col_highlight_color = (0, 0, 0)  # Black color for the column highlight
        for j, header in enumerate(col_headers):
            text_size = cv2.getTextSize(header, font, font_scale, font_thickness)[0]
            text_x = (max_row_header_width if row_headers else 0) + j * image_width + int((image_width - text_size[0]) // 2)
            text_y = top_image.shape[0] - 10

            # Draw a filled rectangle as the column highlight
            rect_start = (text_x - col_padding, text_y - text_size[1] - col_padding)
            rect_end = (text_x + text_size[0] + col_padding, text_y + col_padding)
            cv2.rectangle(combined_image, rect_start, rect_end, col_highlight_color, thickness=cv2.FILLED)

            # Draw the column header text
            cv2.putText(combined_image, header, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    # Save the combined image
    combined_image = cv2.imencode('.jpg', combined_image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])[1]
    cv2.imwrite(output_path, combined_image)

col_headers = ["Downscale 0%", "Downscale 25%", "Downscale 50%"]
row_headers = ["Blur 0, Noise 0", "Blur 0, Noise 27", "Blur 0, Noise 45",
               "Blur 11, Noise 0", "Blur 11, Noise 27", "Blur 11, Noise 45",
               "Blur 21, Noise 0", "Blur 21, Noise 27", "Blur 21, Noise 45"]
def save_comparison_images(before_images, after_images, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for identifier, before_image_list in before_images.items():
        for img in before_image_list:
            after_image_list = after_images.get(identifier, [])
            # breakpoint()
            after_image_list = sorted(after_image_list, key=lambda x : x[0]) # should be 27x27
            # breakpoint()

            after_image_list = [resize_image(x[1], img[1].shape[0:2]) for x in after_image_list]

            output_path = os.path.join(output_directory, f"comparison_{identifier}.png")
            save_images_in_grid(after_image_list, (9,3), output_path, top_image=img[1], row_headers=row_headers, col_headers=col_headers)

def main():
    script_directory = os.path.dirname(__file__)
    
    before_directory = os.path.join(script_directory, input("Enter the relative path for non-preprocessed images: "))
    after_directory = os.path.join(script_directory, input("Enter the relative path for images after machine learning model: "))
    output_directory = os.path.join(script_directory, input("Enter the relative path to save comparison images: "))

    before_images = load_images(before_directory, True)
    after_images = load_images(after_directory, False)

    if not before_images or not after_images:
        print("No images found in the specified directories.")
        return

    # breakpoint()

    # combinations = generate_combinations()

    # # Create after images for each combination of settings
    # for identifier, before_image_list in before_images.items():
    #     for combination in combinations:
    #         after_image_list = [[[]]]
    #         for blur, noise, downscale in zip(*combination):
    #             after_image_id_list = after_images.get(f"{identifier}", [])
    #             # breakpoint()
    #             for x in after_image_id_list:
    #                 if x[0] == f"{identifier}_blur_{blur}_noise_{noise}_downscale_{downscale}.png": after_image_info = x

    #             if after_image_info:
    #                 after_image_list.extend(after_image_info)
                    
    save_comparison_images(before_images, after_images, output_directory)

    print("Comparison images saved in the specified output directory as PNG.")

if __name__ == "__main__":
    main()
