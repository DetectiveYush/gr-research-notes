from vpython import *

# Create a scene
scene = canvas(title="Curvilinear Coordinate Transformation", width=800, height=600)

# Create axis lines for original coordinate system (x)
x_axis = arrow(pos=vector(-5,0,0), axis=vector(10,0,0), color=color.red, shaftwidth=0.05)
y_axis = arrow(pos=vector(0,-5,0), axis=vector(0,10,0), color=color.green, shaftwidth=0.05)

# Create grids for original (x) coordinate system
grid_lines = []
for i in range(-5, 6):
    grid_lines.append(curve(pos=[vector(i, -5, 0), vector(i, 5, 0)], color=color.red))
    grid_lines.append(curve(pos=[vector(-5, i, 0), vector(5, i, 0)], color=color.green))

# Stretch factor for curvilinear coordinate system
stretch_factor = 1

# Function to draw the curvilinear grid (y = x^2 type transformation)
def draw_curvilinear_grid(stretch):
    # Clear previous grid
    for obj in scene.objects:
        if isinstance(obj, curve) and obj.color == color.orange:
            obj.visible = False
    
    # Draw new curvilinear grid lines
    for i in range(-5, 6):
        grid_lines.append(curve(pos=[vector(i, stretch * i**2, 0), vector(i, stretch * (i+1)**2, 0)], color=color.orange))
        grid_lines.append(curve(pos=[vector(stretch * i**2, i, 0), vector(stretch * (i+1)**2, i, 0)], color=color.orange))

# Create original vector in x-system
V = arrow(pos=vector(0,0,0), axis=vector(2,1,0), color=color.blue, shaftwidth=0.1)
label(pos=V.axis + vector(0.5,0,0), text="V in x-system", height=10, color=color.blue)

# Create curvilinear transformed vector in y-system (stretched)
V_prime = arrow(pos=vector(0,0,0), axis=vector(2,1,0), color=color.orange, shaftwidth=0.1)
label(pos=V_prime.axis + vector(0.5,0,0), text="V' in y-system (stretchable)", height=10, color=color.orange)

# Update vector based on stretching
def update_vector(stretch):
    V_prime.axis = vector(stretch * V.axis.x**2, stretch * V.axis.y**2, 0)

# Mouse event handler to stretch/squeeze the curvilinear grid
def stretch_handler(evt):
    global stretch_factor
    # Get mouse x-position relative to center and adjust stretch factor
    stretch_factor = (evt.pos.x + 5) / 5  # normalize to range based on x-pos
    update_vector(stretch_factor)
    draw_curvilinear_grid(stretch_factor)

# Initial drawing of curvilinear grid
draw_curvilinear_grid(stretch_factor)

# Bind mouse click and drag event to stretch handler
scene.bind('mousemove', stretch_handler)

# Display scene info
scene.append_to_caption("\n\nDrag the mouse horizontally to stretch/squeeze the curvilinear grid (orange).")


while 1:
    rate(10)