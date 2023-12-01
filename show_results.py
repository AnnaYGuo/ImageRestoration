import os
import cv2
import numpy as np

def load_images(directory, before):
    images = {}
    for filename in os.listdir(directory):
        # breakpoint()
        if filename.endswith(('.jpg', '.jpeg', '.png', '.tiff')):
            img_path = os.path.join(directory, filename)
            img = cv2.imread(img_path)
            identifier = filename.split('_blur')[0] if not before else filename.split('.')[0]  # Extract the common identifier

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

def save_comparison_images(before_images, after_images, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for before_identifier, before_image_list in before_images.items():
        for before_image_info in before_image_list:
            identifier = before_identifier
            after_image_list = after_images.get(identifier, [])
            # breakpoint()
            for after_image_info in after_image_list:
                # Resize the before image to the size of the first after image
                resized_before_image = resize_image(before_image_info[1], after_image_info[1].shape[:2][::-1])

                # Convert the original image to PNG format
                png_before_image = convert_to_png(resized_before_image)

                # Concatenate the PNG before image and all after images horizontally
                comparison_image = np.concatenate((png_before_image, * [after[1] for after in after_image_list]), axis=1)

                output_path = os.path.join(output_directory, f"comparison_{before_image_info[0]}.png")

                # Save the comparison image in PNG format
                cv2.imwrite(output_path, comparison_image)

def main():
    script_directory = os.path.dirname(__file__)
    
    before_directory = os.path.join(script_directory, input("Enter the relative path for preprocessed images: "))
    after_directory = os.path.join(script_directory, input("Enter the relative path for images after machine learning model: "))
    output_directory = os.path.join(script_directory, input("Enter the relative path to save comparison images: "))

    before_images = load_images(before_directory, True)
    after_images = load_images(after_directory, False)
    # breakpoint()

    if not before_images or not after_images:
        print("No images found in the specified directories.")
        return

    save_comparison_images(before_images, after_images, output_directory)
    print("Comparison images saved in the specified output directory as PNG.")

if __name__ == "__main__":
    main()
