# ray_tracer.py
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Color import Color
from Vector import Vector
from Hit import Hit
from Sphere import Sphere
from Plane import Plane
from Light import Light

# Window dimensions
window_width = 300
window_height = 300

# Scene objects
objects = []
background = Color(0.5, 0.8, 1.0)

# Lights
lights = []

# Camera setup
eye = Vector(0, 0, 4)
u = Vector(1, 0, 0)
v = Vector(0, 1, 0)
n = Vector(0, 0, 1)
N = 1.0
W = 0.5
H = 0.5

# Counter for testing (similar to C++ code)
counter = 0

def setup_scene():
    global objects, lights

    # Sphere
    sphere = Sphere(center=Vector(0, 0, 0), radius=1.0)
    sphere.ambient = Color(0.1, 0.1, 0.1)
    sphere.diffuse = Color(1.0, 0.2, 0.2)
    sphere.specular = Color(0.7, 0.7, 0.7)
    sphere.shininess = 50
    sphere.reflectivity = 0.4
    objects.append(sphere)

    # Plane
    plane = Plane(n=Vector(0, 1, 0), a=-1)
    plane.ambient = Color(0.1, 0.1, 0.1)
    plane.diffuse = Color(0.2, 0.5, 0.2)
    plane.specular = Color(0.7, 0.7, 0.7)
    plane.shininess = 50
    plane.reflectivity = 0.4
    objects.append(plane)

    # Light 1
    light1 = Light(
        position=Vector(-2, 2, 2),
        ambient=Color(0.1, 0.1, 0.1),
        diffuse=Color(0.5, 0.5, 0.5),
        specular=Color(0.5, 0.5, 0.5)
    )
    lights.append(light1)

    # Light 2
    light2 = Light(
        position=Vector(3, 1, 3),
        ambient=Color(0.1, 0.1, 0.1),
        diffuse=Color(0.4, 0.4, 0.6),
        specular=Color(0.3, 0.3, 0.5)
    )
    lights.append(light2)

def intersect(source, d):
    global counter
    counter += 1
    if source == eye:
        if counter in [1, 90000]:
            print(f"d=({d.x:.2f}, {d.y:.2f}, {d.z:.2f})")
    else:
        counter -= 1

    hit = Hit(source, d, -1.0, None)

    for obj in objects:
        t = obj.intersect(source, d)
        if t > 0.00001 and (hit.object is None or t < hit.t):
            hit = Hit(source, d, t, obj)

    return hit

def shade(hit):
    if hit.object is None:
        return background

    color = Color(0.0, 0.0, 0.0)

    for light in lights:
        # Ambient reflection
        color += hit.object.ambient * light.ambient

        p = hit.hit_point()
        v_dir = (eye - p).normalize()
        s = (light.position - p).normalize()
        m = hit.object.normal(p)

        # Ensure light hits the front face
        if s.dot(m) < 0:
            continue

        # Shadow feeler
        feeler = intersect(p, s)
        if feeler.object is None or feeler.t < 0 or feeler.t > 1:
            # Diffuse reflection
            diffuse_intensity = max(s.dot(m), 0.0)
            color += hit.object.diffuse * light.diffuse * diffuse_intensity

            # Specular reflection
            h = (s + v_dir).normalize()
            specular_intensity = max(h.dot(m), 0.0) ** hit.object.shininess
            color += hit.object.specular * light.specular * specular_intensity

    return color.clamp()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)

    for r in range(window_height):
        for c in range(window_width):
            # Construct ray
            dx = -n.x * N + W * (2.0 * c / (window_width - 1) - 1) * u.x + H * (2.0 * r / (window_height - 1) - 1) * v.x
            dy = -n.y * N + W * (2.0 * c / (window_width - 1) - 1) * u.y + H * (2.0 * r / (window_height - 1) - 1) * v.y
            dz = -n.z * N + W * (2.0 * c / (window_width - 1) - 1) * u.z + H * (2.0 * r / (window_height - 1) - 1) * v.z
            d = Vector(dx, dy, dz).normalize()

            # Intersect ray with scene
            hit = intersect(eye, d)

            # Shade pixel
            color = shade(hit)
            glColor3f(color.r, color.g, color.b)
            glVertex2f(c, r)

    glEnd()
    glFlush()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    setup_scene()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Python OpenGL Ray Tracer")
    init()
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
