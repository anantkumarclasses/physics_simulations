from vpython import *

# Define a class to represent a group of objects
class ObjectGroup:
    def __init__(self, objects):
        self.objects = objects
    
    # Method to move the group
    def move(self, offset):
        for obj in self.objects:
            obj.pos += offset
    
    # Method to rotate the group
    def rotate(self, angle, axis, origin=vector(0, 0, 0)):
        for obj in self.objects:
            obj.pos = origin + rotate(obj.pos - origin, angle=angle, axis=axis)


# Scene setup
scene.center = vector(0, 0, 0)
#scene.background = color.white
#scene.up = vec(0, cos(radians(30)), - sin(radians(30)))

# Define constants
g = 9.8  # gravitational acceleration (m/s^2)
m = 0.5  # mass of the block (kg)
k = 200  # spring constant (N/m)
mu = 0.05 # coefficient of kinetic friction
theta = radians(30)
l = 2 #length of the incline
d = 0.15 # size of the cubical block
l0 = 0.25 # natural length of the spring

# Time step
dt = 0.01

incline = box(pos=vec(0,0,0), size=vec(l,0.02 * l, l/2), color=color.cyan, axis=vec(cos(theta), sin(theta), 0))

block = box(
          pos=vec(incline.pos.x + incline.size.x / 2 - d/2, incline.size.y / 2 + d/ 2, 0), 
          size=vec(d,d,d), 
          color=color.orange,
          axis=vec(cos(theta), sin(theta), 0)
          ) 

spring_end_plate = box(
                    pos=vec(incline.pos.x - incline.size.x / 2 + 0.005, incline.size.y / 2 + d/2, 0),
                    size=vec(0.01, d, d),
                    axis=vec(cos(theta), sin(theta), 0)
                    )

spring = helix(
          pos=spring_end_plate.pos + vec(0.01,0,0), 
          length=l0,
          axis=vec(cos(theta), sin(theta), 0), 
          coils=10, 
          radius=0.03
          )


group = ObjectGroup([incline, block, spring_end_plate, spring])
group.rotate(angle=theta, axis=vec(0, 0, 1))

block.v = vec(0, 0 ,0)

# Function to calculate net force on the block up the incline:
def net_force_on(block, spring):
    
    # Gravitational force down the incline
    F_gravity = m * g * sin(theta)
    
    # Spring compression (if the block reaches the spring)
    spring_compression = l0 - spring.length
    if spring_compression > 0:
        F_spring = k * spring_compression
    else:
        F_spring = 0
    
    # Force of friction 
    F_friction = mu * m * g * cos(theta)
    
    # Net force on the block along the incline
    if block.v.x > 0:
        F_net = F_spring - F_gravity - F_friction
    elif block.v.x < 0:
        F_net = F_spring - F_gravity + F_friction
    else:
        F_net = F_spring - F_gravity
        
    
    return F_net


time = 20
t=0
# Simulation loop
while (t <= time):
    rate(100)

    # Calculate forces
    F_net = net_force_on(block, spring)
    
    a = F_net / m
    
    # Update the block's velocity and position using kinematics
    block.v.x += a * dt * cos(theta)
    block.v.y += a* dt * sin(theta)
    block.pos.x += block.v.x * dt
    block.pos.y += block.v.y * dt
    
    # Update the spring's length
    block_end_plate_cc_dist = sqrt(
           (block.pos.x-spring_end_plate.pos.x)**2 + 
           (block.pos.y-spring_end_plate.pos.y)**2 +
           (block.pos.z-spring_end_plate.pos.z)**2 
           )
    sep = block_end_plate_cc_dist - d/2 - 0.005
    spring.length = sep if sep < l0 else l0
    
    t += dt
    
print(spring.length)
    
