import cv2

def draw_skeleton(image_path, coordinates_file, bone_pairs_file, output_path):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image.")
        return

    height, width, _ = image.shape  # Get the dimensions of the image

    # Load 2D coordinates
    coordinates = {}
    try:
        with open(coordinates_file, 'r') as file:
            for line in file:
                bone_name, norm_x, norm_y = line.strip().split(',')
                # Flip the Y-coordinate to match image coordinate origin
                coordinates[bone_name] = (float(norm_x) * width, (1 - float(norm_y)) * height)
    except FileNotFoundError:
        print(f"Error: Coordinates file {coordinates_file} not found.")
        return

    # Load bone pairs
    bone_pairs = []
    try:
        with open(bone_pairs_file, 'r') as file:
            for line in file:
                child, parent = line.strip().split(',')
                bone_pairs.append((child, parent))
    except FileNotFoundError:
        print(f"Error: Bone pairs file {bone_pairs_file} not found.")
        return

    # Draw skeleton lines
    for child, parent in bone_pairs:
        if child in coordinates and parent in coordinates:
            child_coord = coordinates[child]
            parent_coord = coordinates[parent]
            cv2.line(image, (int(child_coord[0]), int(child_coord[1])),
                     (int(parent_coord[0]), int(parent_coord[1])),
                     color=(0, 0, 255), thickness=2)

    # Draw points
    for coord in coordinates.values():
        cv2.circle(image, (int(coord[0]), int(coord[1])), radius=5, color=(0, 255, 0), thickness=-1)

    # Save the final image
    cv2.imwrite(output_path, image)
    print(f"Skeleton image saved to {output_path}")

    # # Debugging output for verification
    # print("Coordinates:")
    # for bone_name, coord in coordinates.items():
    #     print(f"{bone_name}: {coord}")

    # print("\nBone pairs:")
    # for child, parent in bone_pairs:
    #     print(f"{child} -> {parent}")

