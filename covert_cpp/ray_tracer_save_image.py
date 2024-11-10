# ray_tracer.py (Updated for rendering from multiple angles)
import sys
import numpy as np
from Color import Color
from Vector import Vector
from Hit import Hit
from Sphere import Sphere
from Plane import Plane
from Light import Light
from PIL import Image
import math
import os

# Window dimensions
window_width = 300
window_height = 300

# Scene objects
objects = []
background = Color(0.5, 0.8, 1.0)

# Lights
lights = []

# Camera setup - these will be updated for each angle
eye = Vector(0, 0, 4)
u = Vector(1, 0, 0)
v = Vector(0, 1, 0)
n = Vector(0, 0, 1)
N = 1.0
W = 0.5
H = 0.5

# Counter for testing (similar to C++ code)
counter = 0

# Output directory for images
output_dir = "rendered_images"

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

def update_camera(angle_degrees, radius=4.0, height=0.0):
    """
    Updates the camera's position and orientation based on the given angle.
    The camera moves around the y-axis at a fixed radius and height.
    """
    global eye, u, v, n

    theta = math.radians(angle_degrees)
    eye = Vector(radius * math.cos(theta), height, radius * math.sin(theta))

    # Camera looks at the origin
    center = Vector(0, 0, 0)
    n = (eye - center).normalize()

    # Up vector
    up = Vector(0, 1, 0)
    u = up.cross(n).normalize()
    v = n.cross(u)

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

        # Shadow feeler (offset to avoid self-intersection)
        feeler = intersect(p + m * 0.0001, s)
        if feeler.object is None or feeler.t < 0 or feeler.t > 1:
            # Diffuse reflection
            diffuse_intensity = max(s.dot(m), 0.0)
            color += hit.object.diffuse * light.diffuse * diffuse_intensity

            # Specular reflection
            h = (s + v_dir).normalize()
            specular_intensity = max(h.dot(m), 0.0) ** hit.object.shininess
            color += hit.object.specular * light.specular * specular_intensity

    return color.clamp()

def render_scene(output_image_filename):
    # Create a numpy array to store pixel data
    pixel_data = np.zeros((window_height, window_width, 3), dtype=np.uint8)

    for r in range(window_height):
        for c in range(window_width):
            # Construct ray direction d
            u_scalar = W * (2.0 * c / (window_width - 1) - 1)
            v_scalar = H * (2.0 * r / (window_height - 1) - 1)
            d = (-n * N + u * u_scalar + v * v_scalar).normalize()

            # Intersect ray with scene
            hit = intersect(eye, d)

            # Shade pixel
            color = shade(hit)

            # Store color in pixel_data array
            pixel_data[window_height - r - 1, c] = [
                int(color.r * 255),
                int(color.g * 255),
                int(color.b * 255)
            ]

    # Save the pixel_data array as an image
    save_image(pixel_data, output_image_filename)

def save_image(pixel_data, filename):
    # Create a PIL image from the pixel data
    image = Image.fromarray(pixel_data, 'RGB')

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the image to a file
    image.save(os.path.join(output_dir, filename))
    print(f"Image saved to {os.path.join(output_dir, filename)}")

def main():
    setup_scene()
    # Render images at different angles
    for angle in range(0, 360, 10):  # Every 10 degrees
        print(f"Rendering angle {angle} degrees")
        update_camera(angle_degrees=angle)
        output_filename = f"ray_traced_image_{angle}.png"
        render_scene(output_filename)

if __name__ == "__main__":
    main()
