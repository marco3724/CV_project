import subprocess
from highlight_points import draw_skeleton
import sys

import subprocess
import utility
import utility.utility

# Path to the Blender executable (adjust according to your system)
blender_path = "/usr/bin/blender"

# Path to the Blender script you want to execute
script_path = "./extract_info.py"
print( sys.argv[1:])
# Call Blender from the command line with the script
subprocess.run([blender_path, '--background', '--python', script_path] + sys.argv[1:])



args = utility.utility.parse_args(sys.argv[1:])

ncam = 2 if  "n" not in args else  int(args["n"])
ncam = 2 if ncam>2 else ncam

output_base_dir = "./out"
for i in range(ncam):
    n = i+1
    image_path = output_base_dir+f"/render_{n}.png"
    coordinates_file = output_base_dir + f"/bones_2D_coordinates_{n}.txt"  # File containing 2D bone coordinates
    bone_pairs_file = output_base_dir + "/bone_pairs.txt"            # File containing bone pairs
    output_path = output_base_dir + f"/skeleton_{n}.png"
    draw_skeleton(image_path, coordinates_file, bone_pairs_file, output_path)
