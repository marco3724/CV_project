# CV_PROJECT

This project for the Computer Vision course of University of Trento 2023/24.

## Project Structure

```
CV_PROJECT/
├── assets/                     # Resources such as images or datasets
├── blender_scripts/            # Scripts for Blender processing
│   ├── extract_3D_coordinates.py
│   ├── projection_2D.py
│   ├── setup_env.py
├── out/                        # Output folder for generated files
├── utility/                    
│   ├── utility.py              # utility functions
├── .gitignore                  # Git ignore file
├──extract_info.py              # Uses the blender script to extract the information 
├──highlight_points.py          # Highlight the 2D point of the image
├── main.py                     # Main script for coordinating tasks
├── readme.md                   # Readme 
├── requirements.txt            # Requirements
```

## Dependencies
- Python 3.7+
- Blender (Ensure the executable path is configured correctly)
- Change the path in  `main.py` file !!!!
```
# Path to the Blender executable (adjust according to your system)
blender_path = "/usr/bin/blender"
```
- Install the requirements in the requirements.txt
```bash
pip install -r requirements.txt
```

## Usage

The main script, `main.py`, coordinates the workflow and allows you to pass arguments for configuring the camera setup. Below are the available arguments and their descriptions:

### Command-Line Arguments

| Argument     | Description                                              | Format                 |
|--------------|----------------------------------------------------------|------------------------|
| `-n`         | Number of cameras to use in the setup                    | Integer (e.g., 2)      |
| `-t`         | Translation offset of the cameras in cm                  | `x,y,z` (e.g., 1,0,0)  |
| `-r`         | Rotation of the cameras                                  | `x,y,z` (e.g., 0,90,0) |
| `-l`         | Set a light source                                       | (`True` of `False`)    |

### Example Usage
1. **Basic Run**
   ```bash
   python main.py 
2. **Run with parameters**
   ```bash
   python main.py -n 2 -t 1,0,0 -r 0,90,0
