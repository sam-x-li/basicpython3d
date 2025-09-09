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
  - View and edit object/camera parameters and matrices in real time using the GUI

---

## Installation 
```bash
git clone https://github.com/sam-x-li/basicpython3d.git
cd basicpython3d
pip install -r requirements.txt
```


## Usage
Run the engine:
```bash
cd src
python main.py
```
---

### Controls:

- Move camera using WASD keys. Press E to go up, and Q to go down.
- Rotate camera using the arrow keys, or by holding down RMB and dragging the mouse.

- Change parameters and matrices by typing into the GUI
- Transform loaded models under the Objects tab
- Reposition camera, change FOV, and toggle view mode under the Camera tab
- Import and delete models under the Import tab

## Images

<img width="1380" height="980" alt="Screenshot 1" src="https://github.com/user-attachments/assets/61d8541c-3493-4041-8f89-45af06d47360" />
<img width="1380" height="980" alt="screenshot 2" src="https://github.com/user-attachments/assets/5325ed52-7a48-4eba-a100-f42ea4cb3f60" />
<img width="1380" height="980" alt="Screenshot 3" src="https://github.com/user-attachments/assets/73288d1b-2818-4b6f-94b4-096fa706f69b" />

![Clip1](https://github.com/user-attachments/assets/fd5f1850-1ca4-4918-a183-9895b90c7df0)

