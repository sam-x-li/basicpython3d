from vectormaths import * 
from model import *
from camera import *
from scene import *
from math import trunc 
import pygame, pygame_gui

width, height = 1100, 800 
    
pygame.init()
bg = pygame.Surface((1180, 800))
bg.fill(pygame.Color('#8AEFFF'))
screen = pygame.display.set_mode((width, height))

manager = pygame_gui.UIManager((1100, 800)) 

float_formatter = "{:.1f}".format 
np.set_printoptions(formatter={'float_kind':float_formatter})

initial_panel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((800, 0), (300, 800)),
                                                     manager=manager)
clock = pygame.Clock()

class tabGUI: 
    def __init__(self, rect, tabText):
        self.tab = pygame_gui.elements.UIButton(relative_rect=rect,
                                                text=tabText,
                                                manager=manager,
                                                container=initial_panel,
                                                anchors={'right': 'right'})
        self.panel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((0, 100), (480, 700)),
                                                        manager=manager, container=initial_panel, visible=False)
        
    
    def updateLabel(self, label, text): 
        if text:
            label.set_text(text)
    
    @staticmethod
    def dropDown(rect, options_list, starting_option, container): #dropdown menu method
        menu = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=options_list, 
                                                                    starting_option=starting_option, 
                                                                    relative_rect=rect, manager=manager,
                                                                    container=container)
        return menu
    
    @staticmethod
    def label(rect, text, container): 
        pygame_gui.elements.ui_label.UILabel(relative_rect=rect,
                                            manager=manager, container=container,
                                            text=text)
        
    @staticmethod
    def textEntry(rect, text, container): 
        entryLine = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=rect,
                                                                        container=container, manager=manager,
                                                                        initial_text=text)
        entryLine.set_allowed_characters(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '[', ']', '.', ' ', '-', ','])
        entryLine.set_text_length_limit(30)
        return entryLine
    
    @classmethod 
    def displayMatrix(cls, matrixlines, container): 
        matrix_entries = []
        matrix_entries.append(cls.textEntry(pygame.Rect((75, 100), (150, 30)), f'{str(matrixlines[0])}', container))
        matrix_entries.append(cls.textEntry(pygame.Rect((75, 130), (150, 30)), f'{str(matrixlines[1])}', container))
        matrix_entries.append(cls.textEntry(pygame.Rect((75, 160), (150, 30)), f'{str(matrixlines[2])}', container))
        cls.label(pygame.Rect((75, 190), (150, 30)), f'{str(matrixlines[3])}', container)
        return matrix_entries
            
    def conditionInput(line:str, length:int): #conditions text from TextEntryLines into a valid list
        result = line.strip()
        result = result.replace('[', '')
        result = result.replace(']', '')
        result = result.replace(',', '')
        result = result.split(' ')
        if len(result) != length:
            result = False
        return result
        
