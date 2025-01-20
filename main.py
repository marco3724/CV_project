import subprocess
from highlight_points import draw_skeleton


import subprocess

# Path to the Blender executable (adjust according to your system)
blender_path = "/usr/bin/blender"

# Path to the Blender script you want to execute
script_path = "./extract_info.py"

# Call Blender from the command line with the script
subprocess.run([blender_path, '--background', '--python', script_path])




# Example usage

output_base_dir = "./out"
for i in range(1,3):
    image_path = output_base_dir+f"/render_{i}.png"
    coordinates_file = output_base_dir + f"/bones_2D_coordinates_{i}.txt"  # File containing 2D bone coordinates
    bone_pairs_file = output_base_dir + "/bone_pairs.txt"            # File containing bone pairs
    output_path = output_base_dir + f"/skeleton_{i}.png"
    draw_skeleton(image_path, coordinates_file, bone_pairs_file, output_path)
