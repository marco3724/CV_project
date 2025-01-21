import bpy
def setup_env(fbx_file_path,num_cameras=1,position_offset = (0,0,0),rotation=(0.13,0,0)):

    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
        
    # Import the FBX file
    bpy.ops.import_scene.fbx(filepath=fbx_file_path)
    print(f"Setting up the env with {num_cameras} cameras, and offset of {position_offset}, and rotation of {rotation}")
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

    # Create the cameras
    cameras = []
    baseline_distance = 2.0
    px,py,pz = position_offset
    for i in range(num_cameras):
        # Calculate camera position along the baseline
        x_position = 0 if num_cameras == 1 else (-baseline_distance / 2) + (i * (baseline_distance / (num_cameras - 1)))
        camera = bpy.data.objects.new(f"Camera_{i + 1}", bpy.data.cameras.new(f"Camera_{i + 1}"))
        bpy.context.collection.objects.link(camera)

        # Set camera position and orientation
        camera.location = (x_position + px, -2 + py, 25 + pz)  # Fixed Y and Z, aligned along X
        camera.rotation_euler =   rotation # Look straight ahead
        cameras.append(camera)
        

    # Set the first camera as the active scene camera
    bpy.context.view_layer.update()
    return (cameras,armature)