class objects_tab(tabGUI):
    def __init__(self, objectlist, objectIndex):
        super().__init__(pygame.Rect((-290, 5), (100,30)), 'Objects')
        self.makeObjectsMenu(objectlist)
        self.init2(objectlist, objectIndex)

    def makeObjectsMenu(self, objectlist): #generates the object selection menu
        objectNames = [model.name for model in objectlist]
        objectNames.insert(0, 'Select Object')
        self.objectNames = objectNames
        self.model_choice = tabGUI.dropDown(pygame.Rect((0, 0), (140, 30)),
                                        objectNames, 
                                        objectNames[1], self.panel)   
        
    def init2(self, objectlist, objectIndex): #needs to be called when the selected object changes
        self.objects_menu = tabGUI.dropDown(pygame.Rect((160, 0), (140, 30)),
                                        ['Select Values', 'Variables', 'Model Matrix'],    
                                        'Select Values', self.panel)
        
        self.objectIndex = objectIndex
        self.selectedObject = objectlist[objectIndex]
        
        self.modelType = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((75, 100), (150, 30)),
                                                            manager=manager, container=self.panel,
                                                            text=f'Type: {self.selectedObject.type}')
        self.numberOfVertices = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((50, 160), (200, 30)),
                                                                    manager=manager, container=self.panel,
                                                                    text=f'Number of Vertices: {len(self.selectedObject.vectors)}')
        self.numberOfTris = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((50, 220), (200, 30)),
                                                                manager=manager, container=self.panel,
                                                                text=f'Number of Triangles: {len(self.selectedObject.tris)}')
        self.matrixlines = [matrixline.round(1).tolist() for matrixline in self.selectedObject.modelMatrix.val]

        self.matrixPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((0, 300), (480, 400)),
                                                                manager=manager, container=self.panel, visible=False)
        tabGUI.label(pygame.Rect((75, 0), (150, 30)), 'Model Matrix', self.matrixPanel)
        self.resetMatrixButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((112, 50), (75, 30)),
                                            text='Reset',
                                            manager=manager,
                                            container=self.matrixPanel,
                                            command=self.resetMatrix)
        self.matrix_entries = tabGUI.displayMatrix(self.matrixlines, self.matrixPanel)

        self.variablePanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((0, 300), (480, 400)),
                                                                manager=manager, container=self.panel, visible=False)
        tabGUI.label(pygame.Rect((75, 0), (150, 30)), 'Variables', self.variablePanel)
        tabGUI.label(pygame.Rect((0, 50), (150, 30)), 'Position', self.variablePanel)
        tabGUI.label(pygame.Rect((0, 100), (150, 30)), 'Orientation', self.variablePanel)
        tabGUI.label(pygame.Rect((0, 150), (150, 30)), 'Scale', self.variablePanel)

        positionEntry = tabGUI.textEntry(pygame.Rect((150, 50), (150, 30)), f'{str(self.selectedObject.position.val)}', self.variablePanel)
        orientationEntry = tabGUI.textEntry(pygame.Rect((150, 100), (150, 30)), f'{self.selectedObject.orientation}', self.variablePanel)
        scaleEntry = tabGUI.textEntry(pygame.Rect((150, 150), (150, 30)), f'{self.selectedObject.scaling}', self.variablePanel)

        self.variableEntries = [positionEntry, orientationEntry, scaleEntry]
        self.inputVariables = [self.selectedObject.position, self.selectedObject.orientation, self.selectedObject.scaling]

    def show(self): 
        self.model_choice.kill() #just in case
        self.makeObjectsMenu(scene.objects)
        self.panel.show()
        self.matrixPanel.hide()
        self.variablePanel.hide()
    
    def hide(self):
        self.panel.hide()

    def switchPanel(self, event):
        if event.text == 'Model Matrix':
            self.variablePanel.hide()
            self.matrixPanel.show()
        elif event.text == 'Variables':
            self.matrixPanel.hide()
            self.variablePanel.show()
        else:
            self.matrixPanel.hide()
            self.variablePanel.hide()

    def handleMatrixEntry(self, event, entryIndex): #checks user input for errors, changes matrix if valid
        newLine = tabGUI.conditionInput(event.text, 4)
        if newLine:
            self.matrixlines[entryIndex] = newLine
        self.matrix_entries[entryIndex].set_text(str(np.array(self.matrixlines[entryIndex]).astype(float)))

    def updateMatrix(self): #updates matrix after changes made to the text entries
        self.selectedObject.modelMatrix = Matrix.from_list(self.matrixlines)

    def resetMatrix(self): #resets matrix to values given by the variable panel
        self.selectedObject.modelMatrix = self.selectedObject.get_modelMatrix()
        self.matrixlines = [matrixline.round(1).tolist() for matrixline in self.selectedObject.modelMatrix.val]
        for i in range(3):
            self.matrix_entries[i].set_text(str(np.array(self.matrixlines[i]).astype(float)))

    def handleTextEntry(self, event, entryIndex): 
        newLine = tabGUI.conditionInput(event.text, 3)
        if newLine:
            if entryIndex == 0:
                self.inputVariables[entryIndex].val = np.array(list(map(float, newLine)))
            else:
                self.inputVariables[entryIndex] = list(map(float, newLine))
        self.variableEntries[entryIndex].set_text(f'{self.inputVariables[entryIndex]}')
        self.updateVariables(entryIndex)

    def updateVariables(self, entryIndex): #updates all the variables of the selected object
        global modelMoveFlag
        if entryIndex == 0:
            self.selectedObject.position.val = self.inputVariables[entryIndex].val
            modelMoveFlag = True
        elif entryIndex == 1:
            self.selectedObject.orientation = self.inputVariables[entryIndex]
        elif entryIndex == 2:
            self.selectedObject.scaling = self.inputVariables[entryIndex]
        self.selectedObject.modelMatrix = self.selectedObject.get_modelMatrix()
        self.resetMatrix()

    def remakeGUI(self): 
        self.modelType.kill()
        self.numberOfTris.kill()
        self.numberOfVertices.kill()
        self.matrixPanel.kill()
        self.variablePanel.kill()
        self.objects_menu.kill()

    def update(self, event):
        global objectAddedFlag

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element in self.variableEntries:
                i = self.variableEntries.index(event.ui_element)
                self.handleTextEntry(event, i)
            elif event.ui_element in self.matrix_entries:
                i = self.matrix_entries.index(event.ui_element)
                self.handleMatrixEntry(event, i)
                self.updateMatrix()
        
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.model_choice:
                if event.text != 'Select choice':
                    self.remakeGUI()
                    self.init2(scene.objects, self.objectNames.index(event.text)-1)
            elif event.ui_element == self.objects_menu:
                self.switchPanel(event)

        if objectChangeFlag: #if object added or deleted, need to remake the GUI
            self.remakeGUI()
            self.init2(scene.objects, 0)

