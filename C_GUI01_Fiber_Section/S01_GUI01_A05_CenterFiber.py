# -*- coding: utf-8 -*-
"""
ACTUALIZACION:  2024-05-15
AUTOR:          Marcelo Ortiz Á.
SCRIPT:         S01_GUI01_A02_Graf_Sec_OPSVIS.py
COMENTARIOS:    Grafica seccion usando el codigo de OPSVIS adaptado para GUI
                de Jupyter Notebook. Básicamente, se quita el invert_xaxis.
                Además se añade funcion para graficar video de seccion.
"""

# %% [00] LIBRERIAS
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Wedge
import shutil
import os


# %% [01] FUNCIONES
# plot_fiber_section is inspired by plotSection matlab function
# written by D. Vamvatsikos available at
# http://users.ntua.gr/divamva/software.html (plotSection.zip)
def plot_center_fiber_section(fib_sec_list, xlabel_x, ylabel_x, color_PM="r", fillflag=1,
                              matcolor=None):
    """Plot fiber cross-section and the center of fibers.

    Args:
        color_PM: Color of the point in the center of the fiber

        xlabel_x: Label of horizontal axis

        ylabel_x: Label of vertical axis

        fib_sec_list (list): list of lists in the format similar to the parameters
            for the section, layer, patch, fiber OpenSees commands

        fillflag (int): 1 - filled fibers with color specified in matcolor
            list, 0 - no color, only the outline of fibers

        matcolor (list): sequence of colors for various material tags
            assigned to fibers

    Examples:
        ::

            fib_sec_1 = [['section', 'Fiber', 1, '-GJ', 1.0e6],
                         ['patch', 'quad', 1, 4, 1,  0.032, 0.317, -0.311, 0.067, -0.266, 0.005, 0.077, 0.254],  # noqa: E501
                         ['patch', 'quad', 1, 1, 4,  -0.075, 0.144, -0.114, 0.116, 0.075, -0.144, 0.114, -0.116],  # noqa: E501
                         ['patch', 'quad', 1, 4, 1,  0.266, -0.005,  -0.077, -0.254,  -0.032, -0.317,  0.311, -0.067]  # noqa: E501
                         ]
            opsv.fib_sec_list_to_cmds(fib_sec_1)
            matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
            opsv.plot_fiber_section(fib_sec_1, matcolor=matcolor)
            plt.axis('equal')
            # plt.savefig('fibsec_rc.png')
            plt.show()

    Notes:
        ``fib_sec_list`` can be reused by means of a python helper function
            ``opsvis.fib_sec_list_to_cmds(fib_sec_list_1)``

    See also:
        ``opsvis.fib_sec_list_to_cmds()``
    """
    # Define colors
    if matcolor is None:
        matcolor = ['y', 'gray', 'lightblue', 'g', 'm', 'pink',
                    '#98FB98', '#E6E6FA', '#FFDAB9', '#CCCCFF',
                    '#FA8072', '#00FFFF', '#FFFACD', '#C8A2C8',
                    '#AFEEEE', '#F08080', '#87CEEB', '#D8BFD8',
                    '#FFA07A', '#B0E0E6', '#FFEFD5']
    # Create vectors with centers of fibers
    center_fiber_patch = []
    center_fiber_straight = []
    center_fiber_circle = []
    center_fiber_wedge = []

    # Create figure and axis
    fig, ax = plt.subplots()
    # Add labels and grid
    ax.set_xlabel(xlabel_x)
    ax.set_ylabel(ylabel_x)
    ax.grid(False)

    for item in fib_sec_list:

        if item[0] == 'layer':
            matTag = item[2]
            if item[1] == 'straight':
                n_bars = item[3]
                As = item[4]
                Iy, Iz, Jy, Jz = item[5], item[6], item[7], item[8]
                r = np.sqrt(As / np.pi)
                Y = np.linspace(Iy, Jy, n_bars)
                Z = np.linspace(Iz, Jz, n_bars)
                aux_straight = []  # auxiliar list to store the center of fibers
                for zi, yi in zip(Z, Y):
                    bar = Circle((zi, yi), r, ec='k', fc='k', zorder=10)
                    ax.add_patch(bar)
                    # draw point in the center of the fiber
                    ax.scatter(zi, yi, color=color_PM, s=0.8, zorder=20)
                    aux_straight.append([zi, yi])
                center_fiber_straight.append(aux_straight)
            if item[1] == 'circ':
                n_bars, As = item[3], item[4]
                yC, zC, arc_radius = item[5], item[6], item[7]
                if len(item) > 8:
                    a0_deg, a1_deg = item[8], item[9]
                    if (a1_deg - a0_deg) >= 360. and n_bars > 0:
                        a1_deg = a0_deg + 360. - 360. / n_bars
                else:
                    a0_deg, a1_deg = 0., 360. - 360. / n_bars

                a0_rad, a1_rad = np.pi * a0_deg / 180., np.pi * a1_deg / 180.
                r_bar = np.sqrt(As / np.pi)
                thetas = np.linspace(a0_rad, a1_rad, n_bars)
                Y = yC + arc_radius * np.cos(thetas)
                Z = zC + arc_radius * np.sin(thetas)
                aux_circle = []  # auxiliar list to store the center of fibers
                for zi, yi in zip(Z, Y):
                    bar = Circle((zi, yi), r_bar, ec='k', fc='k', zorder=10)
                    ax.add_patch(bar)
                    # draw point in the center of the fiber
                    ax.scatter(zi, yi, color=color_PM, s=0.8, zorder=20)
                    aux_circle.append([zi, yi])
                center_fiber_circle.append(aux_circle)

        if (item[0] == 'patch' and (item[1] == 'quad' or item[1] == 'quadr' or
                                    item[1] == 'rect')):
            matTag, nIJ, nJK = item[2], item[3], item[4]

            aux_quad = []  # auxiliar list to store the center of fibers

            if item[1] == 'quad' or item[1] == 'quadr':
                Iy, Iz, Jy, Jz = item[5], item[6], item[7], item[8]
                Ky, Kz, Ly, Lz = item[9], item[10], item[11], item[12]

            if item[1] == 'rect':
                Iy, Iz, Ky, Kz = item[5], item[6], item[7], item[8]
                Jy, Jz, Ly, Lz = Ky, Iz, Iy, Kz

            # check for convexity (vector products)
            outIJxIK = (Jy - Iy) * (Kz - Iz) - (Ky - Iy) * (Jz - Iz)
            outIKxIL = (Ky - Iy) * (Lz - Iz) - (Ly - Iy) * (Kz - Iz)
            # check if I, J, L points are colinear
            outIJxIL = (Jy - Iy) * (Lz - Iz) - (Ly - Iy) * (Jz - Iz)
            # outJKxJL = (Ky-Jy)*(Lz-Jz) - (Ly-Jy)*(Kz-Jz)

            if outIJxIK <= 0 or outIKxIL <= 0 or outIJxIL <= 0:
                print(
                    '\nWarning! Patch quad is non-convex or counter-clockwise defined or has at least 3 colinear points in line')  # noqa: E501

            IJz, IJy = np.linspace(Iz, Jz, nIJ + 1), np.linspace(Iy, Jy, nIJ + 1)
            JKz, JKy = np.linspace(Jz, Kz, nJK + 1), np.linspace(Jy, Ky, nJK + 1)
            LKz, LKy = np.linspace(Lz, Kz, nIJ + 1), np.linspace(Ly, Ky, nIJ + 1)
            ILz, ILy = np.linspace(Iz, Lz, nJK + 1), np.linspace(Iy, Ly, nJK + 1)

            if fillflag:
                Z = np.zeros((nIJ + 1, nJK + 1))
                Y = np.zeros((nIJ + 1, nJK + 1))

                for j in range(nIJ + 1):
                    Z[j, :] = np.linspace(IJz[j], LKz[j], nJK + 1)
                    Y[j, :] = np.linspace(IJy[j], LKy[j], nJK + 1)

                for j in range(nIJ):
                    for k in range(nJK):
                        zy = np.array([[Z[j, k], Y[j, k]],
                                       [Z[j, k + 1], Y[j, k + 1]],
                                       [Z[j + 1, k + 1], Y[j + 1, k + 1]],
                                       [Z[j + 1, k], Y[j + 1, k]]])
                        poly = Polygon(zy, closed=True, ec='k', fc=matcolor[matTag - 1])
                        ax.add_patch(poly)
                        # draw point in the center of the fiber
                        center_x, center_y = find_polygon_center(zy)
                        ax.scatter(center_x, center_y, color=color_PM, s=0.8, zorder=20)
                        aux_quad.append([center_x, center_y])
                center_fiber_patch.append(aux_quad)
            else:
                # horizontal lines
                for az, bz, ay, by in zip(IJz, LKz, IJy, LKy):
                    plt.plot([az, bz], [ay, by], 'b-', zorder=1)

                # vertical lines
                for az, bz, ay, by in zip(JKz, ILz, JKy, ILy):
                    plt.plot([az, bz], [ay, by], 'b-', zorder=1)

        if item[0] == 'patch' and item[1] == 'circ':
            matTag, nc, nr = item[2], item[3], item[4]

            yC, zC, ri, re = item[5], item[6], item[7], item[8]
            a0, a1 = item[9], item[10]

            dr = (re - ri) / nr
            dth = (a1 - a0) / nc

            aux_wedge = []  # auxiliar list to store the center of fibers

            for j in range(nr):
                rj = ri + j * dr
                rj1 = rj + dr

                for i in range(nc):
                    thi = a0 + i * dth
                    thi1 = thi + dth
                    wedge = Wedge((zC, yC), rj1, thi, thi1, width=dr, ec='k',
                                  lw=1, fc=matcolor[matTag - 1])
                    ax.add_patch(wedge)
                    # draw point in the center of the fiber
                    center_x, center_y = wedge_center(wedge)
                    ax.scatter(center_x, center_y, color=color_PM, s=0.8, zorder=20)
                    aux_wedge.append([center_x, center_y])
            center_fiber_wedge.append(aux_wedge)

            ax.axis('equal')
    ax.axis('equal')
    return center_fiber_patch, center_fiber_straight, center_fiber_circle, center_fiber_wedge


