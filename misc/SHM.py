from vpython import *
import numpy as np

# Create a canvas
scene = canvas(title="Object Moving in a Circle", width=800, height=600)

# Create Cartesian plane 1 (2D)
origin1 =  vector(0,0,0)
x_axis = arrow(pos=origin1, axis=vector(3, 0, 0), color=color.red, shaftwidth=0.02)
y_axis = arrow(pos=origin1, axis=vector(0, 3, 0), color=color.green, shaftwidth=0.02)

# Create a circular path using curve
circle_path = curve(pos = origin1, color=color.blue, radius=0.01)
theta_values = np.linspace(0, 2*np.pi, 100)
for theta in theta_values:
    x = np.cos(theta)+origin1.x
    y = np.sin(theta)+origin1.y
    circle_path.append(vector(x, y, 0))

# Create a small sphere to represent the object
object_sphere = sphere(pos=vector(1, 0, 0)+origin1, radius=0.05, color=color.orange, make_trail=False)

# Animation loop: Move the sphere along the circular path
t = 0  # Initialize time
dt = 0.01  # Time step
w =3 #angular frequency(speed)
while True:
    rate(30)  # Controls the speed of the animation (50 frames per second)
    
    # Parametric equations for circular motion
    x = np.cos(w*t)+origin1.x
    y = np.sin(w*t)+origin1.y
    
    # Update the sphere's position
    object_sphere.pos = vector(x, y, 0)
    
    # Update time
    t += dt
