
# Function to parse arguments
def parse_args(args):
    named_args = {}
    if len(args)%2 !=0:
            args.pop()
    for i in range(0,len(args),2):  # Skip the first argument, which is the script name itself
        name = args[i].replace("-","")
        value = args[i+1]
        
        if name != "n":
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