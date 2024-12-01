import bpy
import mathutils
import random
from bpy_extras.object_utils import world_to_camera_view


def import_mesh():
     # Path to your FBX file
    fbx_path = "/home/sh4ring4n/University/cv/GiuliaRigged.fbx"

    # Import the FBX file
    bpy.ops.import_scene.fbx(filepath=fbx_path)

    print("FBX file imported successfully!")

    # Get the human mesh object 
    human_armature = bpy.data.objects['Armature']
    human_mesh = None
    for obj in human_armature.children:
        if obj.type == "MESH":
            human_mesh = obj
    if human_mesh == None:
        print("No mesh found")
        
    # Set the mesh's location to the origin 
    human_mesh.location = (0.0, 0.0, 0.0) 
    # Update the scene to reflect the change 
    bpy.context.view_layer.update()

    mesh = human_mesh.data
    
    return mesh


def setup():
    # Delete all objects in the scene
    bpy.ops.object.select_all(action='SELECT')  # Select all objects
    bpy.ops.object.delete()  # Delete selected objects
    import_mesh()
    print("All objects in the scene have been deleted.")


   
    # Create a new camera
    camera_data = bpy.data.cameras.new("Ego")
    camera = bpy.data.objects.new("Ego", camera_data)
    bpy.context.collection.objects.link(camera)

    # Position the camera
    camera.location = (0, -2, 25)  # Adjust based on the mesh size
    camera.rotation_euler = (0, 0, 0)  # Look straight down

    # Set the camera as the active camera
    bpy.context.scene.camera = camera

    print("Camera set up successfully!")
    scene = bpy.context.scene

    # Intrinsic parameters
    params = {
        "FOCAL_LENGTH": camera.data.lens,
        "SENSOR_WIDTH": camera.data.sensor_width,
        "SENSOR_HEIGHT": camera.data.sensor_height,
        "IMAGE_WIDTH": scene.render.resolution_x,
        "IMAGE_HEIGHT": scene.render.resolution_y,
        "CAMERA_LOCATION": camera.location,
        "CAMERA_ROTATION": camera.rotation_euler
    
    }
    

    print("Focal Length:", params["FOCAL_LENGTH"])
    print("Sensor Width:", params["SENSOR_WIDTH"])
    print("Sensor Height:", params["SENSOR_HEIGHT"])
    print("Location:", params["CAMERA_LOCATION"])
    print("Rotation:", params["CAMERA_ROTATION"])
    
    return camera, params


def point_in_camera_view(camera, point, params):
    """
    Check if a 3D point is within the camera's field of view.
    """
    # Transform point to camera space
    cam_matrix_world = camera.matrix_world.inverted()
    point_cam_space = cam_matrix_world @ point

    # Camera space coordinates
    x, y, z = point_cam_space.x, point_cam_space.y, point_cam_space.z

    if z <= 0:  # Point is behind the camera
        return False

    # Compute normalized device coordinates (NDC)
    ndc_x = (x / z) * params["FOCAL_LENGTH"] / (params["SENSOR_WIDTH"] / 2)
    ndc_y = (y / z) * params["FOCAL_LENGTH"] / (params["SENSOR_HEIGHT"] / 2)

    # Check if the point is within the normalized device coordinate bounds (-1 to 1)
    return -1 <= ndc_x <= 1 and -1 <= ndc_y <= 1

def generate_random_points(camera, params, num_points=200, depth_range=(1.0, 10.0)):
    """
    Generate random points within the camera's frustum.
    """
    points = []
    while len(points) < num_points:
        # Generate random point in world space
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        z = random.uniform(depth_range[0], depth_range[1])
        point = mathutils.Vector((x, y, z))

        # Check if the point is within the camera's view
        if point_in_camera_view(camera, point, params):
            points.append(point)

    return points

def create_cube_at_point(point, material):
    """
    Create a small cube at a specified point in 3D space and assign a material.
    """
    bpy.ops.mesh.primitive_cube_add(location=point)
    cube = bpy.context.object

    # Ensure the cube has valid data before assigning the material
    if cube and cube.data:
        cube.scale = (0.1, 0.1, 0.1)  # Adjust cube size
        cube.data.materials.append(material)

def create_red_material():
    """
    Create a red material for the cubes.
    """
    material_name = "Red_Material"

    # Check if the material already exists
    if material_name not in bpy.data.materials:
        red_material = bpy.data.materials.new(name=material_name)
        red_material.diffuse_color = (1.0, 0.0, 0.0, 1.0)  # Red color
    else:
        red_material = bpy.data.materials[material_name]
    
    return red_material

def save_2d_coordinates(camera, points):
    """
    Save the 2D coordinates of points in the camera view.
    """
    coordinates = []
    for point in points:
        projected = world_to_camera_view(bpy.context.scene, camera, point)
        coordinates.append((projected.x, projected.y))
    return coordinates

    
def main():
    # Create the camera object if not present
    camera, params = setup()

    # Generate random points within the camera's field of view
    random_points = generate_random_points(camera, params, num_points=100)

    # Create material
    red_material = create_red_material()

    for point in random_points:
        create_cube_at_point(point, red_material)

    # Save and register 2D coordinates
    coordinates = save_2d_coordinates(camera, random_points)
    with open("/home/sh4ring4n/University/cv/3D_coordinates.txt", 'w') as file:
        file.writelines(f"{point.x},{point.y},{point.z}\n" for point in random_points)
    
    with open("/home/sh4ring4n/University/cv/2D_coordinates.txt", 'w') as file:
        file.writelines(f"{point[0]},{point[1]}\n" for point in coordinates)
        
    
        
    

if __name__ == "__main__":
    main()
