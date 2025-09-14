from vectormaths import *

class Model:
    def __init__(self, position:Vec3, orientation:list, scaling:list, path, name='Object'):
        self.position = position
        self.orientation = orientation
        self.scaling = scaling
        self.vectors, self.tris = self.loadobj(path)
        self.clipvectors = []
        self.type = None
        self.name = name
        self.modelMatrix = self.get_modelMatrix() #defined a getter for GUI functionality

    def __repr__(self): 
        return f'''Model: {self.type}
        position = {self.position.val.round(2)} 
        orientation = {self.orientation}
        scaling = {self.scaling}'''
                    
    def loadobj(self, path): #reads .obj file, converts into model
        vertices = []
        tris = []
        with open(path, 'r') as file:
            data = file.read()
        lines = data.split('\n')
        for line in lines:
            line = line.split(' ')
            if line[0] == 'v':
                x, y, z = float(line[1]), float(line[2]), float(line[3])
                vertices.append(Vec4.from_list([x, y, z, 1]))
            elif line[0] == 'f':
                a, b, c = line[1].split('/'), line[2].split('/'), line[3].split('/')
                tris.append(self.Tri((int(a[0]) - 1, int(b[0]) - 1, int(c[0]) - 1)))
        return vertices, tris
    
    def invert(self): #swaps directions the tris face
        for tri in self.tris:
            newpointers = (tri.pointers[1], tri.pointers[0], tri.pointers[2])
            tri.pointers = newpointers

    def get_modelMatrix(self): 
        scale = Matrix.scale(self.scaling)
        rotation = Matrix.rotate(self.orientation)
        translation = Matrix.translate(self.position)
        return translation * rotation * scale
    
    def getValidTris(self): #finds tris that are fully onscreen
        validTris = []
        for tri in self.tris:
            temp = [self.clipvectors[pointer] for pointer in tri.pointers]
            if all(temp): 
                newtri = self.clipTri(temp)
                validTris.append(newtri)
        return validTris
    
    class Tri:
        def __init__(self, pointers):
            self.pointers = pointers
            self.clip_vectors = [] 
        
    class clipTri: #tri in clip space
        def __init__(self, clip_vectors):
            self.clip_vectors = clip_vectors
            self.centroid = (clip_vectors[0] + clip_vectors[1] + clip_vectors[2]) * (1/3)
                
        def getNormal(self, reverse=True):  
            u = self.clip_vectors[1] - self.clip_vectors[0]
            v = self.clip_vectors[2] - self.clip_vectors[0]
            normal = Vec3.cross(u, v)
            if reverse:
                normal *= -1
            return normal + self.centroid
        
        def getSign(self): #returns the sign of the normal, to check facing direction
            a, b, c = self.clip_vectors
            ab = b.val - a.val
            ac = c.val - a.val
            sign = ab[0] * ac[1] - ac[0] * ab[1] 
            return sign
        
        def getDepth(self):
            centroid_z = self.centroid.val[2]
            return centroid_z 
        
        def get2D(self):
            result = [vector.get2D() for vector in self.clip_vectors]
            return result
        
        @staticmethod
        def cull(tris):
            result = [tri for tri in tris if tri.getSign() > 0] # camera faces negative z axis, so if the normal is positive
            return result                                       # it points towards the camera (so you can see it)

class Cube(Model): #preset models
    def __init__(self, position:Vec3 = Vec3.from_list([0, 0, 0]), orientation:tuple = (0, 0, 0), scaling:tuple = (1, 1, 1), name='Object'):
        super().__init__(position, orientation, scaling, path='basicpython3d\assets\cube.txt', name=name)
        self.type = 'Cube'
        
class Square(Model):
    def __init__(self, position:Vec3 = Vec3.from_list([0, 0, 0]), orientation:tuple = (0, 0, 0), scaling:tuple = (1, 1, 1), name='Object'):
        super().__init__(position, orientation, scaling, path='basicpython3d\assets\square.txt', name=name)
        self.type = 'Square'
        self.invert()

class Sphere(Model):
    def __init__(self, position:Vec3 = Vec3.from_list([0, 0, 0]), orientation:tuple = (0, 0, 0), scaling:tuple = (1, 1, 1), name='Object'):
        super().__init__(position, orientation, scaling, path='basicpython3d\assets\sphere.txt', name=name)
        self.type = 'Sphere'

class Cylinder(Model):
    def __init__(self, position:Vec3 = Vec3.from_list([0, 0, 0]), orientation:tuple = (0, 0, 0), scaling:tuple = (1, 1, 1), name='Object'):
        super().__init__(position, orientation, scaling, path='basicpython3d\assets\cylinder.obj', name=name)
        self.type = 'Cylinder'

class Teapot(Model):
    def __init__(self, position:Vec3 = Vec3.from_list([0, 0, 0]), orientation:tuple = (0, 0, 0), scaling:tuple = (1, 1, 1), name='Object'):
        super().__init__(position, orientation, scaling, path='basicpython3d\assets\tea2.obj', name=name)
        self.type = 'Teapot'

class Cow(Model):
    def __init__(self, position:Vec3 = Vec3.from_list([0, 0, 0]), orientation:tuple = (0, 0, 0), scaling:tuple = (1, 1, 1), name='Object'):
        super().__init__(position, orientation, scaling, path='basicpython3d\assets\cow.txt', name=name)
        self.type = 'Cow'

