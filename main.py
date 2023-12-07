import argparse
from PIL import Image, ImageFilter
import numpy as np
from multiprocessing import Pool
import time
import warnings

# Disable DecompressionBombWarning
Image.MAX_IMAGE_PIXELS = None
warnings.simplefilter("ignore", Image.DecompressionBombWarning)


def apply_gaussian_blur(segment):
    img = Image.fromarray(segment)
    blurred = img.filter(ImageFilter.GaussianBlur(radius=10))
    return np.array(blurred)


def image_processing_app(image_path, num_processes, resize_factor=None):
    # Load image
    img = Image.open(image_path)

    # Optionally resize image
    if resize_factor is not None:
        new_size = (int(img.width * resize_factor), int(img.height * resize_factor))
        img = img.resize(new_size, Image.LANCZOS)

    img_arr = np.array(img)

    # Split the image into horizontal segments
    height = img_arr.shape[0]
    segment_height = height // num_processes
    segments = [
        img_arr[i : i + segment_height] for i in range(0, height, segment_height)
    ]

    # Start the timer
    start_time = time.time()

    # Process each segment in parallel
    with Pool(num_processes) as pool:
        processed_segments = pool.map(apply_gaussian_blur, segments)

    # Stop the timer
    processing_time = time.time() - start_time

    # Combine segments
    processed_image = np.vstack(processed_segments)
    processed_image = Image.fromarray(processed_image)

    # Save the processed image
    processed_image.save("processed_image.jpg")
    print(processing_time)


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Image Processing App")
    parser.add_argument("thread_count", type=int, help="Number of threads")
    parser.add_argument("resize_factor", type=float, help="Resize factor for the image")
    args = parser.parse_args()

    # Call the image processing function with provided arguments
    image_processing_app(
        "test.jpg", args.thread_count, resize_factor=args.resize_factor
    )


if __name__ == "__main__":
    main()
