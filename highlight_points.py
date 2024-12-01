import cv2

def draw_points(image_path, coordinates_file, output_path):
    """
    Draws green points on an image at specified normalized coordinates.

    :param image_path: Path to the input image.
    :param coordinates_file: Path to the text file containing normalized 2D coordinates.
    :param output_path: Path to save the output image.
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image.")
        return

    height, width, _ = image.shape  # Get the dimensions of the image

    # Read coordinates from the text file
    try:
        with open(coordinates_file, 'r') as file:
            for line in file:
                # Parse each line to extract normalized coordinates
                try:
                    norm_x, norm_y = map(float, line.strip().split(','))
                    # Convert normalized coordinates to pixel values
                    x = int(norm_x * width)
                    y = int(norm_y * height)
                    # Draw a green circle on the image
                    cv2.circle(image, (x, y), radius=5, color=(0, 255, 0), thickness=-1)
                except ValueError:
                    print(f"Invalid coordinate format: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: File {coordinates_file} not found.")
        return

    # Save the modified image
    cv2.imwrite(output_path, image)
    print(f"Output image saved to {output_path}")


# Example usage
image_path = "./rotated_render.png"
# image_path = "./render.png"

coordinates_file = "2D_coordinates.txt"
output_path = "./out/out.png"

draw_points(image_path, coordinates_file, output_path)
