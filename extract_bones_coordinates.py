import bpy
from bpy_extras.object_utils import world_to_camera_view

# Specify the file path of the FBX file
fbx_file_path = "/home/sh4ring4n/University/cv/GiuliaRigged.fbx"  # Replace with the actual path to your FBX file

# Import the FBX file
bpy.ops.import_scene.fbx(filepath=fbx_file_path)

# Get the imported armature object
armature = None
for obj in bpy.context.scene.objects:
    if obj.type == 'ARMATURE':
        armature = obj
        break

if armature is None:
    raise ValueError("No armature found in the imported FBX file.")

# Move the armature to the origin
armature.location = (0, 0, 0)
bpy.context.view_layer.update()

# Add a camera object
camera = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
bpy.context.collection.objects.link(camera)
camera.location = (0, -2, 25)
camera.rotation_euler = (0.13, 0, 0)
bpy.context.scene.camera = camera
bpy.context.view_layer.update()

# Retrieve the global coordinates of all bones
bone_coordinates_3d = []
if armature.pose:
    for bone in armature.pose.bones:
        # Get the global position of the bone head
        bone_global_position = armature.matrix_world @ bone.head
        bone_coordinates_3d.append((bone.name, bone_global_position))

# Write the 3D bone coordinates to a text file
output_file_path_3d = bpy.path.abspath("/home/sh4ring4n/University/cv/CV_project/bones_3D_coordinates.txt")
with open(output_file_path_3d, "w") as file:
    for bone_name, coord in bone_coordinates_3d:
        file.write(f"{coord.x:.6f}, {coord.y:.6f}, {coord.z:.6f}\n")

print(f"3D bone coordinates have been saved to {output_file_path_3d}")

# Retrieve the 2D coordinates of all bones
bone_coordinates_2d = []
scene = bpy.context.scene
for bone_name, coord in bone_coordinates_3d:
    # Convert 3D global coordinates to 2D screen space
    coord_2d = world_to_camera_view(scene, camera, coord)
    bone_coordinates_2d.append((bone_name, coord_2d))

# Write the 2D bone coordinates to a text file
output_file_path_2d = bpy.path.abspath("/home/sh4ring4n/University/cv/CV_project/bones_2D_coordinates.txt")
with open(output_file_path_2d, "w") as file:
    for bone_name, coord in bone_coordinates_2d:
        file.write(f"{coord.x:.6f}, {coord.y:.6f}\n")

print(f"2D bone coordinates have been saved to {output_file_path_2d}")
