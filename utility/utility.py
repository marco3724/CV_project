
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