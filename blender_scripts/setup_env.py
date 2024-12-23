import bpy
def setup_env(fbx_file_path):
        
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
    return (camera,armature)