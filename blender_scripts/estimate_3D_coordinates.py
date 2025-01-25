# Get the intris params such as the focal lenght, principal component and baseline(even though we asleady known)
# for each point convert the normalized coordinates to pixel coordinates
# perform triangulation
# transform the point from stereo local to camera local
# transform the point from camera local to world
# save the 3d points to a file



import bpy
import mathutils

def get_camera_intrinsics(camera_obj, scene):
    """
    Retrieve focal length in pixel units (f) and principal point (cx, cy)
    from the Blender camera and the scene's render settings.
    This is a simplified approach (no distortion).
    """
    cam_data = camera_obj.data
    render = scene.render
    
    # Render dimensions
    width  = render.resolution_x
    height = render.resolution_y
    
    # Focal length in mm
    focal_mm = cam_data.lens
    # Sensor size in mm. We pick sensor_width unless sensor_fit='VERTICAL'
    if cam_data.sensor_fit != 'VERTICAL':
        sensor_size_mm = cam_data.sensor_width
    else:
        sensor_size_mm = cam_data.sensor_height

    print(f"Focal length: {focal_mm} mm | Sensor size: {sensor_size_mm} mm")
    print(f"Resolution: {cam_data.sensor_width} x { cam_data.sensor_height}")

    # Convert focal length in mm -> focal length in pixel units
    # (assuming no special aspect ratio issues for simplicity)
    f = (focal_mm / sensor_size_mm) * width
    
    # Principal point (cx, cy):
    # Start at the center
    cx = width  * 0.5
    cy = height * 0.5
    
    # Add lens shift if any (in normalized sensor coords)
    shift_x = cam_data.shift_x
    shift_y = cam_data.shift_y
    cx += shift_x * width
    cy += shift_y * height
    
    return f, cx, cy

def get_baseline(camera_left, camera_right):
    """
    Returns the distance (baseline) between the two camera centers in 3D space.
    If the cameras are truly parallel along the X-axis, this is effectively
    the difference in X coordinates. But we'll compute the full Euclidean distance.
    """
    loc_left = camera_left.matrix_world.translation
    loc_right = camera_right.matrix_world.translation
    baseline_vector = loc_right - loc_left
    print(f"Baseline vector: {baseline_vector} {baseline_vector.length}")
    return baseline_vector.length

def stereo_triangulate(uL, vL, uR, vR, f, cx, cy, baseline):
    """
    Triangulates a 3D point under a parallel stereo assumption:
    - (uL, vL) in left camera
    - (uR, vR) in right camera
    - f : focal length (in pixel units)
    - (cx, cy): principal point
    - baseline: distance between cameras
    
    Returns a Vector((X, Y, Z)) in the LEFT camera coordinate system,
    assuming the left camera is at (0,0,0) looking along +Z 
    with the image plane at Z=f and principal point at (cx, cy).
    """
    # Disparity
    disparity = (uL - uR)
    if abs(disparity) < 1e-9:
        print("Warning: Disparity is near zero; point might be infinitely far or matched incorrectly.")
        return None

    # Depth from the standard formula Z = f * B / disparity
    Z = (f * baseline) / disparity

    # X, Y from the left camera's perspective
    X = (uL - cx) * Z / f
    Y = (vL - cy) * Z / f

    return mathutils.Vector((X, Y, Z))


def compute_3d_points(pts1: dict, pts2: dict, cam1, cam2):
    #Get the scene
    scene = bpy.context.scene

    camera_left_obj = cam1
    camera_right_obj = cam2

    print("Computing 3D points \n\n")
    
    if camera_left_obj is None or camera_right_obj is None:
        print("Error: Could not find CameraLeft or CameraRight.")
        return
    # 1) Get intrinsics from the left camera (assuming left & right share same intrinsics)
    f, cx, cy = get_camera_intrinsics(camera_left_obj, scene)
    print(f"Camera intrinsics: f={f}, cx={cx}, cy={cy}")
    
    # 2) Measure baseline (distance between camera centers)
    baseline = get_baseline(camera_left_obj, camera_right_obj)
    points_3d = {}
    for name, coord in pts1.items():
        if name not in pts2:
            continue

        # We need to convert coordinates from normalized camera coordinates
        # to pixel coordinates in order to triangulate the 3D point
        xL,yL,_ = coord
        xR,yR,_ = pts2[name]

        width = scene.render.resolution_x
        height = scene.render.resolution_y
        # Convert from normalized to pixel coordinates, Blender’s y=0 is at the bottom; for a standard top-left origin we do 1-y
        vL = (1 - yL) * height
        vR = (1 - yR) * height
        uR = xR * width
        uL = xL * width
        
    
        # 3) Perform triangulation
        point_3d_left_cam = stereo_triangulate(uL, vL, uR, vR, f, cx, cy, baseline)
        if point_3d_left_cam is None:
            return
        
        # Compensate blender by flipping the Z and Y axes: (X, Y, Z) -> (X, -Y, -Z)
        flip_z = mathutils.Matrix([
            [1,  0,  0],
            [0, -1,  0],
            [0,  0, -1],
        ])
        point_cam_local = flip_z @ point_3d_left_cam
        
        # Step 2: then transform from camera local to world
        point_world = camera_left_obj.matrix_world @ point_cam_local
        points_3d[name] = point_world
            
    with open("./out/reconstructed_3d_points.txt","w") as f:
            for label,(x,y,z) in points_3d.items():
                f.write(f"{label}, {x:.6f}, {y:.6f}, {z:.6f}\n")




