import math
import random

from PIL import ImageDraw

from src.findByLines.Circle import Circle
from src.findByLines.Line import Line

list_of_colors = [
    ("black", "gray"),
    ("chocolate", "beige"),
    ("blue", "cyan"),
    ("green", "lightgreen"),
    ("purple", "violet"),
]


def find_circle(image, pix):
    width, height = image.size

    red_pixels = get_red_pixels(pix, width, height)

    list_of_pixels = random.choices(red_pixels, k=4)
    draw = ImageDraw.Draw(image)
    for pixel in list_of_pixels:  # only for drawing
        draw.ellipse((pixel[0] - 5, pixel[1] - 5, pixel[0] + 5, pixel[1] + 5), fill=(255, 0, 0), outline=(0, 0, 0))
    print(list_of_pixels, "pixels")

    list_of_perpendiculars = get_perpendicular_lines(list_of_pixels)

    for line in list_of_perpendiculars:  # only for drawing
        draw_lines(line, height, image)

    list_of_intersections = intersections(list_of_perpendiculars)
    print(list_of_intersections, "intersections")

    circle_centers = centers(list_of_pixels)
    print(circle_centers, "circle_centers")

    middle = 0
    for i in range(len(list_of_intersections)):
        dist = distance(list_of_intersections[i], list_of_intersections[i - 1])
        if middle == 0:
            middle = middle_point(list_of_intersections[i], list_of_intersections[i - 1])
        else:
            middle = middle_point(list_of_intersections[i], middle)
        if dist > height * 0.05:
            return None

    circle = build_circle(middle[0], middle[1], distance(list_of_pixels[0], list_of_intersections[0]))
    draw.ellipse(
        (circle.x - circle.radius, circle.y - circle.radius, circle.x + circle.radius, circle.y + circle.radius),
        outline=(100, 200, 0), width=3)
    return circle


def build_circle(x, y, radius):
    circle = Circle()
    circle.x = x
    circle.y = y
    circle.radius = radius
    return circle


def centers(list_of_pixels):
    circle_centers = []
    for i in range(len(list_of_pixels)):
        circle_centers.append(center_of_circle(list_of_pixels[i], list_of_pixels[i - 1], list_of_pixels[i - 2]))
    return circle_centers


def intersections(list_of_perpendiculars):
    list_of_intersections = []
    for i in range(len(list_of_perpendiculars)):
        x = intersection_x(list_of_perpendiculars[i], list_of_perpendiculars[i - 1])
        list_of_intersections.append((x, y_fun(x, list_of_perpendiculars[i].c, list_of_perpendiculars[i].slope)))
    return list_of_intersections


def get_perpendicular_lines(list_of_pixels):
    list_of_perpendiculars = []
    for i in range(len(list_of_pixels)):
        list_of_perpendiculars.append(get_perpendicular_line(list_of_pixels[i], list_of_pixels[i - 1]))
    return list_of_perpendiculars


def distance(point1, point2):
    projections = get_line_projections(point1, point2)
    return math.sqrt(projections[0] ** 2 + projections[1] ** 2)


def intersection_x(line1, line2):
    return (line2.c - line1.c) / (line1.slope - line2.slope)


def draw_lines(line, height, image):
    draw = ImageDraw.Draw(image)
    line_color, perp_line_color = list_of_colors.pop()
    draw.line((line.point1, line.point2), fill=line_color, width=3)
    line = get_max_x_points(line.c, line.slope, height)
    draw.line((line.point1, line.point2), fill=perp_line_color, width=3)


def get_red_pixels(pix, width, height):
    red_pixels = []
    for x in range(width):
        for y in range(height):
            if pix[x, y][0] > 200:
                red_pixels.append((x, y))
    return red_pixels


def find_perpendicular_slope(point1, point2):
    slope = float(point1[1] - point2[1]) / float(point1[0] - point2[0])
    return float(-1) / slope


def get_max_x_points(c, slope, height):
    line = Line()
    line.c = c
    line.slope = slope
    line.point1 = (x_fun(0, c, slope), 0)
    line.point2 = (x_fun(height, c, slope), height)
    return line


def get_perpendicular_line(point1, point2):
    line = Line()
    line.slope = find_perpendicular_slope(point1, point2)
    middle = middle_point(point1, point2)
    line.c = middle[1] - line.slope * middle[0]
    line.point1 = point1
    line.point2 = point2
    return line


def middle_point(point1, point2):
    return (point1[0] - get_line_projections(point1, point2)[0] / 2,
            point1[1] - get_line_projections(point1, point2)[1] / 2)


def x_fun(y, c, slope):
    return (y - c) / slope


def y_fun(x, c, slope):
    return (slope * x) + c


def get_line_projections(point1, point2):
    return point1[0] - point2[0], point1[1] - point2[1]


def center_of_circle(p1, p2, p3):
    center_x = (((p_2(p3) - p_2(p1)) / p_diff2(p3, p1, 1) - (p_2(p2) - p_2(p1)) / p_diff2(p2, p1, 1)) * (
            p_diff2(p3, p1, 1) * p_diff2(p2, p1, 1))) / (
                       (p_diff2(p1, p2, 0) * p_diff2(p3, p1, 1)) - (p_diff2(p1, p3, 0) * p_diff2(p2, p1, 1)))
    center_y = (p_2(p2) - p_2(p1)) / p_diff2(p2, p1, 1) + (p_diff2(p1, p2, 0) * center_x) / p_diff2(p2, p1, 1)
    return center_x, center_y


def p_diff2(p1, p2, index):
    return 2 * p1[index] - 2 * p2[index]


def p_2(point):
    return point[0] ** 2 + point[1] ** 2

# y = slope * x + C
# x = (y - C) / slope
# slope = (By - Ay) / (Bx - Ax)

# (x-cenX)**2 + (y-cenY)**2 = r**2
# (Ax - cenX)**2 + (Ay - cenY)**2 = (Bx - cenX)**2 + (By - cenY)**2
# Ax**2 - 2*Ax*cenX + cenX**2 + Ay**2 - 2*Ay*cenY + cenY**2 = Bx**2 - 2*Bx*cenX + cenX**2 + By**2 - 2*By*cenY + cenY**2
# cenY = (Bx**2 + By**2 - Ax**2 - Ay**2) / (2*By - 2*Ay)  + (2*Ax - 2*Bx)*cenX / (2*By - 2*Ay)
# cenX = (((Bx**2 + By**2 - Cx**2 - Cy**2) / (2*By - 2*Cy) - (Bx**2 + By**2 - Ax**2 - Ay**2)) /
#       ((2*By - 2*Ay))*(2*By - 2*Ay)*(2*By - 2*Cy) / ((2*Ax - 2*Bx)(2*By - 2*Cy) - (2*Cx - 2*Bx)(2*By - 2*Ay)))
