import bpy
def setup_env(fbx_file_path,num_cameras=1,position_offset = (0,0,0),rotation=(0.13,0,0),light=False):

    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    position_offset = [x*0.01 for x in position_offset] #cm

    print(f"Setting up the env with {num_cameras} cameras, and offset of {position_offset} cm, and rotation of {rotation} and light {light}")
    if light:
        # Create a new sun light data block
        light_data = bpy.data.lights.new(name="Sun_Light", type='SUN')

        # Create a new light object
        light_object = bpy.data.objects.new(name="Sun_Light", object_data=light_data)

        # Set light position and rotation
        light_object.location = (0, 0, 100)
        light_object.rotation_euler = (0, 0, 0)

        # Link the light object to the active collection
        bpy.context.collection.objects.link(light_object)

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
    armature.delta_scale = (0.115,0.115,0.115)
    bpy.context.view_layer.update()

    # Create the cameras
    cameras = []
    baseline_distance = 12 * 0.01 #cm


    px,py,pz = position_offset
    for i in range(num_cameras):
        # Calculate camera position along the baseline
        x_position = 0 if num_cameras == 1 else (-baseline_distance / 2) + (i * (baseline_distance / (num_cameras - 1)))
        camera = bpy.data.objects.new(f"Camera_{i + 1}", bpy.data.cameras.new(f"Camera_{i + 1}"))
        bpy.context.collection.objects.link(camera)

        # Set camera position and orientation
        camera.location = (x_position + px, -0.2 + py, 2.8 + pz)  # Fixed Y and Z, aligned along X
        camera.rotation_euler =   rotation # Look straight ahead
        cameras.append(camera)


    # Set the first camera as the active scene camera
    bpy.context.view_layer.update()
    return (cameras,armature)
