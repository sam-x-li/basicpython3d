import numpy as np
from math import sin, cos, tan, pi, radians
from abc import ABC, abstractmethod

class Vector(ABC):

    def __init__(self):
        self.val = 0

    @classmethod
    def from_list(cls, l: list): #generates a Vector from a normal list
        result = cls.from_array(np.array(l))
        return result
    
    @classmethod
    def from_array(cls, array: np.array): #generates a Vector directly from the numpy array
        result = cls()
        result.val = array
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
    
    def __sub__(self, other):
        result = Vector()
        result.val = self.val - other.val
        return result
    
    def __mul__(self, other: float): #scalar multiplication only
        result = Vector()
        result.val = self.val * other
        return result
    
    def length(self):
        return np.linalg.norm(self.val)
    
    def normalised(self):
        return self * (1 / self.length()) 
    
    @staticmethod
    def distance(a, b):
        return np.linalg.norm(b - a)
    
class Vec2(Vector):

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f'Vec2 --> {self.val}'
    
    def __add__(self, other):
        result = Vec2()
        result.val = self.val + other.val
        return result
    
    def __mul__(self, other: float): #scalar multiplication only
        result = Vec2.from_array(self.val * other)
        return result

    def toTuple(self):
        return tuple(self.val)

class Vec3(Vector):

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
    def cross(cls, a, b): #between 3D vectors only
        result = cls()
        result.val = np.cross(a.val, b.val)
        return result
    
    def homogeneous(self):
        result = Vec4()
        result.val = np.append(self.val, 1)
        return result
    
    def get2D(self):
        return self.val[:2]
    
    def toTuple(self, dp=0):
        return tuple(self.val.round(dp))
    
class Vec4(Vector):

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
    
    def __mul__(self, other: float): #scalar multiplication only
        result = Vec4.from_array(self.val * other)
        return result

    def matmul(self, matrix): 
        return Vec4.from_array(np.matmul(matrix.val, self.val))

    def pDivide(self): #perspective divide
        w = self.val[3]
        if w == 0:
            raise ValueError
        result = Vec3.from_array(self.val[:3] / w )
        return result

    def toVec3(self): #assumes w = 1
        return Vec3.from_array(self.val[:3])
    

class Matrix:
    def __init__(self):
        self.val = 0 

    @classmethod
    def from_list(cls, l: list): #generates a Matrix from a normal list
        result = cls.from_array(np.array(l).astype(float))
        return result
    
    @classmethod
    def from_array(cls, array: np.array): #generates a Matrix directly from the numpy array
        result = cls()
        result.val = array
        return result
    
    def __str__(self):
        return f'{self.val}'
    
    def __repr__(self):
        return f'Matrix --> {self.val}'

    def __mul__(self, other):
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
    def rotate(cls, orientation, neg=False):
        x, y, z = orientation
        if neg:
            x, y, z = -1 * x, -1 * y, -1 * z
        roll = cls.roll(z)
        pitch = cls.pitch(x)
        yaw = cls.yaw(y)
        result = yaw * pitch * roll
        return result
    
    @classmethod
    def rotate2(cls, orientation, neg=False): #camera does not roll, therefore cheaper
        x, y, z = orientation
        if neg:
            x, y, z = -1 * x, -1 * y, -1 * z
        #roll = cls.roll(phi)
        pitch = cls.pitch(x)
        yaw = cls.yaw(y)
        result = pitch * yaw
        return result
    
    @classmethod
    def translate(cls, vector:Vec3): #translates by a vector (represented using a Vec3 instance)
        x, y, z = vector.val[0], vector.val[1], vector.val[2]
        result = cls()
        result.val = [[1, 0, 0, x],
                      [0, 1, 0, y],
                      [0, 0, 1, z],
                      [0, 0, 0, 1]]
        return result
    
    @classmethod
    def bunch(cls, vertices: tuple): #bunches a tuple of vectors together into a single matrix 
        temp = [vertex.val for vertex in vertices]
        temp = cls.from_array(np.column_stack(temp))
        return temp
    
    @staticmethod
    def unbunch(matrix): #unbunches matrix into a tuple of NUMPY arrays
        n = matrix.val.shape[1]
        return Vec4.batch_create(np.hsplit(matrix.val, n))
