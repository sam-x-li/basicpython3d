# basicpython3d

A 3D graphics engine built from scratch in Python without using external 3D libraries, only numpy, pygame, and pygame_gui. 
Supports importing .obj 3D models, basic transformations, and camera movement. 
Created as a secondary school project to explore graphics pipelines from scratch, and as a mathematical education tool.
Renders using perspective projection and the rasterisation pipeline.

---

## Features:
  - Import 3D object models into the scene
  - Simple object transformations: translation, rotation, scaling
  - Camera control: movement, rotation, FOV
  - Switch between free and orbital camera modes
  - View and edit object/camera parameters in real time using the GUI
  - View and edit matrices (camera, model, perspective) in real time using the GUI

---

## Installation 
git clone https://github.com/sam-x-li/basicpython3d.git
cd basicpython3d
pip install -r requirements.txt

## Usage
cd src
python main.py

---

### Controls:

- Move camera using WASD keys. Press E to go up, and Q to go down.
- Rotate camera using the arrow keys, or by holding down RMB and dragging the mouse.

- Change parameters and matrices by typing into the GUI
- Transform loaded models under the Objects tab
- Reposition camera, change FOV, and toggle view mode under the Camera tab
- Import and delete models under the Import tab