class camera_tab(tabGUI):
    def __init__(self, objectlist, camera):
        super().__init__(pygame.Rect((-190, 5), (100,30)), 'Camera')
        self.objectIndex = 0
        self.cam = camera
        self.cam_menu = tabGUI.dropDown(pygame.Rect((160, 0), (140, 30)),
                                        ['Select Values', 'Variables', 'Camera Matrix', 'Projection Matrix'],    
                                        'Select Values', self.panel)
        self.swapModeButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((75, 75), (150, 30)),
                                                            text='LookAt Mode',
                                                            manager=manager,
                                                            container=self.panel,
                                                            command=self.swapMode)
        tabGUI.label(pygame.Rect((20, 160), (100, 30)), 'Select Target:', self.panel) 
        self.makeObjectsMenu(objectlist)
        self.init2()

    def init2(self):
        self.matrixPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((0, 300), (480, 400)),
                                                                manager=manager, container=self.panel, visible=False)
        tabGUI.label(pygame.Rect((75, 0), (150, 30)), 'Camera Matrix', self.matrixPanel)

        self.projPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((0, 300), (480, 400)),
                                                                manager=manager, container=self.panel, visible=False)
        tabGUI.label(pygame.Rect((75, 0), (150, 30)), 'Projection Matrix', self.projPanel)
        tabGUI.label(pygame.Rect((0, 50), (150, 30)), 'Horizontal FOV', self.projPanel)
        self.FOVEntry = tabGUI.textEntry(pygame.Rect((150, 50), (75, 30)), f'{str(self.cam.fov)}', self.projPanel)
        self.FOVEntry.set_allowed_characters('numbers')
        self.FOVEntry.set_text_length_limit(3)

        self.setMatrix()

        self.variablePanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((0, 300), (480, 400)),
                                                                manager=manager, container=self.panel, visible=False)
        tabGUI.label(pygame.Rect((75, 0), (150, 30)), 'Variables', self.variablePanel)
        tabGUI.label(pygame.Rect((0, 50), (150, 30)), 'Position', self.variablePanel)
        tabGUI.label(pygame.Rect((0, 100), (150, 30)), 'Orientation', self.variablePanel)

        positionEntry = tabGUI.textEntry(pygame.Rect((150, 50), (150, 30)), f'{str(self.cam.position.val)}', self.variablePanel)
        orientationEntry = tabGUI.textEntry(pygame.Rect((150, 100), (150, 30)), f'{self.cam.orientation}', self.variablePanel)

        self.variableEntries = [positionEntry, orientationEntry]
        self.inputVariables = [self.cam.position, self.cam.orientation]

    def makeObjectsMenu(self, objectlist):
        objectNames = [model.name for model in objectlist]
        self.objectNames = objectNames
        self.model_choice = tabGUI.dropDown(pygame.Rect((160, 160), (140, 30)),
                                        objectNames, 
                                        objectNames[0], self.panel) 

    def show(self):
        self.panel.show()
        self.matrixPanel.hide()
        self.variablePanel.hide()
        self.projPanel.hide()
    
    def hide(self):
        self.panel.hide()

    def switchPanel(self, event):
        if event.text == 'Camera Matrix':
            self.matrixPanel.show()
            self.variablePanel.hide()
            self.projPanel.hide()
        elif event.text == 'Projection Matrix':
            self.matrixPanel.hide()
            self.variablePanel.hide()
            self.projPanel.show()
        elif event.text == 'Variables':
            self.matrixPanel.hide()
            self.variablePanel.show()
            self.projPanel.hide()
        else:
            self.matrixPanel.hide()
            self.variablePanel.hide()
            self.projPanel.hide()

    def setMatrix(self): #initialises projection matrix text boxes
        self.matrixlines = [pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((50, 100+ 30 * n), (200, 30)),
                                            manager=manager, container=self.matrixPanel,
                                            text='0') for n in range(4)]
        temp_lines = [matrixline.round(1).tolist() for matrixline in self.cam.projection_matrix.val]
        self.projlines = [pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((50, 100+ 30 * n), (200, 30)),
                                            manager=manager, container=self.projPanel,
                                            text=f'{temp_lines[n]}') for n in range(4)]

    def updateMatrix(self): 
        temp = [matrixline.round(2).tolist() for matrixline in self.cam.view_matrix.val]
        [self.matrixlines[i].set_text(f'{temp[i]}') for i in range(4)]

    def swapMode(self):
        global cameraMode
        if cameraMode == 1:
            cameraMode = 2
            self.swapModeButton.set_text('Regular Mode')
        else:
            cameraMode = 1
            self.swapModeButton.set_text('LookAt Mode')
            self.cam.fixVectors()

    def handleTextEntry(self, event, entryIndex):
        newLine = tabGUI.conditionInput(event.text, 3)
        if newLine:
            if entryIndex == 0:
                self.inputVariables[entryIndex].val = np.array(list(map(float, newLine)))
            else:
                self.inputVariables[entryIndex] = list(map(float, newLine))
        self.variableEntries[entryIndex].set_text(f'{self.inputVariables[entryIndex]}')
        self.updateVariables(entryIndex)

    def updateVariables(self, entryIndex):
        if entryIndex == 0:
            self.cam.position.val = self.inputVariables[entryIndex].val
        elif entryIndex == 1:
            self.cam.orientation = self.inputVariables[entryIndex]

    def handleFOV(self, event): 
        if 0 < int(event.text) < 180: #tan(90) is undefined so we try to prevent this case
            self.cam.fov = 180 - int(event.text) 
            self.cam.projection_matrix = self.cam.get_projection_matrix()
            temp = [matrixline.round(3).tolist() for matrixline in self.cam.projection_matrix.val]
            [self.projlines[i].set_text(f'{temp[i]}') for i in range(4)]
        self.FOVEntry.set_text(str(180 - self.cam.fov))

    def setText(self, keys): #sets the text entry boxes for the variable panel
        orientation = list(map(trunc, self.cam.orientation[:2]))
        self.inputVariables = [str(self.cam.position), str(orientation)]
        if self.variablePanel.visible: #updates variable panel when camera moves
            if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d] or keys[pygame.K_q] or keys[pygame.K_e]:
                self.variableEntries[0].set_text(self.inputVariables[0])
            if cameraTurning:
                self.variableEntries[1].set_text(self.inputVariables[1])
        elif self.matrixPanel.visible:
            self.updateMatrix()

    def update(self, event, keys):
        global modelMoveFlag, objectAddedFlag

        self.setText(keys)
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element in self.variableEntries:
                i = self.variableEntries.index(event.ui_element)
                self.handleTextEntry(event, i)
            elif event.ui_element == self.FOVEntry:
                self.handleFOV(event)

        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.cam_menu:
                self.switchPanel(event)
            elif event.ui_element == self.model_choice:
                self.objectIndex = self.objectNames.index(event.text)
                self.cam.target = scene.objects[self.objectIndex].position

        if modelMoveFlag:
            self.cam.target = scene.objects[self.objectIndex].position
            modelMoveFlag = False

        if objectChangeFlag:
            self.model_choice.kill()
            self.makeObjectsMenu(scene.objects)

