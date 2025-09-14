from model import * 
import pygame

class Camera: 
    def __init__(self, position:Vec3, orientation:list, height:int, fov:float = 90, near:float = 1, far:float = 100):
        self.position = position
        self.orientation = orientation
        self.fov = fov
        self.near = near
        self.far = far
        self.target = Vec3()
        self.forwardVector = Vec3.from_list([0, 0, -1]) #dictates direction of movement
        self.rightVector = Vec3.from_list([1, 0, 0])
        self.upVector = Vec3.from_list([0, 1, 0])
        self.moveSpeed = 5
        self.turnSpeed = 90
        self.view_matrix = self.get_view_matrix()
        self.height = height #height of screen, needed for projection matrix
        self.projection_matrix = self.get_projection_matrix()
        self.mouseLock = False

    def get_view_matrix(self):
        translation = Matrix.translate(self.position * -1)
        rotation = Matrix.rotate2(self.orientation, neg=True)
        yaw = Matrix.yaw(self.orientation[1])
        viewMatrix = rotation * translation
        self.forwardVector = Vec4.from_list([0, 0, -1, 1]).matmul(yaw).toVec3() #calculates the direction vector for the front of the camera
        self.rightVector =  Vec3.cross(self.upVector, self.forwardVector) * -1 
        return viewMatrix
    
    def get_projection_matrix(self): 
        t = 1 / tan(radians(self.fov/2))
        right = self.near * t
        top = right * self.height / 800
        result = Matrix.from_list([
            [self.near/right, 0.0, 0.0, 0.0],
            [0, self.near/top, 0.0, 0.0],
            [0.0, 0.0, -(self.far + self.near) / (self.far - self.near), -2 * (self.far * self.near) / (self.far - self.near)],
            [0.0, 0.0, -1, 0.0]])
        return result
    
    def lookAt(self):
        up = Vec3.from_list([0, 1, 0])
        forward = (self.position - self.target).normalised()
        self.forwardVector = forward * -1
        left = Vec3.cross(up, forward).normalised()
        self.rightVector = left
        up = Vec3.cross(forward, left)
        self.upVector = up
        mat = Matrix()
        mat.val = np.array([[left.val[0], left.val[1], left.val[2], -1 * Vec3.dot(left, self.position)],
                   [up.val[0], up.val[1], up.val[2], -1 * Vec3.dot(up, self.position)],
                   [forward.val[0], forward.val[1], forward.val[2], -1 * Vec3.dot(forward, self.position)],
                   [0, 0, 0, 1]])
        return mat
    
    def fixVectors(self): #resets vectors to default
        self.forwardVector = Vec3.from_list([0, 0, -1])
        self.rightVector = Vec3.from_list([1, 0, 0])
        self.upVector = Vec3.from_list([0, 1, 0])

    def moveForward(self, dt):
        self.position += self.forwardVector * self.moveSpeed * dt

    def moveLeft(self, dt):
        self.position -= self.rightVector * self.moveSpeed * dt
    
    def moveRight(self, dt):
        self.position += self.rightVector * self.moveSpeed * dt
    
    def moveBackward(self, dt):
        self.position -= self.forwardVector * self.moveSpeed * dt
    
    def moveDown(self, dt):
        self.position -= self.upVector * self.moveSpeed * dt
    
    def moveUp(self, dt):
        self.position += self.upVector * self.moveSpeed * dt

    def update(self, keys, cameraMode, writingFlag, dt):
        if writingFlag:
            return #prevents camera from moving while typing into GUI
        if keys[pygame.K_w]:
            self.moveForward(dt)
        if keys[pygame.K_a]:
            self.moveLeft(dt)
        if keys[pygame.K_d]:
            self.moveRight(dt)
        if keys[pygame.K_s]:
            self.moveBackward(dt)
        if keys[pygame.K_e]:
            self.moveUp(dt)
        if keys[pygame.K_q]:
            self.moveDown(dt)
        if keys[pygame.K_UP]:
            self.orientation[0] += self.turnSpeed * dt
        if keys[pygame.K_DOWN]:
            self.orientation[0] -= self.turnSpeed * dt
        if keys[pygame.K_RIGHT]:
            self.orientation[1] = (self.orientation[1] - self.turnSpeed * dt) % 360
        if keys[pygame.K_LEFT]:
            self.orientation[1] = (self.orientation[1] + self.turnSpeed * dt) % 360

        if self.mouseLock:
            self.mouseUpdate()

        if self.orientation[0] > 75: 
            self.orientation[0] = 75
        elif self.orientation[0] < -75:
            self.orientation[0] = -75

        if cameraMode == 1:
            self.view_matrix = self.get_view_matrix()
        elif cameraMode == 2:
            self.view_matrix = self.lookAt()


    def lockmouse(self): #locks mouse when rotating camera
        if self.mouseLock:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)
        else:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)

    def mouseUpdate(self): 
        movement = np.array(pygame.mouse.get_rel()) #stores change in position as a vector
        self.orientation[0] -= 0.1 * movement[1]
        self.orientation[1] = (self.orientation[1] - 0.1 * movement[0]) % 360


