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
from matplotlib.patches import Circle, Polygon, Wedge, Patch
import shutil
import os


# %% [01] FUNCIONES
# plot_fiber_section is inspired by plotSection matlab function
# written by D. Vamvatsikos available at
# http://users.ntua.gr/divamva/software.html (plotSection.zip)
def plot_fiber_section(fib_sec_list, xlabel_x, ylabel_x, fillflag=1, mat_tag_color=False,
                       matcolor=None, fibers = True, zoom=1):
    """Plot fiber cross-section.

    Args:
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

    if matcolor is None:
        matcolor = ['y', 'gray', 'lightblue', 'g', 'm', 'pink',
                    '#98FB98', '#E6E6FA', '#FFDAB9', '#CCCCFF',
                    '#FA8072', '#00FFFF', '#FFFACD', '#C8A2C8',
                    '#AFEEEE', '#F08080', '#87CEEB', '#D8BFD8',
                    '#FFA07A', '#B0E0E6', '#FFEFD5']
        # Initialize an empty dictionary to store matTag as keys and their 
        # corresponding colors as values. To see legend of colors.
        matTag_colors = {}
    
    # Create figure with the size that I want
    desired_width_px = 635
    desired_height_px = 807 * zoom
    dpi = 100  # You can adjust this value according to your needs

    # Calculate the size in inches
    width_in_inches = desired_width_px / dpi
    height_in_inches = desired_height_px / dpi

    # Create the figure with the specified size and DPI
    fig, ax = plt.subplots(figsize=(width_in_inches, height_in_inches), dpi=dpi)
    
    # Set the position of the axes object
    # Example: set_position([left, bottom, width, height])
    ax.set_position([0.12, 0.07, 0.85, 0.91])
    
    
    ax.set_xlabel('z')
    # ax.invert_xaxis()  # To make z-axis positive to the left
    ax.set_ylabel('y')
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
                for zi, yi in zip(Z, Y):
                    # To higlight the fibers
                    if matTag == 21 and mat_tag_color == False:
                        bar = Circle((zi, yi), r, ec='k', fc=matcolor[matTag - 1], zorder=10)
                    elif mat_tag_color == True:
                        bar = Circle((zi, yi), r, ec='k', fc=matcolor[matTag - 1], zorder=10)
                        matTag_colors[matTag] = matcolor[matTag - 1]
                    else:
                        bar = Circle((zi, yi), r, ec='k', fc='k', zorder=10)
                    ax.add_patch(bar)
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
                for zi, yi in zip(Z, Y):
                    # To higlight the fibers
                    if matTag == 21 and mat_tag_color == False:
                        bar = Circle((zi, yi), r, ec='k', fc=matcolor[matTag - 1], zorder=10)
                    elif mat_tag_color == True:
                        bar = Circle((zi, yi), r, ec='k', fc=matcolor[matTag - 1], zorder=10)
                        matTag_colors[matTag] = matcolor[matTag - 1]
                    else:
                        bar = Circle((zi, yi), r_bar, ec='k', fc='k', zorder=10)
                    ax.add_patch(bar)

        if (item[0] == 'patch' and (item[1] == 'quad' or item[1] == 'quadr' or
                                    item[1] == 'rect')):
            matTag, nIJ, nJK = item[2], item[3], item[4]

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
                
                # Only if the fibers are going to be plotted
                if fibers:
                    for j in range(nIJ):
                        for k in range(nJK):
                            zy = np.array([[Z[j, k], Y[j, k]],
                                        [Z[j, k + 1], Y[j, k + 1]],
                                        [Z[j + 1, k + 1], Y[j + 1, k + 1]],
                                        [Z[j + 1, k], Y[j + 1, k]]])
                            poly = Polygon(zy, closed=True, ec='k', fc=matcolor[matTag - 1])
                            ax.add_patch(poly)
                            if mat_tag_color == True:
                                matTag_colors[matTag] = matcolor[matTag - 1]  # Save color to legend
                # If the fibers are not going to be plotted
                else:
                    zy = np.array([[Iz, Iy], [Jz, Jy], [Kz, Ky], [Lz, Ly]])
                    poly = Polygon(zy, closed=True, ec='k', fc=matcolor[matTag - 1])
                    ax.add_patch(poly)
                    if mat_tag_color == True:
                        matTag_colors[matTag] = matcolor[matTag - 1]  # Save color to legend
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

            # If the fibers are going to be plotted
            if fibers:
                for j in range(nr):
                    rj = ri + j * dr
                    rj1 = rj + dr

                    for i in range(nc):
                        thi = a0 + i * dth
                        thi1 = thi + dth
                        wedge = Wedge((zC, yC), rj1, thi, thi1, width=dr, ec='k',
                                    lw=1, fc=matcolor[matTag - 1])
                        ax.add_patch(wedge)
                        if mat_tag_color == True:
                            matTag_colors[matTag] = matcolor[matTag - 1]  # Save color to legend
            
            # If the fibers are not going to be plotted
            else:
                wedge = Wedge((zC, yC), re, a0, a1, width=re-ri, ec='k', lw=1, fc=matcolor[matTag - 1])
                ax.add_patch(wedge)
                if mat_tag_color == True:
                    matTag_colors[matTag] = matcolor[matTag - 1] # Save color to legend

            ax.axis('equal')
    ax.axis('equal')
    
    # Legend of colors
    if mat_tag_color:
        # Create a list of patches for the legend
        patches = [Patch(color=color, label=f'MatTag {matTag}') for matTag, color in matTag_colors.items()]
        # Add the legend to the plot
        ax.legend(handles=patches, loc='upper left', bbox_to_anchor=(0.80, 1.02)) # 1.16
        
    # Add labels and grid
    ax.set_xlabel(xlabel_x)
    ax.set_ylabel(ylabel_x)


# plot_fiber_section is inspired by plotSection matlab function
# written by D. Vamvatsikos available at
# http://users.ntua.gr/divamva/software.html (plotSection.zip)
def foto_fiber_section(fib_sec_list, url_x, xlabel_x, ylabel_x, fillflag=1,
                       matcolor=None):
    """Plot fiber cross-section.

    Args:
        xlabel_x: Label of horizontal axis

        ylabel_x: Label of vertical axis

        url_x: Directory to save frames

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

    if matcolor is None:
        matcolor = ['y', 'gray', 'lightblue', 'g', 'm', 'pink',
                    '#98FB98', '#E6E6FA', '#FFDAB9', '#CCCCFF',
                    '#FA8072', '#00FFFF', '#FFFACD', '#C8A2C8',
                    '#AFEEEE', '#F08080', '#87CEEB', '#D8BFD8',
                    '#FFA07A', '#B0E0E6', '#FFEFD5']
    # Frames directory
    try:
        os.mkdir(url_x)
    except FileExistsError:
        shutil.rmtree(url_x)
        os.mkdir(url_x)

    # Create figure with the size that I want
    desired_width_px = 640
    desired_height_px = 864
    dpi = 100  # You can adjust this value according to your needs

    # Calculate the size in inches
    width_in_inches = desired_width_px / dpi
    height_in_inches = desired_height_px / dpi

    # Create the figure with the specified size and DPI
    fig, ax = plt.subplots(figsize=(width_in_inches, height_in_inches), dpi=dpi)
    
    # Set the position of the axes object
    # Example: set_position([left, bottom, width, height])
    ax.set_position([0.12, 0.07, 0.85, 0.91])
    
    
    ax.set_xlabel('z')
    # ax.invert_xaxis()  # To make z-axis positive to the left
    ax.set_ylabel('y')
    ax.grid(False)
    frame_count = 1  # Counter for frame number
    ax.set_xlim(-0.6, 0.6)
    ax.set_ylim(-0.4, 0.4)

    # Add labels and grid
    ax.set_xlabel(xlabel_x)
    ax.set_ylabel(ylabel_x)

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
                for zi, yi in zip(Z, Y):
                    bar = Circle((zi, yi), r, ec='k', fc='k', zorder=10)
                    ax.add_patch(bar)
                    # Save frame
                    ax.axis('equal')
                    plt.savefig(f'{url_x}/{frame_count:07d}.png')
                    frame_count += 1
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
                for zi, yi in zip(Z, Y):
                    bar = Circle((zi, yi), r_bar, ec='k', fc='k', zorder=10)
                    ax.add_patch(bar)
                    # Save frame
                    ax.axis('equal')
                    plt.savefig(f'{url_x}/{frame_count:07d}.png')
                    frame_count += 1

        if (item[0] == 'patch' and (item[1] == 'quad' or item[1] == 'quadr' or
                                    item[1] == 'rect')):
            matTag, nIJ, nJK = item[2], item[3], item[4]

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
                        # Save frame
                        ax.axis('equal')
                        plt.savefig(f'{url_x}/{frame_count:07d}.png')
                        frame_count += 1

            else:
                # horizontal lines
                for az, bz, ay, by in zip(IJz, LKz, IJy, LKy):
                    plt.plot([az, bz], [ay, by], 'b-', zorder=1)
                    # Save frame
                    plt.savefig(f'{url_x}/{frame_count:07d}.png')
                    frame_count += 1

                # vertical lines
                for az, bz, ay, by in zip(JKz, ILz, JKy, ILy):
                    plt.plot([az, bz], [ay, by], 'b-', zorder=1)
                    # Save frame
                    ax.axis('equal')
                    plt.savefig(f'{url_x}/{frame_count:07d}.png')
                    frame_count += 1

        if item[0] == 'patch' and item[1] == 'circ':
            matTag, nc, nr = item[2], item[3], item[4]

            yC, zC, ri, re = item[5], item[6], item[7], item[8]
            a0, a1 = item[9], item[10]

            dr = (re - ri) / nr
            dth = (a1 - a0) / nc

            for j in range(nr):
                rj = ri + j * dr
                rj1 = rj + dr

                for i in range(nc):
                    thi = a0 + i * dth
                    thi1 = thi + dth
                    wedge = Wedge((zC, yC), rj1, thi, thi1, width=dr, ec='k',
                                  lw=1, fc=matcolor[matTag - 1])
                    ax.add_patch(wedge)
                    # Save frame
                    ax.axis('equal')
                    plt.savefig(f'{url_x}/{frame_count:07d}.png')
                    frame_count += 1

            ax.axis('equal')
    ax.axis('equal')