class import_tab(tabGUI):
    def __init__(self):
        super().__init__(pygame.Rect((-90, 5), (100,30)), 'Import')
        self.addObjectPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((0, 0), (480, 400)),
                                                                manager=manager, container=self.panel)
        tabGUI.label(pygame.Rect((90, 30), (100,30)), 'Add Object', self.addObjectPanel)
        tabGUI.label(pygame.Rect((20, 75), (100,30)), 'Name:', self.addObjectPanel)
        tabGUI.label(pygame.Rect((20, 120), (100,30)), 'Select Type:', self.addObjectPanel)

        self.removeObjectPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((0, 400), (480, 400)),
                                                                manager=manager, container=self.panel)
        tabGUI.label(pygame.Rect((90, 30), (100,30)), 'Delete Object', self.removeObjectPanel)
        tabGUI.label(pygame.Rect((15, 80), (100,30)), 'Select Object:', self.removeObjectPanel)
        self.addIndex = 0

        self.nameInput = ''
        self.nameInputLine = tabGUI.textEntry(pygame.Rect((170, 75), (100, 30)), '', self.addObjectPanel)
        self.nameInputLine.set_allowed_characters('alpha_numeric')
        self.nameInputLine.set_text_length_limit(20)

        self.objectLineUp = ['Cube', 'Square', 'Sphere', 'Cylinder', 'Teapot', 'Cow']
        self.modelSelect = tabGUI.dropDown(pygame.Rect((170, 120), (100,30)), self.objectLineUp,
                                            'Cube', self.addObjectPanel)
        self.addObjectButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((170, 170), (100, 30)),
                                            text='Add',
                                            manager=manager,
                                            container=self.addObjectPanel,
                                            command=self.addObject)
        self.delObjectButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((112, 150), (75, 30)),
                                            text='Delete',
                                            manager=manager,
                                            container=self.removeObjectPanel,
                                            command=self.delObject)
        self.browseFilesButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 170), (100, 30)),
                                            text='Browse',
                                            manager=manager,
                                            container=self.addObjectPanel,
                                            command=self.fileSelect)
        self.makeObjectsMenu(scene.objects)
        
    def hide(self):
        self.panel.hide()
    
    def show(self):
        self.panel.show()
        
    def makeObjectsMenu(self, objectlist):
        objectNames = [model.name for model in objectlist]
        self.objectNames = objectNames
        self.model_choice = tabGUI.dropDown(pygame.Rect((170, 80), (100, 30)),
                                        objectNames, 
                                        objectNames[0], self.removeObjectPanel) 
        self.delIndex = 0

    def fileSelect(self):
        pygame_gui.windows.UIFileDialog(pygame.Rect((0, 0), (1000, 800)), manager, 'Select File (.obj only)')
        
    def addObject(self):
        global objectChangeFlag
        if self.nameInput == '' or self.nameInput in self.objectNames: #don't permit empty or already existing names
            return
        if self.addIndex == 0:
            scene.objects.append(Cube(name=self.nameInput))
        elif self.addIndex == 1:
            scene.objects.append(Square(name=self.nameInput))
        elif self.addIndex == 2:
            scene.objects.append(Sphere(name=self.nameInput))
        elif self.addIndex == 3:
            scene.objects.append(Cylinder(name=self.nameInput))
        elif self.addIndex == 4:
            scene.objects.append(Teapot(name=self.nameInput))
        elif self.addIndex == 5:
            scene.objects.append(Cow(name=self.nameInput))
        objectChangeFlag = True

    def delObject(self):
        global objectChangeFlag
        if len(scene.objects) > 1:
            scene.objects.pop(self.delIndex)
            objectChangeFlag = True

    def validatePath(self, path):
        if path.endswith('.obj'):
            return True
        return False

    def update(self, event):
        global objectChangeFlag
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.modelSelect:
                self.addIndex = self.objectLineUp.index(event.text)
            elif event.ui_element == self.model_choice:
                self.delIndex = self.objectNames.index(event.text)

        elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.nameInputLine:
                self.nameInput = event.text

        elif event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
            path = event.text
            if self.validatePath(path) and self.nameInput != '' and self.nameInput not in self.objectNames:
                try:
                    newObject = Model(Vec3.from_list([0, 0, 0]), [0, 0, 0], [1, 1, 1], path, self.nameInput)
                    scene.objects.append(newObject)
                    objectChangeFlag = True
                except:
                    pygame_gui.windows.ui_message_window.UIMessageWindow(pygame.Rect((0, 0), (500, 400)), 'File invalid', 
                                                                         manager=manager, window_title='Error!')
            elif self.nameInput == '' or self.nameInput in self.objectNames:
                pygame_gui.windows.ui_message_window.UIMessageWindow(pygame.Rect((0, 0), (500, 400)), 'Object name is invalid', 
                                                                     manager=manager, window_title='Error!')
            elif not self.validatePath(path):
                pygame_gui.windows.ui_message_window.UIMessageWindow(pygame.Rect((0, 0), (500, 400)), 'File invalid [must be .obj]', 
                                                                     manager=manager, window_title='Error!')

        if objectChangeFlag:
            self.model_choice.kill()
            self.makeObjectsMenu(scene.objects)

