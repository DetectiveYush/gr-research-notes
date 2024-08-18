from vpython import sphere, vector, curve, canvas, color, rate, scene, cross, dot, norm

# Create a canvas
scene = canvas(title='Stereographic Projection', width=800, height=600, center=vector(0, 0, 0), background=color.white)

# Create a sphere (representing the unit sphere)
R = 1  # Radius of the sphere
center=vector(0,0,R)
earth = sphere(pos=center, radius=R, color=color.blue, opacity=0.5)

# Lists to store drawn curves
drawn_curves_sphere = []
drawn_curves_plane = []

# Flag to indicate if the mouse is being pressed
is_drawing = False
current_curve_sphere = None
current_curve_plane = None

# Function for reverse stereographic projection
def stereographic_projection(x, y, z):
    denom = 2*R - z
    return (2*R * x / denom, 2*R * y / denom)

# Event handler for mouse down
def on_mousedown(evt):
    global is_drawing, current_curve_sphere, current_curve_plane
    is_drawing = True
    current_curve_sphere = curve(color=color.red)
    current_curve_plane = curve(color=color.green)
    drawn_curves_sphere.append(current_curve_sphere)
    drawn_curves_plane.append(current_curve_plane)
    add_point(evt.pos)

# Event handler for mouse move
def on_mousemove(evt):
    if is_drawing:
        add_point(evt.pos)

# Event handler for mouse up
def on_mouseup(evt):
    global is_drawing
    is_drawing = False

#Function to find if point is inside sphere
def point_inside_sphere(pos):
    distance = center - pos
    if distance.mag < R:
        return 1
    else:
        return -1
#Scaling factor to scale viwing direction appropriately to match surface of sphere (needs corrections)
def scale_to_sphere_factor(sign, direction, pos):
    p2=(pos-center).mag**2
    d2=direction.mag**2
    x2 = (p2 + sign*(R**2))/d2
    #print("x^2 = ",x2)
    x = pow(x2,0.5)
    return x


# Function to add point to the current curves
def add_point(pos):
    #print(pos)
    normal = norm(scene.camera.axis)
    shift = - normal * (abs(dot(normal,(center - pos))))
    shifted_pos = pos + shift
    
    scaling_factor_to_sphere = pow((pow(R,2) - pow((shifted_pos - center).mag,2)),0.5)
    sphere_point = shifted_pos - (normal * scaling_factor_to_sphere)
    print("shift = ",shift) ; print("center = ",center); print("pos = ",pos); print("normal = ",normal); print("sphere_point = ",sphere_point)
    current_curve_sphere.append(sphere_point)
    
    # Project this point onto the plane using stereographic projection
    proj_x, proj_y = stereographic_projection(sphere_point.x, sphere_point.y, sphere_point.z)
    proj_point = vector(proj_x, proj_y, 0)
    
    # Add the projected point to the plane curve
    current_curve_plane.append(proj_point)

# Event handler for key presses
def on_keydown(evt):
    global drawn_curves_sphere, drawn_curves_plane
    if evt.key == 'r':
        # Remove all drawn curves on the sphere and the plane
        for curve_obj in drawn_curves_sphere:
            curve_obj.visible = False  # Hide the curve on the sphere
        for curve_obj in drawn_curves_plane:
            curve_obj.visible = False  # Hide the curve on the plane
        drawn_curves_sphere.clear()  # Clear the list for sphere curves
        drawn_curves_plane.clear()  # Clear the list for plane curves

# Bind the mouse and key events to their handlers
scene.bind('mousedown', on_mousedown)
scene.bind('mousemove', on_mousemove)
scene.bind('mouseup', on_mouseup)
scene.bind('keydown', on_keydown)

# Draw a grid to represent the projection plane
plane = curve(vector(-2, -2, 0), vector(2, -2, 0), vector(2, 2, 0), vector(-2, 2, 0), vector(-2, -2, 0), color=color.black)
while True:
    rate(10)  # Run the loop at a reasonable rate (10 frames per second)
