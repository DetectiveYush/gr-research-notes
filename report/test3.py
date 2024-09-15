from vpython import sphere, vector, curve, canvas, color, rate, scene, arrow, box, dot, cross, norm, radians, rotate

# Create a canvas
scene = canvas(title='Curvature to Torsion Visualization', width=800, height=600, center=vector(0, 0, 0), background=color.white)

# Parameters
R = 1  # Radius of the sphere
center_sphere = vector(0, 0, 0)  # Center of the sphere
torsion_plane_offset = 3  # Distance from the sphere to the torsion plane

# Create a sphere (representing curved space in GR)
earth = sphere(pos=center_sphere, radius=R, color=color.blue, opacity=0.2)

# Create a flat plane (representing torsion in TEGR)
plane = box(pos=vector(torsion_plane_offset, 0, 0), size=vector(4, 4, 0.01), color=color.gray(0.8), opacity=0.5)

# Function to create a vector (arrow) on the sphere
def create_vector_on_sphere(theta, phi):
    # Convert spherical to Cartesian coordinates
    x = R * sin(theta) * cos(phi)
    y = R * sin(theta) * sin(phi)
    z = R * cos(theta)
    vector_pos = vector(x, y, z)
    vec = arrow(pos=center_sphere, axis=vector_pos, color=color.red)
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
vector_plane = arrow(pos=vector(torsion_plane_offset, 1, 0), axis=vector(1, 1, 0), color=color.green)

# Visualization loop
while True:
    rate(20)
    # Rotate the vector on the sphere (simulating curvature)
    rotate_vector_on_sphere(vector_sphere, angle=radians(1))

    # After a certain angle, start transitioning to torsion visualization
    if abs(dot(vector_sphere.axis, vector(0, 1, 0))) < 0.5:
        # Simulate torsion effect by twisting the vector on the plane
        twist_vector_on_plane(vector_plane, radians(2))
