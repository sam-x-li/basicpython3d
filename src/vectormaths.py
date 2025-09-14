import numpy as np
from math import sin, cos, radians, tan
from abc import ABC, abstractmethod

class Vector(ABC): 
    size = None

    def __init__(self):
        self.val = 0

    @classmethod 
    def from_list(cls, l: list): #generates a Vector from a  list
        result = cls.from_array(np.array(l))
        return result
    
    @classmethod
    def from_array(cls, array: np.array): #generates a Vector directly from the numpy array
        result = cls()
        if not np.all(np.isreal(array)): #isreal() returns True for real numbers only
            raise TypeError("Incompatible datatypes") 
        result.val = array
        if len(result.val) != cls.size: #i.e. if a 4D vector incorrectly tries to have 5 components 
            raise TypeError("Incorrect dimensionality") 
        return result
    
    def __str__(self):
        return f'{self.val}'
    
    @abstractmethod 
    def __repr__(self): 
        return f'Vector --> {self.val}'
    
    @abstractmethod
    def __add__(self, other):
        result = Vector()
        result.val = self.val + other.val
        return result
    
    @abstractmethod
    def __sub__(self, other):
        result = Vector()
        result.val = self.val - other.val
        return result
    
    @abstractmethod
    def __mul__(self, other: float): #scalar multiplication only
        result = Vector()
        result.val = self.val * other
        return result
    
    def __rmul__(self, other: float): 
        return self * other 
    
    def length(self):
        return np.linalg.norm(self.val) #euclidean distance 
    
    def normalised(self):
        return self * (1 / self.length()) 
    
    @staticmethod
    def distance(a, b):
        return np.linalg.norm(b.val - a.val)
    
class Vec2(Vector): 
    size = 2
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f'Vec2 --> {self.val}'
    
    def __add__(self, other):
        result = Vec2()
        result.val = self.val + other.val
        return result
    
    def __sub__(self, other):
        result = Vec2()
        result.val = self.val - other.val
        return result
    
    def __mul__(self, other: float): #scalar multiplication only
        result = Vec2.from_array(self.val * other)
        return result

    def toTuple(self): #for screen coordinates
        return tuple(self.val)

class Vec3(Vector):
    size = 3
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f'Vec3 --> {self.val}'
    
    def __add__(self, other):
        result = Vec3()
        result.val = self.val + other.val
        return result
    
    def __sub__(self, other):
        result = Vec3()
        result.val = self.val - other.val
        return result
    
    def __mul__(self, other: float): #scalar multiplication only
        result = Vec3.from_array(self.val * other)
        return result
    
    @classmethod
    def dot(cls, a, b):
        return np.dot(a.val, b.val)
    
    @classmethod
    def cross(cls, a, b): #for 3D vectors only
        result = cls()
        result.val = np.cross(a.val, b.val)
        return result
    
    def homogeneous(self): #adds homogeneous coordinate w = 1 to the end
        result = Vec4()
        result.val = np.append(self.val, 1)
        return result
    
    def get2D(self):
        return self.val[:2]
    
    def toTuple(self, dp=0):
        return tuple(self.val.round(dp))
    
class Vec4(Vector):
    size = 4
    def __init__(self):
        super().__init__()
        
    def __repr__(self):
        return f'Vec4 --> {self.val}'
    
    @classmethod
    def batch_create(cls, vectors): #makes a list of Vec4s from a list of arrays
        return [cls.from_array(np.transpose(vector)[0]) for vector in vectors]
    
    def __add__(self, other):
        result = Vec4()
        result.val = self.val + other.val
        return result
    
    def __sub__(self, other):
        result = Vec4()
        result.val = self.val - other.val
        return result
    
    def __mul__(self, other: float): #scalar multiplication only
        result = Vec4.from_array(self.val * other)
        return result

    def matmul(self, matrix): 
        return Vec4.from_array(np.matmul(matrix.val, self.val))

    def pDivide(self): #perspective divide, 'flattens' to 2D
        w = self.val[3]
        if w == 0:
            raise ValueError
        result = Vec3.from_array(self.val[:3] / w )
        return result

    def toVec3(self): #assumes w=1
        return Vec3.from_array(self.val[:3])
    

