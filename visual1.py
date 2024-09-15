from vpython import *

# Set up the scene
scene = canvas(title="Visualizing Gravity as Torsion in Flat Spacetime",
               width=800, height=600, center=vector(0,0,0), background=color.black)

# Central mass as a sphere
central_mass = sphere(pos=vector(0,0,0), radius=0.5, color=color.red)

# Parameters for the grid and vectors
grid_range = 5
spacing = 1
twist_factor = 2

# Create a flat grid of twisting vectors
for x in range(-grid_range, grid_range + 1, spacing):
    for y in range(-grid_range, grid_range + 1, spacing):
        if x == 0 and y == 0:
            continue  # Skip the central mass position
        
        # Calculate position of the vector origin
        position = vector(x, y, 0)
        
        # Define the torsion effect - vectors twist around the central mass
        r = mag(position)
        if r != 0:
            direction = vector(-y, x, 0) * (twist_factor / (r ** 2 + 1))
        else:
            direction = vector(0, 0, 0)
        
        # Create an arrow to represent the vector field
        arrow(pos=position, axis=direction, color=color.blue)

# Add labels or more elements as needed
label(pos=vector(0, -grid_range - 1, 0), text="Twisting Vectors around Mass", xoffset=0, yoffset=20, color=color.white)

# Let the scene remain interactive
while True:
    rate(30)
