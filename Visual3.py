from vpython import *


# Set up the scene
scene = canvas(title="Two Masses in a Torsion Field with SHM",
               width=800, height=600, center=vector(0,0,0), background=color.black)

# Create two masses
mass1 = sphere(pos=vector(-5, 0, 0), radius=0.5, color=color.red, make_trail=True)
mass2 = sphere(pos=vector(5, 0, 0), radius=0.5, color=color.blue, make_trail=True)

# Define initial velocities (small velocities towards each other)
mass1.velocity = vector(0.03, 0.03, 0)
mass2.velocity = vector(-0.03, -0.03, 0)

# Parameters for the torsion field visualization
grid_range = 10  # Increase the range for a larger field
spacing = 1
twist_factor = -2

# Create a flat grid of twisting vectors
arrows = []
for x in range(-grid_range, grid_range + 1, spacing):
    for y in range(-grid_range, grid_range + 1, spacing):
        if abs(x) == 5 and y == 0:
            continue  # Skip the positions of the masses
        
        # Calculate position of the vector origin
        position = vector(x, y, 0)
        
        # Define torsion effect - vectors twist around both masses
        r1 = mag(position - mass1.pos)
        r2 = mag(position - mass2.pos)
        
        if r1 != 0:
            direction1 = vector(-(position.y - mass1.pos.y), position.x - mass1.pos.x, 0) * (twist_factor / (r1 ** 2 + 1))
        else:
            direction1 = vector(0, 0, 0)
        
        if r2 != 0:
            direction2 = vector(-(position.y - mass2.pos.y), position.x - mass2.pos.x, 0) * (twist_factor / (r2 ** 2 + 1))
        else:
            direction2 = vector(0, 0, 0)
        
        # Total direction is the combined effect of torsion fields
        total_direction = direction1 + direction2

        # Create an arrow to represent the vector field
        a = arrow(pos=position, axis=total_direction, color=color.green)
        arrows.append(a)



# Simulation loop
while True:
    rate(50)
    
    # Update positions of masses due to torsion "attraction"
    r = mass1.pos - mass2.pos
    force_magnitude = 0.1 / (mag(r)**2 + 1)  # inverse square Force
    
    # Apply forces due to torsion-like effects
    force = norm(r) * force_magnitude
    mass1.velocity -= force
    mass2.velocity += force

    # Update positions
    mass1.pos += mass1.velocity
    mass2.pos += mass2.velocity

    # Update the torsion vectors
    for a in arrows:
        r1 = mag(a.pos - mass1.pos)
        r2 = mag(a.pos - mass2.pos)
        
        if r1 != 0:
            direction1 = vector(-(a.pos.y - mass1.pos.y), a.pos.x - mass1.pos.x, 0) * (twist_factor / (r1 ** 2 + 1))
        else:
            direction1 = vector(0, 0, 0)
        
        if r2 != 0:
            direction2 = vector(-(a.pos.y - mass2.pos.y), a.pos.x - mass2.pos.x, 0) * (twist_factor / (r2 ** 2 + 1))
        else:
            direction2 = vector(0, 0, 0)

        # Update arrow directions to represent the dynamic torsion field
        a.axis = direction1 + direction2