scene = Scene(height)
scene.objects = [Cube(Vec3.from_list([0, 0, -2]), [0, 0, 0], [1, 1, 1], name='Cube1')]

objects_tab = objects_tab(scene.objects, 0)
camera_tab = camera_tab(scene.objects, scene.camera)     
import_tab = import_tab()

def main():
    global cameraTurning, modelMoveFlag, objectChangeFlag, writingFlag, cameraMode

    cameraTurning = False
    modelMoveFlag = False
    objectChangeFlag = False
    writingFlag = False

    cameraMode = 1

    crashed = False
    dt = 1/60 #time step

    while not crashed:

        clock.tick(60)
        framerate = clock.get_fps()
        if framerate != 0:
            dt = 1/framerate

        keys = pygame.key.get_pressed()
        writingFlag = False
        if import_tab.nameInputLine.hovered:
            writingFlag = True #stops camera from moving while typing a name in
        for event in pygame.event.get():
            import_tab.update(event)
            objects_tab.update(event)
            camera_tab.update(event, keys)
            objectChangeFlag = False

            if event.type == pygame.QUIT:
                crashed = True
        
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                scene.camera.mouseLock = False
                cameraTurning = False
                scene.camera.lockmouse()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: 
                pygame.mouse.get_rel()
                scene.camera.mouseLock = True
                cameraTurning = True
                scene.camera.lockmouse()

            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == objects_tab.tab:
                    if objects_tab.panel.visible:
                        objects_tab.hide()
                    else:
                        camera_tab.hide()
                        import_tab.hide()
                        objects_tab.show()
                elif event.ui_element == camera_tab.tab:
                    if camera_tab.panel.visible:
                        camera_tab.hide()
                    else:
                        camera_tab.show()
                        import_tab.hide()
                        objects_tab.hide()
                elif event.ui_element == import_tab.tab:
                    if import_tab.panel.visible:
                        import_tab.hide()
                    else:
                        import_tab.show()
                        camera_tab.hide()
                        objects_tab.hide()

            manager.process_events(event)
        manager.update(dt)

        pygame.display.set_caption(f'{framerate:.0f} fps')
        screen.blit(bg, (0, 0))
        scene.update(keys, cameraMode, writingFlag, screen, bg, dt)
        manager.draw_ui(screen)

        pygame.display.update()
        pygame.display.flip()

if __name__ == '__main__':
    main()







    



