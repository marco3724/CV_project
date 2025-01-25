
import numpy as np

# Function to parse arguments
def parse_args(args):
    named_args = {}
    
    if len(args)%2 !=0:
            args.pop()
    for i in range(0,len(args),2):  
        name = args[i].replace("-","")
        value = args[i+1]
        if name == "l":
            value = value == "True"
        elif name != "n":
            value = tuple((map(float,value.split(","))))
            if len(value) != 3:
                 continue
            
            
        named_args[name] = value
    return named_args



def create_coordinates_map(file_path):
    coordinates_map = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4: 
                label = parts[0].strip()
                x, y, z = map(float, parts[1:])
                coordinates_map[label] = {'x': x, 'y': y, 'z': z}
    return coordinates_map


def compute_results(common_labels,predicted_map, ground_truth_map):
    
    errors = []
    x, y, z = 0, 0, 0
    for label in common_labels:
        
        predicted_coord = predicted_map[label]
        ground_truth_coord = ground_truth_map[label]
        
        # Compute the Euclidean distance (L2 norm) for the current label
        predicted_array = np.array([predicted_coord['x'], predicted_coord['y'], predicted_coord['z']])
        ground_truth_array = np.array([ground_truth_coord['x'], ground_truth_coord['y'], ground_truth_coord['z']])
        
        # Compute the Average absolte error        
        x += abs(predicted_coord['x'] - ground_truth_coord['x'])
        y += abs(predicted_coord['y'] - ground_truth_coord['y'])
        z += abs(predicted_coord['z'] - ground_truth_coord['z'])
        
        
        error = np.linalg.norm(predicted_array - ground_truth_array)
        errors.append(error)

    # Compute the mean error
    mpjpe = np.mean(errors)
    
    return (mpjpe, x/len(common_labels), y/len(common_labels), z/len(common_labels))