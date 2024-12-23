import bpy
from bpy_extras.object_utils import world_to_camera_view
import os
# Specify the file path of the FBX file
fbx_file_path = "./GiuliaRigged.fbx"  # Replace with the actual path to your FBX file

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
bone_pairs = []
# Retrieve the global coordinates of all bones
bone_coordinates_3d = []
if armature.pose:
    for bone in armature.pose.bones:
        
        if bone.parent:
            bone_pairs.append((bone.name, bone.parent.name))
        # Get the global position of the bone head
        bone_global_position = armature.matrix_world @ bone.head
        bone_coordinates_3d.append((bone.name, bone_global_position))


    # File path to save bone pairs
# output_file ="./bone_pairs.txt"
    
    # Save bone pairs to a file
with open(output_file, "w") as file:
    for child, parent in bone_pairs:
        file.write(f"{child},{parent}\n")

# Write the 3D bone coordinates to a text file
output_file_path_3d = "./bones_3D_coordinates.txt"
with open(output_file_path_3d, "w") as file:
    for bone_name, coord in bone_coordinates_3d:
        file.write(f"{bone_name}, {coord.x:.6f}, {coord.y:.6f}, {coord.z:.6f}\n")

print(f"3D bone coordinates have been saved to {output_file_path_3d}")

# Retrieve the 2D coordinates of all bones
bone_coordinates_2d = []
scene = bpy.context.scene
for bone_name, coord in bone_coordinates_3d:
    # Convert 3D global coordinates to 2D screen space
    coord_2d = world_to_camera_view(scene, camera, coord)
    bone_coordinates_2d.append((bone_name, coord_2d))

# Write the 2D bone coordinates to a text file
output_file_path_2d = "./bones_2D_coordinates.txt"
with open(output_file_path_2d, "w") as file:
    for bone_name, coord in bone_coordinates_2d:
        file.write(f"{bone_name}, {coord.x:.6f}, {coord.y:.6f}\n")

print(f"2D bone coordinates have been saved to {output_file_path_2d}")


# Define the output file path for the rendered image
render_output_path = bpy.path.abspath("./render.png")  # Save in the same directory as the .blend file

# Ensure the camera is set up in the scene
if bpy.context.scene.camera is None:
    print("Error: No camera found in the scene.")
else:
    # Render the scene
    bpy.context.scene.render.filepath = render_output_path
    bpy.ops.render.render(write_still=True)
    print(f"Render saved to {render_output_path}")

    # Optional: Verify the file exists
    if os.path.exists(render_output_path):
        print("Render completed successfully.")
    else:
        print("Render failed. Check the file path and permissions.")
        
        
        