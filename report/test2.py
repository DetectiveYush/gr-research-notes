from vpython import sphere, vector, curve, canvas, color, rate, scene, arrow, box, dot, rotate, radians, sin, cos

# Create a canvas
scene = canvas(title='Curvature to Torsion via Stereographic Projection', width=800, height=600, center=vector(0, 0, 0), background=color.white)

# Parameters
R = 1  # Radius of the sphere
center_sphere = vector(0, 0, R)  # Center of the sphere moved to (0, 0, R)
torsion_plane_offset = 3  # Distance from the sphere to the torsion plane

# Create a sphere (representing curved space in GR)
earth = sphere(pos=center_sphere, radius=R, color=color.blue, opacity=0.2)

# Create a flat plane (representing torsion in TEGR)
plane = box(pos=vector(0, 0, 0), size=vector(4, 4, 0.01), color=color.gray(0.8), opacity=0.5)

# Function for stereographic projection
def stereographic_projection(point):
    # Calculate stereographic projection of a point on the sphere onto the plane
    x, y, z = point.x, point.y, point.z
    denom = R - (z - center_sphere.z)
    if denom == 0:
        denom = 1e-8  # Avoid division by zero at the north pole
    proj_x = 2 * R * x / denom
    proj_y = 2 * R * y / denom
    return vector(proj_x, proj_y, 0)  # Projection is on the plane (z=0)

# Function to create a vector (arrow) on the sphere
def create_vector_on_sphere(theta, phi):
    # Convert spherical to Cartesian coordinates
    x = R * sin(theta) * cos(phi)
    y = R * sin(theta) * sin(phi)
    z = R * cos(theta)
    vector_pos = vector(x, y, z) + center_sphere  # Adjust for new center
    vec = arrow(pos=center_sphere, axis=vector_pos - center_sphere, color=color.red)
    return vec

# Function to rotate a vector around the Y-axis (simulate curvature in GR)
def rotate_vector_on_sphere(vec, angle):
    vec.axis = rotate(vec.axis, angle=angle, axis=vector(0, 1, 0))
    vec.pos = center_sphere + vec.axis

# Function to simulate torsion: Twist the vector on a flat plane
def twist_vector_on_plane(vec, twist_angle):
    vec.axis = rotate(vec.axis, angle=twist_angle, axis=vector(0, 0, 1))
    vec.pos = plane.pos + vector(vec.pos.x, vec.pos.y, 0)  # Project onto the plane

# Initialize vectors
vector_sphere = create_vector_on_sphere(radians(45), radians(45))
vector_plane = arrow(pos=vector(0, 1, 0), axis=vector(1, 1, 0), color=color.green)

# Visualization loop
while True:
    rate(20)
    # Rotate the vector on the sphere (simulating curvature)
    rotate_vector_on_sphere(vector_sphere, angle=radians(1))

    # Project the rotating vector onto the plane using stereographic projection
    proj_point = stereographic_projection(vector_sphere.axis + center_sphere)
    vector_plane.pos = plane.pos + proj_point  # Update plane vector's position

    # Simulate torsion effect by twisting the vector on the plane
    twist_vector_on_plane(vector_plane, radians(2))
