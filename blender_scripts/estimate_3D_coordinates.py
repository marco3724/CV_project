import numpy as np
import bpy

# Load 2D coordinates from the file
def load_2d_coordinates(file_path):
    points_2d = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            label = parts[0].strip()
            x = float(parts[1].strip())
            y = float(parts[2].strip())
            points_2d[label] = (x, y)
    return points_2d

# Function to get the intrinsic matrix of a camera
def get_intrinsic_matrix(camera, scene):
    focal_length = camera.lens  # in mm
    sensor_width = camera.sensor_width  # in mm
    resolution_x = scene.render.resolution_x
    resolution_y = scene.render.resolution_y
    scale = scene.render.resolution_percentage / 100

    # Adjust resolution based on scale
    resolution_x *= scale
    resolution_y *= scale

    # Focal lengths in pixel units
    f_x = (focal_length / sensor_width) * resolution_x
    f_y = (focal_length / sensor_width) * resolution_y
    c_x = resolution_x / 2
    c_y = resolution_y / 2

    # Intrinsic matrix
    K = np.array([
        [f_x, 0,   c_x],
        [0,   f_y, c_y],
        [0,   0,   1]
    ])
    return K

# Function to get the extrinsic matrix of a camera
def get_extrinsic_matrix(camera):
    cam_matrix = camera.matrix_world
    rotation_matrix = cam_matrix.to_3x3()
    translation_vector = cam_matrix.to_translation()
    
    # Convert to NumPy arrays
    rot = np.array(rotation_matrix)
    trans = np.array(translation_vector)
    
    # Create 3x4 extrinsic matrix
    extrinsic = np.hstack((rot, trans.reshape(3, 1)))
    return extrinsic

# Triangulation function
def triangulate_points(p1, p2, cam1, cam2):
    A = np.zeros((4, 4))
    A[0] = p1[0] * cam1[2] - cam1[0]
    A[1] = p1[1] * cam1[2] - cam1[1]
    A[2] = p2[0] * cam2[2] - cam2[0]
    A[3] = p2[1] * cam2[2] - cam2[1]

    _, _, Vt = np.linalg.svd(A)
    X = Vt[-1]
    return X[:3] / X[3]

# Main function to process the file and compute 3D points
def compute_3d_points(points2D_1,points2D_2,cam1,cam2):
    scene = bpy.context.scene


 


    # Get camera matrices
    K1 = get_intrinsic_matrix(cam1.data, scene)
    K2 = get_intrinsic_matrix(cam2.data, scene)
    E1 = get_extrinsic_matrix(cam1)
    E2 = get_extrinsic_matrix(cam2)

    # Projection matrices
    P1 = K1 @ E1
    P2 = K2 @ E2

    # Compute 3D points
    points_3d = {}
    print(points2D_1)
    for i,(label, (x, y,z)) in enumerate(points2D_1):
        
        # Assume the same 2D point in both cameras for simplicity
        # Replace with actual 2D points from both cameras if available
        p1 = np.array([x, y, 1])
        label, (x2,y2,z2) = points2D_2[i]
        p2 = np.array([x2, y2, 1])  # Replace with second camera points if different
        X_3D = triangulate_points(p1, p2, P1, P2)
        points_3d[label] = X_3D

    print("3D points computed successfully.", points_3d)



