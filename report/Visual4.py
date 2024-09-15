from vpython import *

# Set up the scene
scene = canvas(title="Two Masses in a Gravitational Field",
               width=800, height=600, center=vector(0, 0, 0), background=color.black)

# Create two masses
mass1 = sphere(pos=vector(-5, 0, 0), radius=0.5, color=color.red, make_trail=True)
mass2 = sphere(pos=vector(5, 0, 0), radius=0.5, color=color.blue, make_trail=True)

# Define initial velocities (small velocities towards each other)
mass1.velocity = vector(0.03, 0.03, 0)
mass2.velocity = vector(-0.03, -0.03, 0)

# Parameters for the gravitational field visualization
grid_range = 10
spacing = 1
G = 0.1  # Gravitational constant for scaling purposes

# Create a flat grid of gravitational field vectors
arrows = []
for x in range(-grid_range, grid_range + 1, spacing):
    for y in range(-grid_range, grid_range + 1, spacing):
        if abs(x) == 5 and y == 0:
            continue  # Skip the positions of the masses
        
        # Calculate position of the vector origin
        position = vector(x, y, 0)
        
        # Calculate gravitational effect - vectors point toward each mass
        r1 = position - mass1.pos
        r2 = position - mass2.pos
        mag_r1 = mag(r1)
        mag_r2 = mag(r2)
        
        if mag_r1 != 0:
            direction1 = -norm(r1) * (G / (mag_r1 ** 2))
        else:
            direction1 = vector(0, 0, 0)
        
        if mag_r2 != 0:
            direction2 = -norm(r2) * (G / (mag_r2 ** 2))
        else:
            direction2 = vector(0, 0, 0)
        
        # Total direction is the combined gravitational effect from both masses
        total_direction = direction1 + direction2

        # Create an arrow to represent the gravitational field
        a = arrow(pos=position, axis=total_direction, color=color.green)
        arrows.append(a)

# Simulation loop
while True:
    rate(50)
    
    # Update positions of masses due to gravitational attraction
    r = mass1.pos - mass2.pos
    force_magnitude = G / (mag(r)**2 + 1)
    
    # Apply forces due to gravitational effects
    force = norm(r) * force_magnitude
    mass1.velocity -= force
    mass2.velocity += force

    # Update positions
    mass1.pos += mass1.velocity
    mass2.pos += mass2.velocity

    # Update the gravitational field vectors
    for a in arrows:
        r1 = a.pos - mass1.pos
        r2 = a.pos - mass2.pos
        mag_r1 = mag(r1)
        mag_r2 = mag(r2)
        
        if mag_r1 != 0:
            direction1 = -norm(r1) * (G / (mag_r1 ** 2))
        else:
            direction1 = vector(0, 0, 0)
        
        if mag_r2 != 0:
            direction2 = -norm(r2) * (G / (mag_r2 ** 2))
        else:
            direction2 = vector(0, 0, 0)

        # Update arrow directions to represent the gravitational field
        a.axis = direction1 + direction2