class Matrix: 
    def __init__(self):
        self.val = 0 

    @classmethod
    def from_list(cls, l: list): #generates a Matrix from a list
        result = cls.from_array(np.array(l).astype(float))
        return result
    
    @classmethod
    def from_array(cls, array: np.array): #generates a Matrix directly from the numpy array
        if not np.all(np.isreal(array)): #isreal() returns True for real numbers only
            raise TypeError("Incompatible datatypes") 
        if array.ndim != 2:  #checks if 2D array
            raise TypeError("Incorrect dimensionality")
        if not all(len(row) == len(array[0]) for row in array):
            raise TypeError("Mismatched row lengths")
        result = cls()
        result.val = array
        return result
    
    def __str__(self):
        return f'{self.val}'
    
    def __repr__(self):
        return f'Matrix --> {self.val}'

    def __mul__(self, other): #matrix multiplication 
        result = Matrix()
        result.val = np.matmul(self.val, other.val)
        return result
    
    def __add__(self, other):
        result = Matrix()
        result.val = self.val + other.val 
        return result
    
    def __sub__(self, other):
        result = Matrix()
        result.val = self.val - other.val
        return result
    
    def scalar_mul(self, scalar: float):
        result = Matrix()
        result.val = scalar * self.val
        return result
    
    @classmethod
    def scale(cls, scaling):
        x, y, z = scaling
        result = cls()
        result.val = np.array([[x, 0, 0, 0],
                               [0, y, 0, 0],
                               [0, 0, z, 0],
                               [0, 0, 0, 1]])
        return result
    
    @classmethod
    def roll(cls, phi):
        #rotates about z axis
        #angles given in degrees 
        s = sin(radians(phi))
        c = cos(radians(phi))
        result = cls()
        result.val = np.array([[c, -s, 0, 0],
                               [s, c, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])
        return result

    @classmethod
    def yaw(cls, theta):
        #rotates about y axis
        s = sin(radians(theta))
        c = cos(radians(theta))
        result = cls()
        result.val = np.array([[c, 0, s, 0],
                               [0, 1, 0, 0],
                               [-s, 0, c, 0],
                               [0, 0, 0, 1]])
        return result
        
    @classmethod
    def pitch(cls, psi):
        #rotates about x axis
        s = sin(radians(psi))
        c = cos(radians(psi))
        result = cls()
        result.val = np.array([[1, 0, 0, 0],
                               [0, c, -s, 0],
                               [0, s, c, 0],
                               [0, 0, 0, 1]])
        return result
    
    @classmethod
    def rotate(cls, orientation, neg=False): #rotates about all 3 axes
        x, y, z = orientation
        if neg:
            x, y, z = -1 * x, -1 * y, -1 * z
        roll = cls.roll(z)
        pitch = cls.pitch(x)
        yaw = cls.yaw(y)
        result = yaw * pitch * roll
        return result
    
    @classmethod
    def rotate2(cls, orientation, neg=False): #camera does not roll, so only 2 axes
        x, y, z = orientation
        if neg:
            x, y, z = -1 * x, -1 * y, -1 * z
        #roll = cls.roll(phi)
        pitch = cls.pitch(x)
        yaw = cls.yaw(y)
        result = pitch * yaw
        return result
    
    @classmethod
    def translate(cls, vector:Vec3): #translates by a vector represented by a Vec3
        x, y, z = vector.val[0], vector.val[1], vector.val[2]
        result = cls()
        result.val = [[1, 0, 0, x],
                      [0, 1, 0, y],
                      [0, 0, 1, z],
                      [0, 0, 0, 1]]
        return result
    
    @classmethod
    def bunch(cls, vertices: tuple): #concatenates a tuple of Vec3s together into a single matrix
        temp = [vertex.val for vertex in vertices]
        temp = cls.from_array(np.column_stack(temp))
        return temp
    
    @staticmethod
    def unbunch(matrix): #breaks up matrix into a tuple of numpy arrays
        n = matrix.val.shape[1]
        return Vec4.batch_create(np.hsplit(matrix.val, n))