# %%  [02] SUPPORT FUNCTIONS
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
    return center_x_fun, center_y_fun


# Function to calculate the center of a wedge
def wedge_center(wedge):
    center = wedge.center
    radius = wedge.r
    width = wedge.width
    theta1, theta2 = wedge.theta1, wedge.theta2

    # Calculate the midpoint angle in radians
    midpoint_angle = np.radians((theta1 + theta2) / 2)

    # Calculate midpoint radius between the inner and outer radii
    inner_radius = radius - width if width else 0
    midpoint_radius = (inner_radius + radius) / 2

    # Calculate the coordinates of the midpoint
    x_center = center[0] + midpoint_radius * np.cos(midpoint_angle)
    y_center = center[1] + midpoint_radius * np.sin(midpoint_angle)

    return x_center, y_center


# %%  [02] TEST

if __name__ == '__main__':

    aux_Test_find_polygon_center = True
    aux_Test_plot_center_fiber_section = False

    if aux_Test_find_polygon_center:
        # Test function find_polygon_center:
        import math
        # Create a zy array representing a square polygon
        zy_x = np.array([[0, 0],  # Bottom left vertex
                         [3 * math.cos(math.pi / 6), 3 * math.sin(math.pi / 6)],
                         [3 * 2 ** 0.5 * math.cos(math.pi / 6 + math.pi / 4),
                          3 * 2 ** 0.5 * math.sin(math.pi / 6 + math.pi / 4)],
                         [1 * math.cos(math.pi / 6 + math.pi / 4),
                          1 * math.sin(math.pi / 6 + math.pi / 4)]])

        # Use the find_polygon_center function
        center_x_test, center_y_test = find_polygon_center(zy_x)
        print(f"The center of the polygon is at ({center_x_test}, {center_y_test})")
        center_x_theoretic = (2 ** 2 + 1 ** 2) ** 0.5 * math.cos(math.pi / 6 + math.atan(1 / 2))
        center_y_theoretic = (2 ** 2 + 1 ** 2) ** 0.5 * math.sin(math.pi / 6 + math.atan(1 / 2))
        print(
            f"Theoretic center of a triangle rectangle with sides 3, 3, 3*2**0.5 rotated pi/6 is at ({center_x_theoretic},{center_y_theoretic})")
        
        # Graphic of the polygon and center point
        fig_x, ax_x = plt.subplots()
        poly_x = Polygon(zy_x, closed=True, ec='k', fc='lightblue')
        ax_x.add_patch(poly_x)
        ax_x.scatter(center_x_test, center_y_test, color='r', s=100)
        ax_x.axis('equal')
        plt.show()

    if aux_Test_plot_center_fiber_section:
        # Test function plot_center_fiber_section:
        # Define fiber section
        fib_sec_1 = [['section', 'Fiber', 1, '-GJ', 1.0e6],
                     ['patch', 'quad', 1, 4, 1,  0.032, 0.317, -0.311, 0.067, -0.266, 0.005, 0.077, 0.254],  # noqa: E501
                     ['patch', 'quad', 1, 1, 4,  -0.075, 0.144, -0.114, 0.116, 0.075, -0.144, 0.114, -0.116],  # noqa: E501
                     ['patch', 'quad', 1, 4, 1,  0.266, -0.005,  -0.077, -0.254,  -0.032, -0.317,  0.311, -0.067]  # noqa: E501
                     ]
        # Labels
        xlabel = 'y [m]'
        ylabel = 'z [m]'

        # List with data of center of fibers
        center_fiber_patch_x, center_fiber_straight_x, center_fiber_circle_x, center_fiber_wedge_x = (
            plot_center_fiber_section(fib_sec_1, xlabel, ylabel))

        # Show the plot
        plt.show()

        # Print the center of fibers
        print("Center of fibers in patch fibers:")
        print(center_fiber_patch_x)
        print("Center of fibers in straight fibers:")
        print(center_fiber_straight_x)
        print("Center of fibers in circular fibers:")
        print(center_fiber_circle_x)
        print("Center of fibers in wedge fibers:")
        print(center_fiber_wedge_x)
