import os
import bpy
from bpy_extras.object_utils import world_to_camera_view

def is_point_visible(ndc):
    """
    Determines if a point in NDC is visible within the camera's view frustum.
    
    :param ndc: Vector containing NDC coordinates (x, y, z)
    :return: Boolean indicating visibility
    """
    # Check if the point is in front of the camera
    if ndc.z < 0.0:
        return False

    # Check if the point is within the horizontal and vertical bounds
    if 0.0 <= ndc.x <= 1.0 and 0.0 <= ndc.y <= 1.0:
        return True
    else:
        return False



def projection(camera,bone_coordinates_3d,output_file_path_2d,output_render):
    # Retrieve the 2D coordinates of all bones
    bone_coordinates_2d = []
    scene = bpy.context.scene
    for bone_name, coord in bone_coordinates_3d:
        # Convert 3D global coordinates to 2D screen space

        coord_2d = world_to_camera_view(scene, camera, coord)

        if is_point_visible(coord_2d):
            bone_coordinates_2d.append((bone_name, coord_2d))

    # Write the 2D bone coordinates to a text file
    with open(output_file_path_2d, "w") as file:
        for bone_name, coord in bone_coordinates_2d:
            file.write(f"{bone_name}, {coord.x:.6f}, {coord.y:.6f}\n")

    print(f"2D bone coordinates have been saved to {output_file_path_2d}")


    # Define the output file path for the rendered image
    render_output_path = bpy.path.abspath(output_render)  # Save in the same directory as the .blend file

    bpy.context.scene.camera = camera
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
    
        
        