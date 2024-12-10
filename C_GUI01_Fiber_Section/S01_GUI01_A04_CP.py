# -*- coding: utf-8 -*-
"""
ACTUALIZACION:  2024-05-15
AUTOR:          Marcelo Ortiz Á.
SCRIPT:         A03_Seccion_en_CP.py
COMENTARIOS:    Recibe una seccion, y la redibuja disponiendo su centro en el CP de la seccion.

"""

# %% [00] INTRODUCTION
# The function returns the same section but drawn with respect to its Plastic Centroid (CP). The aim is to facilitate the
# process of defining the section. In addition, it ensures that the 'zerolength' element does not have an undesired
# eccentricity during the development of the moment-curvature diagram and interaction diagram.

# Y_original ^                                                 ^ Y_CP
#            |   -------------------                  ---------|---------
#            |   |  |           |  |                  |  |     |     |  |
#            |   |  °--°--°--°--°  |                  |  °--°--°--°--°  |
#            |   |  |           |  |                  |  |     |     |  |
#            |   |  °           °  |                  |  °     |     °  |
#            |   |  |           |  |                  |  |     |     |  |
#            |   |  °           °  |         ==>      |  °     |-----°--|---> Z_CP
#            |   |  |           |  |                  |  |           |  |
#            |   |  °           °  |                  |  °           °  |
#            |   |  |           |  |                  |  |           |  |
#            |   |  °--°--°--°--°  |                  |  °--°--°--°--°  |
#            |   |  |           |  |                  |  |           |  |
#            |   -------------------                  -------------------
#            |
#            |---------------------> Z_original
#
#         Coord. System easy to work with        Coord. System necessary for MC


# %% TODO: [01] LIBRERIAS
import numpy as np


# %% TODO: [02] FUNCIONES
# Function to calculate the centroid of a quadrilateral patch
# This function was created to plot the center of the quadrilateral patch
# See S01_GUI01_A05_CenterFiber.py
# For that, in the initial function, is defined the coordinate in other 
# format.
def quad_centroid_area(coords):
    # Re arrange the coordinates
    x1, y1, x2, y2, x3, y3, x4, y4 = coords
    # Create a zy array representing a quad.
    zy_x = np.array([[x1, y1],
                     [x2, y2],
                     [x3, y3],
                     [x4, y4]])
    center_x_test, center_y_test, area = find_polygon_center(zy_x)
    return center_x_test, center_y_test, area


# Function to calculate the center of the polygon
def find_polygon_center(coords):
    """
    Function to find the center of a polygon based on its coordinates.

    Args:
        coords (numpy.ndarray): 2D array of shape (n, 2) representing the coordinates of the polygon vertices.

    Returns:
        tuple: A tuple (center_x, center_y) representing the coordinates of the center of the polygon.
    """
    area = 0.0
    center_x_fun = 0.0
    center_y_fun = 0.0
    n = len(coords)
    for i in range(n):
        j = (i + 1) % n
        xi, yi = coords[i]
        xj, yj = coords[j]
        cross_product = xi * yj - xj * yi
        area += cross_product
        center_x_fun += (xi + xj) * cross_product
        center_y_fun += (yi + yj) * cross_product
    area *= 0.5
    center_x_fun /= (6.0 * area)
    center_y_fun /= (6.0 * area)
    return center_x_fun, center_y_fun, area


# Function to calculate the area of a rectangular patch
def rect_area(coords):
    y1, z1, y2, z2 = coords
    return abs((y2 - y1) * (z2 - z1))


# Function to calculate the centroid of a rectangular patch
def rect_centroid(coords):
    y1, z1, y2, z2 = coords
    cy = (y1 + y2) / 2.0
    cz = (z1 + z2) / 2.0
    return cy, cz


# Function to calculate the area of a circular patch
def area_circ_wedge(ri, re, ang_beg, ang_end):
    a0_rad = np.deg2rad(ang_beg)
    a1_rad = np.deg2rad(ang_end)
    dth = a1_rad - a0_rad
    area = 0.5 * (re ** 2 - ri ** 2) * dth
    return area


