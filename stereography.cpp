#include <GL/glut.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtx/norm.hpp>
#include <vector>
#include <iostream>

// Variables
float R = 1.0f; // Radius of the sphere
glm::vec3 center(0.0f, 0.0f, R);
std::vector<std::vector<glm::vec3>> drawn_curves_sphere;
std::vector<std::vector<glm::vec3>> drawn_curves_plane;
bool is_drawing = false;
std::vector<glm::vec3> current_curve_sphere;
std::vector<glm::vec3> current_curve_plane;

// Function to perform stereographic projection
glm::vec2 stereographic_projection(float x, float y, float z) {
    float denom = 2 * R - z;
    return glm::vec2(2 * R * x / denom, 2 * R * y / denom);
}

// Function to check if a point is inside the sphere
int point_inside_sphere(glm::vec3 pos) {
    float distance = glm::length(center - pos);
    return (distance < R) ? 1 : -1;
}

// Function to calculate the scaling factor to the sphere
float scale_to_sphere_factor(int sign, glm::vec3 direction, glm::vec3 pos) {
    float p2 = glm::length2(pos - center);
    float d2 = glm::length2(direction);
    float x2 = (p2 + sign * (R * R)) / d2;
    return sqrt(x2);
}

// Function to erase drawn curves
void erase() {
    drawn_curves_sphere.clear();
    drawn_curves_plane.clear();
}

// Function to add a point to the current curve
void add_point(glm::vec3 pos) {
    glm::vec3 normal = glm::normalize(glm::vec3(0.0f, 0.0f, 1.0f)); // Assume normal in Z direction
    glm::vec3 shift = -normal * glm::dot(normal, (center - pos));
    glm::vec3 shifted_pos = pos + shift;
    float temp = R * R - glm::length2(shifted_pos - center);
    if (temp > 0) {
        float scaling_factor_to_sphere = sqrt(temp);
        glm::vec3 sphere_point = shifted_pos - (normal * scaling_factor_to_sphere);
        current_curve_sphere.push_back(sphere_point);

        glm::vec2 proj = stereographic_projection(sphere_point.x, sphere_point.y, sphere_point.z);
        glm::vec3 proj_point(proj.x, proj.y, 0.0f);

        current_curve_plane.push_back(proj_point);
    }
}

// Mouse and Keyboard Event Handling
void on_mouse(int button, int state, int x, int y) {
    if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN) {
        is_drawing = true;
        current_curve_sphere.clear();
        current_curve_plane.clear();
        drawn_curves_sphere.push_back(current_curve_sphere);
        drawn_curves_plane.push_back(current_curve_plane);
    }
    if (button == GLUT_LEFT_BUTTON && state == GLUT_UP) {
        is_drawing = false;
    }
}

void on_motion(int x, int y) {
    if (is_drawing) {
        glm::vec3 pos = glm::vec3(x / 100.0f, y / 100.0f, 0.0f);
        add_point(pos);
    }
}

void on_keyboard(unsigned char key, int x, int y) {
    if (key == 'r') {
        erase();
    }
}

// Function to draw the scene
void draw_scene() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glColor3f(0.0f, 0.0f, 1.0f);
    glutSolidSphere(R, 50, 50); // Draw the sphere

    // Draw the curves on the sphere
    glColor3f(1.0f, 0.0f, 0.0f);
    for (auto &curve : drawn_curves_sphere) {
        glBegin(GL_LINE_STRIP);
        for (auto &point : curve) {
            glVertex3f(point.x, point.y, point.z);
        }
        glEnd();
    }

    // Draw the curves on the plane
    glColor3f(0.0f, 1.0f, 0.0f);
    for (auto &curve : drawn_curves_plane) {
        glBegin(GL_LINE_STRIP);
        for (auto &point : curve) {
            glVertex3f(point.x, point.y, point.z);
        }
        glEnd();
    }

    glutSwapBuffers();
}

void setup() {
    glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
    glEnable(GL_DEPTH_TEST);
}

int main(int argc, char **argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(800, 600);
    glutCreateWindow("Stereographic Projection");

    setup();

    glutDisplayFunc(draw_scene);
    glutIdleFunc(draw_scene);
    glutMouseFunc(on_mouse);
    glutMotionFunc(on_motion);
    glutKeyboardFunc(on_keyboard);

    glutMainLoop();
    return 0;
}
