import time
import random

half_width = 800
scene = []


class Barrier():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
    def display(self):
        push()
        fill(255)
        stroke(255)
        strokeWeight(2)
        line(self.x1, self.y1, self.x2, self.y2)
        pop()
    def returnProp(self):
        return [self.x1, self.y1, self.x2, self.y2]
    
    
class Emitter():
    def __init__(self):
        pass
        
class Ray():
    def __init__(self, x, y, angle):
        self.pos = PVector(x, y)
        self.angle = angle
        self.dir = PVector.fromAngle(radians(self.angle))
        
        self.closestWalldist = half_width*height # initialized value
        self.currentWall = 0
        self.closestWallVector = PVector(0,0)
        self.wallDists = {}
    def display(self):
        global mouseVector
        stroke(255)
        #mouseVector = PVector(mouseX-self.pos.x, mouseY-self.pos.y)
        #mouseVector.normalize()
        #line(self.pos.x, self.pos.y, (self.pos.x+(mouseVector.x)*100), (self.pos.y+(mouseVector.y)*100))
        line(self.pos.x, self.pos.y, (self.pos.x+(self.dir.x)), (self.pos.y+(self.dir.y)))
        if mouseX > half_width:
            noLoop()
        else:
            self.pos.x = mouseX
            self.pos.y = mouseY
    def checkCollision(self, wall):
        self.record = 0
        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.pos.x + self.dir.x
        y4 = self.pos.y + self.dir.y
        wallProps = wall.returnProp()
        x1 = wallProps[0]
        y1 = wallProps[1]
        x2 = wallProps[2]
        y2 = wallProps[3]
        
        den = ((x1 - x2)*(y3-y4)-(y1-y2) * (x3-x4))
        if den == 0:
            return
        t = ((x1 - x3) *(y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = ((x2 - x1)*(y1 - y3) - (y2-y1)*(x1-x3)) / den
        
        if t > 0 and t < 1 and u > 0:
            self.currentWall = PVector((x1 + t*(x2 -x1)), (y1 + t*(y2-y1)))
            #self.currentWall = PVector(x3 + u*(x4-x3), y3 + u * (y4 - y3))
            self.anglefromPlane = degrees(PVector.angleBetween(self.dir, camera_plane))
            if self.anglefromPlane > 90:
                self.anglefromPlane -= (self.anglefromPlane-90)*2
            #self.anglefromRay = 90 - self.anglefromPlane
            #line(self.currentWall.x, self.currentWall.y, self.currentWall.x + (self.camera_plane_perp_vector.x *100), self.currentWall.y + (self.camera_plane_perp_vector.y *100))
        
            self.currentWalldistEU = dist(self.pos.x, self.pos.y, self.currentWall.x, self.currentWall.y)
            self.currentWalldist = sin(radians(self.anglefromPlane))* self.currentWalldistEU
            print(self.anglefromPlane , self.currentWalldistEU, self.currentWalldist)
            self.wallDists[self.currentWalldist] = self.currentWall
            
            #print(dist(self.pos.x, self.pos.y, self.currentWall.x, self.currentWall.y))
            #if self.closestWalldist > dist(self.pos.x, self.pos.y, self.currentWall.x, self.currentWall.y):
             #   self.closestWalldist = dist(self.pos.x, self.pos.y, self.currentWall.x, self.currentWall.y)
              #  self.closestWallVector = self.currentWall
            #return PVector((x1 + t*(x2 -x1)), (y1 + t*(y2-y1)))
            #line(self.pos.x, self.pos.y, (x1 + t*(x2 -x1)), (y1 + t*(y2-y1)))
            #ellipse((x1 + t*(x2 -x1)), (y1 + t*(y2-y1)), 4, 4)
        else:
            return
    def drawRay(self):
        for i in sorted(self.wallDists):
            self.closestWallVector = self.wallDists[i]
            self.closestWalldist = i
            break
        #print(self.closestWallVector)
        if self.closestWalldist != half_width*height:
            line(self.pos.x, self.pos.y, self.closestWallVector.x, self.closestWallVector.y)
            scene.append(self.closestWalldist)
        else:
        
            line(self.pos.x, self.pos.y, (self.pos.x+(self.dir.x)*8000), (self.pos.y+(self.dir.y)*8000))
            scene.append(height)
            
class Scene():
    def drawScene(self, scene):
        push()
        translate(half_width,height/2)
        rectMode(CENTER)
        #print(scene)
        x_coord = (half_width/len(scene))
        
        noStroke()
        for sc in scene:
            fill(map(sc**2, 0, height**2, 255, 0))
            rect(x_coord, 0, (half_width/len(scene))+1, map(sc, 0, height, height, 0)) #(half_width/len(scene))
            #rect(0, 0, 10, 10)
            x_coord += (half_width/len(scene))
        
        pop()
        

def setup():
    global barrier
    global ray
    global mouseVector
    global barriers
    global rays
    global sceneObj
    global middle_vector
    
    barriers = []
    rays = []
    size(1600, 800)
    sceneObj = Scene()
    background(0)
    #barriers.append(Barrier(350, 500, 150, 500))
    #barriers.append(Barrier(0, 0, 0, height))
    #barriers.append(Barrier(0, 0, 0, half_width))
    #barriers.append(Barrier(half_width, height, 0, height))
    barriers.append(Barrier(half_width, height, half_width, 0))
    #barriers.append(Barrier(350, 150, 150, 150))
    
    for i in range(5):
        barriers.append(Barrier(random.randint(0,half_width),random.randint(0,height),random.randint(0,half_width),random.randint(0,height)))
    for i in range(0, 60, 1):
        rays.append(Ray(half_width/2, height/2, i))
    middle_vector = rays[(len(rays)/2)-1].dir
    #print(rays[(len(rays)/2)-1].dir)
    
def draw():
    background(0)
    global scene
    global camera_plane
    
    scene = []
    camera_plane = PVector(middle_vector.y, -(middle_vector.x))
    
    line(mouseX-(camera_plane.x*100), mouseY-(camera_plane.y*100), mouseX+(camera_plane.x*100), mouseY+(camera_plane.y*100))
    #line(mouseX, mouseY, mouseX + (middle_vector.x *100), mouseY + (middle_vector.y * 100))
    #print(camera_plane)
    for ray in rays:
        
        ray.display()
        ray.closestWalldist = half_width*height
        ray.wallDists.clear()
        #time.sleep(1)
        for i in range(0, len(barriers)):
            barriers[i].display()
            
            ray.checkCollision(barriers[i])
            if i == len(barriers)-1:
                ray.drawRay()
    if len(scene) > 0:
        sceneObj.drawScene(scene)
    
    """
        closest_barrier = 0
        for i in range(0,len(barriers)):
            barriers[i].display()
            if ray.checkCollision(barriers[i]) is not None:
                if ray_pos.dist(ray.checkCollision(barriers[i])) > closest_barrier:
                    closest_barrier = ray.checkCollision(barrier[i])
            if i == len(barriers)-1:
                if closest_barrier != 0:
                    line(ray.pos().x, ray.pos().y, closest_barrier.x, closest_barrier.y)
                #else:
                    #line(ray.pos().x, ray.pos().y, (ray.pos().x+(ray.dir().x)*800), (ray.pos().y+(ray.dir().y)*800))
    """
    
def keyPressed():
    global rays
    global middle_vector
    if key == CODED:
        if keyCode == LEFT:
            rays.pop(len(rays)-1)
            rays.insert(0,Ray(rays[0].pos.x, rays[0].pos.y, rays[0].angle-1))
            middle_vector = rays[(len(rays)/2)-1].dir
    
        if keyCode == RIGHT:
            #print(rays[len(rays)-1].angle+1)
            rays.pop(0)
            rays.append(Ray(rays[len(rays)-1].pos.x, rays[len(rays)-1].pos.y, rays[len(rays)-1].angle+1))
            middle_vector = rays[(len(rays)/2)-1].dir
            #for ray in range(0,len(rays)):
             #   print(rays[ray].angle, ray)

def mouseMoved():
    if mouseX < half_width:
        loop()
    