# Function to calculate the centroid of a wedge in the radio direction
def circ_centroid(ri, re):
    # return (2/3) * (re**3 - ri**3) / (re**2 - ri**2)
    return (2 * (ri ** 2 + ri * re + re ** 2)) / (3 * (ri + re))


def circ_patch_centroid(number_fibers_theta, number_fibers_radius, yC, zC, radius_begin, radius_end, angle_beginning,
                        angle_end):
    if number_fibers_theta <= 0 or number_fibers_radius <= 0:
        raise ValueError("Number of fibers must be positive.")

    # Convert angles from degrees to radians
    a0_rad = np.deg2rad(angle_beginning)
    a1_rad = np.deg2rad(angle_end)

    # Calculate the radial and angular increments
    dr = (radius_end - radius_begin) / number_fibers_radius
    dth = (a1_rad - a0_rad) / number_fibers_theta

    total_area = 0
    cx_weighted_sum = 0
    cy_weighted_sum = 0

    for j in range(number_fibers_radius):
        rj = radius_begin + j * dr
        rj1 = rj + dr
        for i in range(number_fibers_theta):
            thi = a0_rad + i * dth
            thi1 = thi + dth

            # Area of each wedge-shaped fiber
            fiber_area = 0.5 * (rj1 ** 2 - rj ** 2) * dth

            # Centroid of each wedge-shaped fiber in polar coordinates
            r_centroid = ((2 * (rj ** 2 + rj * rj1 + rj1 ** 2)) / (3 * (rj + rj1)))
            theta_centroid = (thi + thi1) / 2

            # Convert to Cartesian coordinates
            cx = yC + r_centroid * np.cos(theta_centroid)
            cy = zC + r_centroid * np.sin(theta_centroid)

            total_area += fiber_area
            cx_weighted_sum += fiber_area * cx
            cy_weighted_sum += fiber_area * cy

    # Calculate the weighted total area sum
    total_area_weighted_sum = total_area

    # Calculate plastic centroid coordinates
    plastic_centroid_x = cx_weighted_sum / total_area_weighted_sum
    plastic_centroid_y = cy_weighted_sum / total_area_weighted_sum

    return plastic_centroid_y, plastic_centroid_x


# Function to calculate the centroid of a circular layer
def circ_layer_centroid(number_bars, yC, zC, radius, angle_beginning, angle_end):
    if number_bars <= 0:
        raise ValueError("Number of bars must be positive.")

    # Convert angles from degrees to radians
    a0_rad = np.deg2rad(angle_beginning)
    a1_rad = np.deg2rad(angle_end)

    # Adjust the end angle if it exceeds a full circle
    if (a1_rad - a0_rad) >= 2 * np.pi:
        a1_rad = a0_rad + 2 * np.pi - 2 * np.pi / number_bars

    # Generate the angular positions of the bars
    thetas = np.linspace(a0_rad, a1_rad, number_bars)

    # Calculate the coordinates of each bar
    Y = yC + radius * np.cos(thetas)
    Z = zC + radius * np.sin(thetas)

    # Calculate the centroid (average position) of the bars
    cx = np.mean(Y)
    cy = np.mean(Z)

    return cx, cy


