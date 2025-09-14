from camera import * 

class Scene: 
    def __init__(self, height):
        self.camera = Camera(Vec3.from_list([0, 0, 0]), [0, 0, 0], height)
        self.objects = []
        self.height = height
        
    def clip(self, vectors): #clips points that are offscreen
        result = []
        for vector in vectors:
            w = vector.val[3]
            if w == 0:
                result.append(False) 
                continue
            for element in vector.val[:3]:
                if not -w <= element <= w:
                    result.append(False)
                    break
            else: 
                result.append(vector.pDivide()) 
            continue
        return result
    
    def full_transform(self):
        viewMatrix = self.camera.view_matrix
        projectionMatrix = self.camera.projection_matrix
        pv = projectionMatrix * viewMatrix
        for model in self.objects:
            bunch = Matrix.bunch(model.vectors) #vectors are grouped so only 1 matrix multiplication needed
            clip_bunch = pv * model.modelMatrix * bunch
            clipvectors = Matrix.unbunch(clip_bunch)
            model.clipvectors = self.clip(clipvectors)

    def set_target(self, i):
        self.camera.target = self.objects[i].position

    def get_tris(self): 
        def depth(tri): 
            return tri.getDepth() 
        tris = np.concatenate([model.getValidTris() for model in self.objects]) 
        tris = Model.clipTri.cull(tris) #removes tris facing away from the camera
        temp = np.array([depth(tri) for tri in tris]) 
        indexes = np.argsort(temp) #sorts by depth ascending
        return indexes[::-1], tris #then reverses the indexes to get it descending, painter's algorithm

    def align(self, points): #viewport transform, maps from NDC to screen
        result = [np.multiply(point, np.array([800/2, -self.height/2])) + np.array([800/2, self.height/2]) for point in points]
        return result   
    
    def draw(self, indexes, tris, screen, bg):
        for i in indexes:
            points = self.align(tris[i].get2D()) #finds 2D coordinates of each tri
            pygame.draw.polygon(screen, (255, 255, 255), points)
            pygame.draw.lines(screen, (0, 0, 0), True, points, 1) 
  
    def update(self, keys, cameraMode, writingFlag, screen, bg, dt):
        self.camera.update(keys, cameraMode, writingFlag, dt)
        self.full_transform()
        indexes, tris = self.get_tris()
        screen.lock() 
        self.draw(indexes, tris, screen, bg)
        screen.unlock()
