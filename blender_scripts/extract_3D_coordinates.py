def extract_3d_coordinates(armature,output_file_path_3d,output_file):

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


        
        # Save bone pairs to a file
    with open(output_file, "w") as file:
        for child, parent in bone_pairs:
            file.write(f"{child},{parent}\n")
            
    with open(output_file_path_3d, "w") as file:
        for bone_name, coord in bone_coordinates_3d:
            file.write(f"{bone_name}, {coord.x:.6f}, {coord.y:.6f}, {coord.z:.6f}\n")

    print(f"3D bone coordinates have been saved to {output_file_path_3d}")
    return bone_coordinates_3d