def Seccion_CP(fib_sec, materials):
    # Define number of decimals for rounding
    num_decimals = 4
    
    # Initialize variables for centroid calculation
    total_weighted_area = 0.0
    cx_weighted_sum = 0.0
    cy_weighted_sum = 0.0

    # Loop over fibers
    for fiber in fib_sec:
        if fiber[0] == 'patch':
            mat_id = fiber[2]
            if fiber[1] == 'quad':
                coords = fiber[5:]
                cx, cy, area = quad_centroid_area(coords)
            elif fiber[1] == 'rect':
                coords = fiber[5:]
                area = rect_area(coords)
                cx, cy = rect_centroid(coords)
            elif fiber[1] == 'circ':
                n_fib_th = fiber[3]
                n_fib_r = fiber[4]
                yC, zC = fiber[5], fiber[6]
                ri, re = fiber[7], fiber[8]
                ang_beg, ang_end = fiber[9], fiber[10]
                area = area_circ_wedge(ri, re, ang_beg, ang_end)
                cx, cy = circ_patch_centroid(n_fib_th, n_fib_r, yC, zC, ri, re, ang_beg, ang_end)
            total_weighted_area += area * materials[str(mat_id)]
            cx_weighted_sum += area * cx * materials[str(mat_id)]
            cy_weighted_sum += area * cy * materials[str(mat_id)]
        elif fiber[0] == 'layer':
            mat_id = fiber[2]
            num_bars = fiber[3]
            As = fiber[4]
            area = As * num_bars
            if fiber[1] == 'straight':
                y1, z1, y2, z2 = fiber[5:]
                cx, cy = (y1 + y2) / 2.0, (z1 + z2) / 2.0
            elif fiber[0] == 'layer' and fiber[1] == 'circ':
                yC = fiber[5]
                zC = fiber[6]
                r = fiber[7]
                a_beg = fiber[8]
                a_end = fiber[9]
                cx, cy = circ_layer_centroid(num_bars, yC, zC, r, a_beg, a_end)
            total_weighted_area += area * materials[str(mat_id)]
            cx_weighted_sum += area * cx * materials[str(mat_id)]
            cy_weighted_sum += area * cy * materials[str(mat_id)]

    # Calculate plastic centroid coordinates
    plastic_centroid_x = cx_weighted_sum / total_weighted_area  # round(, 6)
    plastic_centroid_y = cy_weighted_sum / total_weighted_area  # round(, 6)

    print(f"Plastic Centroid: ({plastic_centroid_x}, {plastic_centroid_y})")

    # Adjust coordinates to the plastic centroid
    adjusted_fib_sec = []

    for fiber in fib_sec:
        if fiber[0] == 'section':
            adjusted_fib_sec.append(fiber)
        elif fiber[0] == 'patch':
            mat_id = fiber[2]
            if fiber[1] == 'quad':
                coords = fiber[5:]
                adjusted_coords = []
                for i in range(0, len(coords), 2):
                    adjusted_coords.append(round(coords[i] - plastic_centroid_x, num_decimals))
                    adjusted_coords.append(round(coords[i + 1] - plastic_centroid_y, num_decimals))
                adjusted_fib_sec.append(['patch', 'quad', mat_id, fiber[3], fiber[4]] + adjusted_coords)
            elif fiber[1] == 'rect':
                coords = fiber[5:]
                adjusted_coords = [round(coords[0] - plastic_centroid_x, num_decimals), 
                                   round(coords[1] - plastic_centroid_y, num_decimals),
                                   round(coords[2] - plastic_centroid_x, num_decimals), 
                                   round(coords[3] - plastic_centroid_y, num_decimals)]
                adjusted_fib_sec.append(['patch', 'rect', mat_id, fiber[3], fiber[4]] + adjusted_coords)
            elif fiber[1] == 'circ':
                ri, re = fiber[7], fiber[8]
                cx, cy = fiber[5], fiber[6]
                adjusted_cx, adjusted_cy = round(cx - plastic_centroid_x, num_decimals), round(cy - plastic_centroid_y, num_decimals)
                adjusted_fib_sec.append(
                    ['patch', 'circ', mat_id, fiber[3], fiber[4], adjusted_cx, adjusted_cy, ri, re, fiber[9],
                     fiber[10]])
        elif fiber[0] == 'layer':
            mat_id = fiber[2]
            if fiber[1] == 'straight':
                coords = fiber[5:]
                adjusted_coords = []
                for i in range(0, len(coords), 2):
                    adjusted_coords.append(round(coords[i] - plastic_centroid_x, num_decimals))
                    adjusted_coords.append(round(coords[i + 1] - plastic_centroid_y, num_decimals))
                adjusted_fib_sec.append(['layer', 'straight', mat_id, fiber[3], fiber[4]] + adjusted_coords)
            elif fiber[1] == 'circ':
                num_bars = fiber[3]
                As = fiber[4]
                cx, cy = fiber[5], fiber[6]
                adjusted_cx, adjusted_cy = round(cx - plastic_centroid_x, num_decimals), round(cy - plastic_centroid_y, num_decimals)
                adjusted_fib_sec.append(
                    ['layer', 'circ', mat_id, fiber[3], fiber[4], adjusted_cx, adjusted_cy, fiber[7], fiber[8],
                     fiber[9]])

    return adjusted_fib_sec
