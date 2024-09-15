from vpython import sphere, vector, curve, canvas, color, rate, scene, arrow, dot

# Parameters
R = 1  # Radius of the sphere
center = vector(0, 0, R)

# Create a canvas
scene = canvas(title='Stereographic Projection of Rotating Vector', width=800, height=600, center=vector(0, 0, 0), background=color.white)

# Create the sphere
earth = sphere(pos=center, radius=R, color=color.blue, opacity=0.5)

# Create the initial rotating vector on the sphere
rotating_vector = arrow(pos=center, axis=vector(0.5, 0.5, 0.707) * R, color=color.red)

# Draw a grid to represent the projection plane
plane = curve(vector(-2, -2, 0), vector(2, -2, 0), vector(2, 2, 0), vector(-2, 2, 0), vector(-2, -2, 0), color=color.black)

# Function for reverse stereographic projection
def stereographic_projection(x, y, z):
    denom = 2 * R - z
    return (2 * R * x / denom, 2 * R * y / denom)

# Draw the initial projected vector
proj_x, proj_y = stereographic_projection(rotating_vector.axis.x, rotating_vector.axis.y, rotating_vector.axis.z)
projected_vector = arrow(pos=vector(proj_x, proj_y, 0), axis=vector(proj_x, proj_y, 0), color=color.green)

# Function to rotate a vector
def rotate_vector(v, angle, axis):
    return v.rotate(angle=angle, axis=axis)

# Main loop to rotate the vector and update the projection
while True:
    rate(30)  # Control the frame rate

    # Rotate the vector around the z-axis
    rotating_vector.axis = rotate_vector(rotating_vector.axis, 0.05, vector(0, 0, 1))

    # Update the stereographic projection
    proj_x, proj_y = stereographic_projection(rotating_vector.axis.x, rotating_vector.axis.y, rotating_vector.axis.z + R)
    projected_vector.pos = vector(proj_x, proj_y, 0)
    projected_vector.axis = vector(proj_x, proj_y, 0)
