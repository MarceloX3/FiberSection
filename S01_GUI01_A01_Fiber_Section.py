# -*- coding: utf-8 -*-
"""
ACTUALIZACION:  2024-05-21
AUTOR:          Marcelo Ortiz Á.
SCRIPT:         S01_GUI01_A01_Fiber_Section.py
COMENTARIOS:    Interfaz gráfica de usuario para definicion de sección en base a fibras. Sección desarrollada acorde
                a los requerimientos de libreria OPSVIS.
"""

# %% [00] INTRODUCTION
# GUI in Jupyter Notebook that generate the section of a fiber element in OpenSeespy. 

# (.ipynb):                         %run S01_GUI01_A01_Fiber_Section.py


# %% [01] LIBRARIES
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Dropdown, IntText, Textarea, Output, Text
from IPython.display import display, Image, Video
import os
import shutil
import math

import sys
sys.path.insert(0, './C_GUI01_Fiber_Section')
import S01_GUI01_A02_Graf_Sec_OPSVIS as opsv1
import S01_GUI01_A03_Video as vid
import S01_GUI01_A04_CP as CP
import S01_GUI01_A05_CenterFiber as CF

# %% [02] INITIALIZATION
# Create directories for the GUI in case it doesn't exist.
def create_directory(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


# Directories to create
directories = ['C_GUI01_Fiber_Section/C_GUI01_Fiber_Section',
               'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones',
               'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Fotogramas_Video']

# Create all directories
for dir_i in directories:
    create_directory(dir_i)


# %% [03] FUNCTIONS

# %%% [03-00] UPDATE DROPDOWNS
# Function to update the type dropdown based on element type
def update_patch_layer_type_options(change):
    if element_type_dropdown.value == 'patch':
        patch_layer_type_dropdown.options = ['rect', 'quad', 'circ']
        patch_layer_type_dropdown.value = 'rect'
    elif element_type_dropdown.value == 'layer':
        patch_layer_type_dropdown.options = ['straight', 'circ']
        patch_layer_type_dropdown.value = 'straight'
    update_input_widgets()


# Function to update the "Unit" dropdown based on "Graphic Unit"
def update_unit_options(change):
    if graphic_unit_dropdown.value == '-':
        unit_dropdown.options = ['-']
    else:
        unit_dropdown.options = ['m', 'cm', 'mm', 'ft', 'IN']
        unit_dropdown.value = 'cm'
    update_input_widgets()


# Function to update the "Edit Patch/Layer" dropdown based on the actual section
def update_edit_patch_layer_options(change):
    if code_params_output.value == '':
        return
    
    try:
        params = eval(section_params_output.value)
        if not isinstance(params, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = section_params_output.value
        # section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return

    # If there are patch or layer elements in the section, enable the dropdown
    if len(params) > 1:
        edit_patch_layer_dropdown.disabled = False
    
        # Find all the patch and layer elements in the section
        patch_layer_elements = []
        for item in params:
            if item[0] in ['patch', 'layer']:
                patch_layer_elements.append(item)
        
        # Create the options for the dropdown
        options = [str(item) for item in patch_layer_elements]
        
        # Insert the option '-' in the 0 position
        options.insert(0, '-')
        
        # Update the dropdown options
        edit_patch_layer_dropdown.options = options
    
    # If there are no patch or layer elements in the section, disable the dropdown
    else:
        edit_patch_layer_dropdown.disabled = True
        edit_patch_layer_dropdown.options = ['-']
        edit_patch_layer_dropdown.value = '-'


# %%% [03-01] INPUT DATA
# Function to update input widgets layout based on patch or layer type
def update_input_widgets(change=None):
    element_type = element_type_dropdown.value
    patch_layer_type = patch_layer_type_dropdown.value
    unit = unit_dropdown.value
    text_patch_layer_param = widgets.HTML(value="Patch/Layer Parameters:", layout=widgets.Layout(margin="0px 0 0 2px"))
    text_patch_layer_param.style.font_size = '14px'

    def update_description(widget_x, desc):
        if unit != '-':
            if 'as:' in widget_x.description.lower():
                widget_x.description = f"{desc} [{unit}\u00b2]"
            else:
                widget_x.description = f"{desc} [{unit}]"
        else:
            widget_x.description = desc

    # Only update the widgets if the section is being added
    if add_section_button.description == 'Delete Section':
        if element_type == 'patch':
            if patch_layer_type == 'rect':
                new_widgets = [text_patch_layer_param, material_tag_input, nFibY_input, nFibZ_input, y1_input, z1_input, y2_input, z2_input]
                update_description(y1_input, 'y1:')
                update_description(z1_input, 'z1:')
                update_description(y2_input, 'y2:')
                update_description(z2_input, 'z2:')
            elif patch_layer_type == 'quad':
                new_widgets = [text_patch_layer_param, material_tag_input, numSubdivIJ_input, numSubdivJK_input, yI_input, zI_input, yJ_input,
                               zJ_input, yK_input, zK_input, yL_input, zL_input]
                update_description(yI_input, 'yI:')
                update_description(zI_input, 'zI:')
                update_description(yJ_input, 'yJ:')
                update_description(zJ_input, 'zJ:')
                update_description(yK_input, 'yK:')
                update_description(zK_input, 'zK:')
                update_description(yL_input, 'yL:')
                update_description(zL_input, 'zL:')
            elif patch_layer_type == 'circ':
                new_widgets = [text_patch_layer_param, material_tag_input, numSubdivCirc_input, numSubdivRad_input, yc_input, zc_input,
                               r_ini_input,
                               r_end_input, ang_ini_input, ang_end_input]
                update_description(yc_input, 'yc:')
                update_description(zc_input, 'zc:')
                update_description(r_ini_input, 'r_ini:')
                update_description(r_end_input, 'r_end:')
        elif element_type == 'layer':
            if patch_layer_type == 'straight':
                new_widgets = [text_patch_layer_param, material_tag_input, numFiber_input, areaFiber_input, y1_input, z1_input, y2_input,
                               z2_input]
                update_description(areaFiber_input, 'As:')
                update_description(y1_input, 'y1:')
                update_description(z1_input, 'z1:')
                update_description(y2_input, 'y2:')
                update_description(z2_input, 'z2:')
            elif patch_layer_type == 'circ':
                new_widgets = [text_patch_layer_param, material_tag_input, numFiber_input, areaFiber_input, yc_input, zc_input, radius_input,
                               ang_ini_input, ang_end_input]
                update_description(areaFiber_input, 'As:')
                update_description(yc_input, 'yc:')
                update_description(zc_input, 'zc:')
                update_description(radius_input, 'radius:')

        model_widgets.children = new_widgets


# %%% [03-02] BUTTONS

# %%%% [03-02-00] ADD_SECTION_DEFINITION
# Function to add a new section definition and delete actual section and image.
def add_section_definition(change=None):
    if add_section_button.description == 'Add Section':
        add_section_button.description = 'Delete Section'
        add_section_button.style.button_color = 'red'
        add_patch_layer_button.description = 'Define'
        refresh_button.description = 'MatTag'
        video_button.description = 'Video'
        code_button.description = 'Code'
        cover_button.description = 'Cover'
        replicate_button.description = 'Replicate'
        material_button.description = 'Strength'
        CP_button.description = 'Solve PC'
        center_button.description = 'Center'
        edit_patch_layer_button.description = 'Edit'
        cancel_patch_layer_button.description = 'Copy'

        # Enable widgets to define and see patch and layer
        add_patch_layer_button.disabled = False
        refresh_button.disabled = False
        video_button.disabled = False
        code_button.disabled = False
        cover_button.disabled = False
        replicate_button.disabled = False
        CP_button.disabled = False
        material_button.disabled = False
        center_button.disabled = False
        edit_patch_layer_button.disabled = False
        cancel_patch_layer_button.disabled = False
        zoom_dropdown.disabled = False
        fiber_plot_dropdown.disabled = False
        
        # Disable widgets to define the section
        graphic_unit_dropdown.disabled = True
        secTag_input.disabled = True
        GJ_input.disabled = True

        # Add a new section_params_output.
        secTag = secTag_input.value
        GJ = float(GJ_input.value)
        section_def = f"""[
['section', 'Fiber', {secTag}, '-GJ', {GJ}]
]"""
        section_params_output.value = section_def  # str(section_def)
        code_params_output.value = "Section added successfully"

    else:
        # Unfreeze the unit graphic.
        add_section_button.description = 'Add Section'
        add_section_button.style.button_color = 'green'
        add_patch_layer_button.description = '-'
        refresh_button.description = '-'
        video_button.description = '-'
        code_button.description = '-'
        cover_button.description = '-'
        replicate_button.description = '-'
        material_button.description = '-'
        CP_button.description = '-'
        center_button.description = '-'
        cancel_patch_layer_button.description = '-'
        edit_patch_layer_button.description = '-'
        graphic_unit_dropdown.disabled = False
        add_patch_layer_button.disabled = True
        refresh_button.disabled = True
        video_button.disabled = True
        code_button.disabled = True
        cover_button.disabled = True
        replicate_button.disabled = True
        CP_button.disabled = True
        material_button.disabled = True
        center_button.disabled = True
        cancel_patch_layer_button.disabled = True
        edit_patch_layer_button.disabled = True
        patch_layer_type_dropdown.disabled = True
        element_type_dropdown.disabled = True
        unit_dropdown.disabled = True
        zoom_dropdown.disabled = True
        fiber_plot_dropdown.disabled = True
        secTag_input.disabled = False
        GJ_input.disabled = False
        # Delete the section_params_output.
        section_params_output.value = ""
        # Delete the code_params_output.
        code_params_output.value = ""
        # Delete image in out
        out.clear_output()  # wait=False
        model_widgets.children = []


# %%%% [03-02-01] ADD_PATCH_LAYER
# Function auxiliar to add patch or layer definition
def aux_add_patch_layer(change=None):
    # Save the patch or layer definition
    try:
        params = eval(section_params_output.value)
        if not isinstance(params, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = section_params_output.value
        section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return

    element_type = element_type_dropdown.value
    patch_layer_type = patch_layer_type_dropdown.value
    patch_layer_params = [element_type, patch_layer_type, material_tag_input.value]
    unit = unit_dropdown.value

    # Function to add unit to the section definition.
    def unit_patch_layer(value, unit_x, coef):
        if unit_x == "-":
            return value
        else:
            if coef == 1:
                return str(value) + f"*{unit_x}"
            if coef >= 2:
                return str(value) + f"*{unit_x}**{coef}"

    if element_type == 'patch':
        if patch_layer_type == 'rect':
            patch_layer_params += [nFibY_input.value, nFibZ_input.value,
                                unit_patch_layer(float(y1_input.value), unit, 1),
                                unit_patch_layer(float(z1_input.value), unit, 1),
                                unit_patch_layer(float(y2_input.value), unit, 1),
                                unit_patch_layer(float(z2_input.value), unit, 1)]
        elif patch_layer_type == 'quad':
            patch_layer_params += [numSubdivIJ_input.value, numSubdivJK_input.value,
                                unit_patch_layer(float(yI_input.value), unit, 1),
                                unit_patch_layer(float(zI_input.value), unit, 1),
                                unit_patch_layer(float(yJ_input.value), unit, 1),
                                unit_patch_layer(float(zJ_input.value), unit, 1),
                                unit_patch_layer(float(yK_input.value), unit, 1),
                                unit_patch_layer(float(zK_input.value), unit, 1),
                                unit_patch_layer(float(yL_input.value), unit, 1),
                                unit_patch_layer(float(zL_input.value), unit, 1)]
        elif patch_layer_type == 'circ':
            patch_layer_params += [numSubdivCirc_input.value, numSubdivRad_input.value,
                                unit_patch_layer(float(yc_input.value), unit, 1),
                                unit_patch_layer(float(zc_input.value), unit, 1),
                                unit_patch_layer(float(r_ini_input.value), unit, 1),
                                unit_patch_layer(float(r_end_input.value), unit, 1), float(ang_ini_input.value),
                                float(ang_end_input.value)]
    elif element_type == 'layer':
        if patch_layer_type == 'straight':
            patch_layer_params += [numFiber_input.value, unit_patch_layer(float(areaFiber_input.value), unit, 2),
                                unit_patch_layer(float(y1_input.value), unit, 1),
                                unit_patch_layer(float(z1_input.value), unit, 1),
                                unit_patch_layer(float(y2_input.value), unit, 1),
                                unit_patch_layer(float(z2_input.value), unit, 1)]
        elif patch_layer_type == 'circ':
            patch_layer_params += [numFiber_input.value, unit_patch_layer(float(areaFiber_input.value), unit, 2),
                                unit_patch_layer(float(yc_input.value), unit, 1),
                                unit_patch_layer(float(zc_input.value), unit, 1),
                                unit_patch_layer(float(radius_input.value), unit, 1), float(ang_ini_input.value),
                                float(ang_end_input.value)]

    params.append(patch_layer_params)
    params_string = str(params).replace("[[", "[\n[")
    params_string = params_string.replace("], [", "],\n[")
    params_string = params_string.replace("]]", "]\n]")
    section_params_output.value = params_string
    show_section()


# Function to add patch or layer definition
def add_patch_layer(change=None):
    # If the button is in the 'Define' state, the function will show the parameters to define the patch or layer.
    if add_patch_layer_button.description == 'Define':
        # See patch or layer parameters
        update_input_widgets()
        
        # Change the button description and color
        add_patch_layer_button.description = 'Save'
        add_patch_layer_button.style.button_color = 'green'
        
        # Disable the other buttons
        add_section_button.disabled = True
        refresh_button.disabled = True
        video_button.disabled = True
        code_button.disabled = True
        cover_button.disabled = True
        replicate_button.disabled = True
        CP_button.disabled = True
        material_button.disabled = True
        center_button.disabled = True
        edit_patch_layer_button.disabled = True
        edit_patch_layer_dropdown.disabled = True
        
        # Enable the button to cancel the definition
        cancel_patch_layer_button.disabled = False
        # Modify the description of the cancel button and the color
        cancel_patch_layer_button.description = 'Delete'
        cancel_patch_layer_button.style.button_color = 'red'
        
        # Enable the button to show and hide the new patch or layer
        edit_patch_layer_button.disabled = False
        # Modify the description of the edit button
        edit_patch_layer_button.description = 'Hide'
        edit_patch_layer_button.style.button_color = 'blue'
        
        # Enable the dropdowns to define the patch or layer
        patch_layer_type_dropdown.disabled = False
        element_type_dropdown.disabled = False
        unit_dropdown.disabled = False
        
        # Show the actual section with the new patch or layer
        show_section_update()
        
        # Message to the user
        code_params_output.value = "Define the patch or layer parameters"  
    
    
    # If the button is in the 'Save' state, the function will save the patch or layer definition.
    # And show the section with the new patch or layer.
    else:
        # Hide the patch or layer parameters
        model_widgets.children = []
        
        # Change the button description and color
        add_patch_layer_button.description = 'Define'
        add_patch_layer_button.style.button_color = None
        
        # Enable the other buttons
        add_section_button.disabled = False
        refresh_button.disabled = False
        video_button.disabled = False
        code_button.disabled = False
        cover_button.disabled = False
        replicate_button.disabled = False
        CP_button.disabled = False
        material_button.disabled = False
        center_button.disabled = False
        edit_patch_layer_button.disabled = False
        edit_patch_layer_dropdown.disabled = False
        
        # Modify the description of the edit button
        edit_patch_layer_button.description = 'Edit'
        
        # Disable the button to cancel the definition
        cancel_patch_layer_button.disabled = False
        # Modify the description of the cancel button and the color
        cancel_patch_layer_button.description = 'Copy'
        cancel_patch_layer_button.style.button_color = None
        
        # Disable the button to show and hide the new patch or layer
        edit_patch_layer_button.disabled = False
        # Modify the description of the edit button
        edit_patch_layer_button.description = 'Edit'
        edit_patch_layer_button.style.button_color = None
        
        # Disable the dropdowns to define the patch or layer
        patch_layer_type_dropdown.disabled = True
        element_type_dropdown.disabled = True
        unit_dropdown.disabled = True   
        
        # Save the patch or layer definition
        aux_add_patch_layer()
        


# %%%% [03-02-02] SHOW_SECTION
# Function to show the section created
def show_section(change=None):
    try:
        params = eval(section_params_output.value)
        if not isinstance(params, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = section_params_output.value
        section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return

    # Remove unit annotations from the plot parameters
    unit_factors_new = {
        'm': {'m': 1, 'cm': 0.01, 'mm': 0.001, 'ft': 0.3048, 'IN': 0.0254},
        'cm': {'m': 100, 'cm': 1, 'mm': 0.1, 'ft': 30.48, 'IN': 2.54},
        'mm': {'m': 1000, 'cm': 10, 'mm': 1, 'ft': 304.8, 'IN': 25.4},
        'ft': {'m': 3.2808399, 'cm': 0.032808399, 'mm': 0.00328084, 'ft': 1, 'IN': 0.0833333},
        'IN': {'m': 39.370079, 'cm': 0.39370079, 'mm': 0.039370079, 'ft': 12, 'IN': 1}
    }
    graphic_unit = graphic_unit_dropdown.value

    for param in params:
        for i in range(len(param)):
            if isinstance(param[i], str) and '*' in param[i]:
                # Split the string into value and unit
                parts = param[i].split('*')
                # Convert the value to float
                value = float(parts[0])
                # Get the conversion factor for the unit
                unit_str = parts[1]
                factor = unit_factors_new[graphic_unit][unit_str]
                # Check if the unit is squared
                if '**2' in param[i]:
                    factor = factor ** 2
                # Convert the value to the desired unit
                param[i] = value * factor

    with out:
        # See list to plot programmer window
        # programmer_output.value = str(params)
        out.clear_output(wait=True)
        xlabel_x = f'z [{graphic_unit}]'
        ylabel_x = f'y [{graphic_unit}]'
        zoom = float(zoom_dropdown.value)
        fibers = True if fiber_plot_dropdown.value == 'On' else False
        opsv1.plot_fiber_section(params, xlabel_x, ylabel_x, fibers=fibers, zoom=zoom)
        plt.axis('equal')
        plt.savefig(r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones/Fib_Sec_GUI01.png')
        plt.close()
        display(Image(filename=r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones/Fib_Sec_GUI01.png'))
    code_params_output.value = "Section created successfully"


# %%%% [03-02-02] SHOW_SECTION_UPDATE
# Function to show the section with the new patch or layer
def show_section_update(change=None):
    # Obtain the actual section
    try:
        params_old = eval(section_params_output.value)
        if not isinstance(params_old, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = section_params_output.value
        section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return

    # Add the element in base the parameters of the patch or layer
    aux_add_patch_layer()
    
    # Re-write the section with the patch layer original
    params_string = str(params_old).replace("[[", "[\n[")
    params_string = params_string.replace("], [", "],\n[")
    params_string = params_string.replace("]]", "]\n]")
    section_params_output.value = params_string


# %%%% [03-02-02] SHOW_MATERIAL_SECTION
# Function to show the material in the section
def show_material_section(change=None):
    try:
        params = eval(section_params_output.value)
        if not isinstance(params, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = section_params_output.value
        section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return

    # Remove unit annotations from the plot parameters
    unit_factors_new = {
        'm': {'m': 1, 'cm': 0.01, 'mm': 0.001, 'ft': 0.3048, 'IN': 0.0254},
        'cm': {'m': 100, 'cm': 1, 'mm': 0.1, 'ft': 30.48, 'IN': 2.54},
        'mm': {'m': 1000, 'cm': 10, 'mm': 1, 'ft': 304.8, 'IN': 25.4},
        'ft': {'m': 3.2808399, 'cm': 0.032808399, 'mm': 0.00328084, 'ft': 1, 'IN': 0.0833333},
        'IN': {'m': 39.370079, 'cm': 0.39370079, 'mm': 0.039370079, 'ft': 12, 'IN': 1}
    }
    graphic_unit = graphic_unit_dropdown.value

    for param in params:
        for i in range(len(param)):
            if isinstance(param[i], str) and '*' in param[i]:
                # Split the string into value and unit
                parts = param[i].split('*')
                # Convert the value to float
                value = float(parts[0])
                # Get the conversion factor for the unit
                unit_str = parts[1]
                factor = unit_factors_new[graphic_unit][unit_str]
                # Check if the unit is squared
                if '**2' in param[i]:
                    factor = factor ** 2
                # Convert the value to the desired unit
                param[i] = value * factor

    with out:
        # See list to plot programmer window
        # programmer_output.value = str(params)
        out.clear_output(wait=True)
        xlabel_x = f'z [{graphic_unit}]'
        ylabel_x = f'y [{graphic_unit}]'
        zoom = float(zoom_dropdown.value)
        fibers = True if fiber_plot_dropdown.value == 'On' else False
        opsv1.plot_fiber_section(params, xlabel_x, ylabel_x, mat_tag_color=True, fibers=fibers, zoom=zoom)
        plt.axis('equal')
        plt.savefig(r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones/Fib_Sec_GUI01.png')
        plt.close()
        display(Image(filename=r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones/Fib_Sec_GUI01.png'))
    code_params_output.value = "Section created successfully"


# %%%% [03-02-03] EDIT_PATCH_LAYER
# Function to edit patch or layer definition
def edit_patch_layer(change=None):
    # If the button is in the 'Edit' state, the function will select a patch or layer to edit
    # from the edit_patch_layer_dropdown. And show the parameters to edit the patch or layer
    # in base of the values from the edit_patch_layer_dropdown.
    if edit_patch_layer_button.description == 'Edit':
        # Verify if there are selected a patch or layer to edit
        if edit_patch_layer_dropdown.value == '-':
            code_params_output.value = "Select a patch or layer to edit"
            return 
        
        # See patch or layer parameters
        update_input_widgets()
        
        # Change the button description and color
        add_patch_layer_button.description = 'Save'
        add_patch_layer_button.style.button_color = 'green'
        
        # Disable the other buttons
        add_section_button.disabled = True
        refresh_button.disabled = True
        video_button.disabled = True
        code_button.disabled = True
        cover_button.disabled = True
        replicate_button.disabled = True
        CP_button.disabled = True
        material_button.disabled = True
        center_button.disabled = True
        edit_patch_layer_button.disabled = True
        edit_patch_layer_dropdown.disabled = True
        
        # Enable the button to cancel the definition
        cancel_patch_layer_button.disabled = False
        # Modify the description of the cancel button and the color
        cancel_patch_layer_button.description = 'Delete'
        cancel_patch_layer_button.style.button_color = 'red'
        
        # Enable the button to show and hide the new patch or layer
        edit_patch_layer_button.disabled = False
        # Modify the description of the edit button
        edit_patch_layer_button.description = 'Hide'
        edit_patch_layer_button.style.button_color = 'blue'
        
        # Enable the dropdowns to define the patch or layer
        patch_layer_type_dropdown.disabled = False
        element_type_dropdown.disabled = False
        unit_dropdown.disabled = False
        
        # Get the patch or layer to edit
        patch_layer_to_edit = edit_patch_layer_dropdown.value
        patch_layer_to_edit_recover = patch_layer_to_edit  # Save the patch or layer to edit to recover it later
        # Transform the string to a list
        patch_layer_to_edit = eval(patch_layer_to_edit)
        
        # Assign the values of the patch or layer to the dropdowns
        element_type_dropdown.value = patch_layer_to_edit[0]
        patch_layer_type_dropdown.value = patch_layer_to_edit[1]
        
        # Obtain the units of the patch or layer
        # If graphic_unit is '-', the unit is adimensional
        if graphic_unit_dropdown.value == '-':
            unit_dropdown.value = '-'
        else:
            parts = patch_layer_to_edit[6].split('*')
            if 'm' == parts[1]:
                unit_dropdown.value = 'm'
            elif 'cm' == parts[1]:
                unit_dropdown.value = 'cm'
            elif 'mm' == parts[1]:
                unit_dropdown.value = 'mm'
            elif 'ft' == parts[1]:
                unit_dropdown.value = 'ft'
            elif 'IN' == parts[1]:
                unit_dropdown.value = 'IN'
        
        # Delete the unit from the values of the patch or layer
        for term in patch_layer_to_edit:
            if isinstance(term, str) and '*' in term:
                parts = term.split('*')
                patch_layer_to_edit[patch_layer_to_edit.index(term)] = parts[0]
        
        # Assign the values of the patch or layer to the input widgets
        if element_type_dropdown.value == 'patch':
            if patch_layer_type_dropdown.value == 'rect':
                material_tag_input.value = int(patch_layer_to_edit[2])
                nFibY_input.value = int(patch_layer_to_edit[3])
                nFibZ_input.value = int(patch_layer_to_edit[4])
                y1_input.value = str(patch_layer_to_edit[5])
                z1_input.value = str(patch_layer_to_edit[6])
                y2_input.value = str(patch_layer_to_edit[7])
                z2_input.value = str(patch_layer_to_edit[8])
            elif patch_layer_type_dropdown.value == 'quad':
                material_tag_input.value = int(patch_layer_to_edit[2])
                numSubdivIJ_input.value = int(patch_layer_to_edit[3])
                numSubdivJK_input.value = int(patch_layer_to_edit[4])
                yI_input.value = str(patch_layer_to_edit[5])
                zI_input.value = str(patch_layer_to_edit[6])
                yJ_input.value = str(patch_layer_to_edit[7])
                zJ_input.value = str(patch_layer_to_edit[8])
                yK_input.value = str(patch_layer_to_edit[9])
                zK_input.value = str(patch_layer_to_edit[10])
                yL_input.value = str(patch_layer_to_edit[11])
                zL_input.value = str(patch_layer_to_edit[12])
            elif patch_layer_type_dropdown.value == 'circ':
                material_tag_input.value = int(patch_layer_to_edit[2])
                numSubdivCirc_input.value = int(patch_layer_to_edit[3])
                numSubdivRad_input.value = int(patch_layer_to_edit[4])
                yc_input.value = str(patch_layer_to_edit[5])
                zc_input.value = str(patch_layer_to_edit[6])
                r_ini_input.value = str(patch_layer_to_edit[7])
                r_end_input.value = str(patch_layer_to_edit[8])
                ang_ini_input.value = str(patch_layer_to_edit[9])
                ang_end_input.value = str(patch_layer_to_edit[10])
        elif element_type_dropdown.value == 'layer':
            if patch_layer_type_dropdown.value == 'straight':
                material_tag_input.value = int(patch_layer_to_edit[2])
                numFiber_input.value = int(patch_layer_to_edit[3])
                areaFiber_input.value = str(patch_layer_to_edit[4])
                y1_input.value = str(patch_layer_to_edit[5])
                z1_input.value = str(patch_layer_to_edit[6])
                y2_input.value = str(patch_layer_to_edit[7])
                z2_input.value = str(patch_layer_to_edit[8])
            elif patch_layer_type_dropdown.value == 'circ':
                material_tag_input.value = int(patch_layer_to_edit[2])
                numFiber_input.value = int(patch_layer_to_edit[3])
                areaFiber_input.value = str(patch_layer_to_edit[4])
                yc_input.value = str(patch_layer_to_edit[5])
                zc_input.value = str(patch_layer_to_edit[6])
                radius_input.value = str(patch_layer_to_edit[7])
                ang_ini_input.value = str(patch_layer_to_edit[8])
                ang_end_input.value = str(patch_layer_to_edit[9])
        
        # Show the actual section with the new patch or layer
        show_section_update()

        # Show the actual element to edit (It's useful to debug the code)
        # edit_patch_layer_dropdown.value = patch_layer_to_edit_recover
        
        # Delete the patch or layer to edit from the section
        try:
            params = eval(section_params_output.value)
            if not isinstance(params, list):
                raise ValueError("Invalid list format")
        except Exception as e:
            actual = section_params_output.value
            section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
            return

        for item in params:
            if str(item) == patch_layer_to_edit_recover:
                params.remove(item)
                break
            
        params_string = str(params).replace("[[", "[\n[")
        params_string = params_string.replace("], [", "],\n[")
        params_string = params_string.replace("]]", "]\n]")
        section_params_output.value = params_string
        
        # Update the dropdown to edit the patch or layer
        update_edit_patch_layer_options()
        
        # Disable the dropdown to edit the patch or layer
        edit_patch_layer_dropdown.disabled = True
        
        # Message to the user
        code_params_output.value = "Edit the patch or layer parameters"
    
    # If the button is in the 'Hide' state, the function will hide the patch or layer actually
    # in definition.
    elif edit_patch_layer_button.description == 'Hide':
        # Only show the actual section without the new patch or layer
        show_section()
        
        # Change the button description and color
        edit_patch_layer_button.description = 'Show'
        edit_patch_layer_button.style.button_color = 'magenta'
        
        # Disable the buttons to save and cancel the patch or layer definition
        add_patch_layer_button.disabled = True
        cancel_patch_layer_button.disabled = True
        
        # Disable the dropdowns to define the patch or layer
        patch_layer_type_dropdown.disabled = True
        element_type_dropdown.disabled = True
        unit_dropdown.disabled = True
        
        # Disable the input widgets to define the patch or layer
        model_widgets.children = []
        
    
    # If the button is in the 'Show' state, the function will show the patch or layer actually
    # in definition.
    elif edit_patch_layer_button.description == 'Show':
        # Show the actual section with the new patch or layer
        show_section_update()
        
        # Change the button description and color
        edit_patch_layer_button.description = 'Hide'
        edit_patch_layer_button.style.button_color = 'blue'
        
        # Enable the buttons to save and cancel the patch or layer definition
        add_patch_layer_button.disabled = False
        cancel_patch_layer_button.disabled = False
        
        # Enable the dropdowns to define the patch or layer
        patch_layer_type_dropdown.disabled = False
        element_type_dropdown.disabled = False
        unit_dropdown.disabled = False
        
        # Enable the input widgets to define the patch or layer
        update_input_widgets()


# %%%% [03-02-03] CANCEL_PATCH_LAYER
# Function to cancel patch or layer definition
def cancel_patch_layer(change=None):
    # If the button is in the 'Delete' state, the function will cancel the patch or layer definition.
    if cancel_patch_layer_button.description == 'Delete':
        # Hide the patch or layer parameters
        model_widgets.children = []
        
        # Change the button description and color
        add_patch_layer_button.description = 'Define'
        add_patch_layer_button.style.button_color = None
        
        # Enable the other buttons
        add_section_button.disabled = False
        refresh_button.disabled = False
        video_button.disabled = False
        code_button.disabled = False
        cover_button.disabled = False
        replicate_button.disabled = False
        CP_button.disabled = False
        material_button.disabled = False
        center_button.disabled = False
        edit_patch_layer_button.disabled = False
        edit_patch_layer_dropdown.disabled = False
        
        # Modify the description of the edit button
        edit_patch_layer_button.description = 'Edit'
        
        # Disable the button to cancel the definition
        cancel_patch_layer_button.disabled = False
        # Modify the description of the cancel button and the color
        cancel_patch_layer_button.description = 'Copy'
        cancel_patch_layer_button.style.button_color = None
        
        # Disable the button to show and hide the new patch or layer
        edit_patch_layer_button.disabled = False
        # Modify the description of the edit button
        edit_patch_layer_button.description = 'Edit'
        edit_patch_layer_button.style.button_color = None
        
        # Disable the dropdowns to define the patch or layer
        patch_layer_type_dropdown.disabled = True
        element_type_dropdown.disabled = True
        unit_dropdown.disabled = True   
        
        # Clear output
        with out:
            out.clear_output()
            show_section()
        
        # Message to the user
        code_params_output.value = "Patch or layer definition canceled"
    
    
    # If the button is in the 'Copy' state, the function will copy the patch or layer definition.
    elif cancel_patch_layer_button.description == 'Copy':
        # See patch or layer parameters
        update_input_widgets()
        
        # Change the button description and color
        add_patch_layer_button.description = 'Save'
        add_patch_layer_button.style.button_color = 'green'
        
        # Disable the other buttons
        add_section_button.disabled = True
        refresh_button.disabled = True
        video_button.disabled = True
        code_button.disabled = True
        cover_button.disabled = True
        replicate_button.disabled = True
        CP_button.disabled = True
        material_button.disabled = True
        center_button.disabled = True
        edit_patch_layer_button.disabled = True
        edit_patch_layer_dropdown.disabled = True
        
        # Enable the button to cancel the definition
        cancel_patch_layer_button.disabled = False
        # Modify the description of the cancel button and the color
        cancel_patch_layer_button.description = 'Delete'
        cancel_patch_layer_button.style.button_color = 'red'
        
        # Enable the button to show and hide the new patch or layer
        edit_patch_layer_button.disabled = False
        # Modify the description of the edit button
        edit_patch_layer_button.description = 'Hide'
        edit_patch_layer_button.style.button_color = 'blue'
        
        # Enable the dropdowns to define the patch or layer
        patch_layer_type_dropdown.disabled = False
        element_type_dropdown.disabled = False
        unit_dropdown.disabled = False
        
        # Get the patch or layer to edit
        patch_layer_to_edit = edit_patch_layer_dropdown.value
        patch_layer_to_edit_recover = patch_layer_to_edit  # Save the patch or layer to edit to recover it later
        # Transform the string to a list
        patch_layer_to_edit = eval(patch_layer_to_edit)
        
        # Assign the values of the patch or layer to the dropdowns
        element_type_dropdown.value = patch_layer_to_edit[0]
        patch_layer_type_dropdown.value = patch_layer_to_edit[1]
        
        # Obtain the units of the patch or layer
        # If graphic_unit is '-', the unit is adimensional
        if graphic_unit_dropdown.value == '-':
            unit_dropdown.value = '-'
        else:
            parts = patch_layer_to_edit[6].split('*')
            if 'm' == parts[1]:
                unit_dropdown.value = 'm'
            elif 'cm' == parts[1]:
                unit_dropdown.value = 'cm'
            elif 'mm' == parts[1]:
                unit_dropdown.value = 'mm'
            elif 'ft' == parts[1]:
                unit_dropdown.value = 'ft'
            elif 'IN' == parts[1]:
                unit_dropdown.value = 'IN'
        
        # Delete the unit from the values of the patch or layer
        for term in patch_layer_to_edit:
            if isinstance(term, str) and '*' in term:
                parts = term.split('*')
                patch_layer_to_edit[patch_layer_to_edit.index(term)] = parts[0]
        
        # Assign the values of the patch or layer to the input widgets
        if element_type_dropdown.value == 'patch':
            if patch_layer_type_dropdown.value == 'rect':
                material_tag_input.value = int(patch_layer_to_edit[2])
                nFibY_input.value = int(patch_layer_to_edit[3])
                nFibZ_input.value = int(patch_layer_to_edit[4])
                y1_input.value = str(patch_layer_to_edit[5])
                z1_input.value = str(patch_layer_to_edit[6])
                y2_input.value = str(patch_layer_to_edit[7])
                z2_input.value = str(patch_layer_to_edit[8])
            elif patch_layer_type_dropdown.value == 'quad':
                material_tag_input.value = int(patch_layer_to_edit[2])
                numSubdivIJ_input.value = int(patch_layer_to_edit[3])
                numSubdivJK_input.value = int(patch_layer_to_edit[4])
                yI_input.value = str(patch_layer_to_edit[5])
                zI_input.value = str(patch_layer_to_edit[6])
                yJ_input.value = str(patch_layer_to_edit[7])
                zJ_input.value = str(patch_layer_to_edit[8])
                yK_input.value = str(patch_layer_to_edit[9])
                zK_input.value = str(patch_layer_to_edit[10])
                yL_input.value = str(patch_layer_to_edit[11])
                zL_input.value = str(patch_layer_to_edit[12])
            elif patch_layer_type_dropdown.value == 'circ':
                material_tag_input.value = int(patch_layer_to_edit[2])
                numSubdivCirc_input.value = int(patch_layer_to_edit[3])
                numSubdivRad_input.value = int(patch_layer_to_edit[4])
                yc_input.value = str(patch_layer_to_edit[5])
                zc_input.value = str(patch_layer_to_edit[6])
                r_ini_input.value = str(patch_layer_to_edit[7])
                r_end_input.value = str(patch_layer_to_edit[8])
                ang_ini_input.value = str(patch_layer_to_edit[9])
                ang_end_input.value = str(patch_layer_to_edit[10])
        elif element_type_dropdown.value == 'layer':
            if patch_layer_type_dropdown.value == 'straight':
                material_tag_input.value = int(patch_layer_to_edit[2])
                numFiber_input.value = int(patch_layer_to_edit[3])
                areaFiber_input.value = str(patch_layer_to_edit[4])
                y1_input.value = str(patch_layer_to_edit[5])
                z1_input.value = str(patch_layer_to_edit[6])
                y2_input.value = str(patch_layer_to_edit[7])
                z2_input.value = str(patch_layer_to_edit[8])
            elif patch_layer_type_dropdown.value == 'circ':
                material_tag_input.value = int(patch_layer_to_edit[2])
                numFiber_input.value = int(patch_layer_to_edit[3])
                areaFiber_input.value = str(patch_layer_to_edit[4])
                yc_input.value = str(patch_layer_to_edit[5])
                zc_input.value = str(patch_layer_to_edit[6])
                radius_input.value = str(patch_layer_to_edit[7])
                ang_ini_input.value = str(patch_layer_to_edit[8])
                ang_end_input.value = str(patch_layer_to_edit[9])
        
        # Show the actual section with the new patch or layer
        show_section_update()

        # Show the actual element to edit (It's useful to debug the code)
        # edit_patch_layer_dropdown.value = patch_layer_to_edit_recover
        
        # Disable the dropdown to edit the patch or layer
        edit_patch_layer_dropdown.disabled = True
        
        # Message to the user
        code_params_output.value = "Edit the patch or layer parameters"
        

# %%%% [03-02-03] REPLICATE
# Function to save the replicate definition
def save_replicate(change=None):
    # Copy the value in the cover parameters output into the section parameters output
    section_params_output.value = replicate_params_output.value

    # Hide the cover parameters
    model_widgets.children = []
    
    # Enable the button
    replicate_button.disabled = False

    # Enable the other buttons
    cover_button.disabled = False
    add_section_button.disabled = False
    add_patch_layer_button.disabled = False
    refresh_button.disabled = False
    video_button.disabled = False
    code_button.disabled = False
    CP_button.disabled = False
    material_button.disabled = False
    center_button.disabled = False
    edit_patch_layer_button.disabled = False
    edit_patch_layer_dropdown.disabled = False
    cancel_patch_layer_button.disabled = False
    section_params_output.disabled = False
    
    # Show the section
    with out:
        out.clear_output()
        show_section()
    
    # Update button description
    save_replicate_button.description = '-'


# Function to cancel the replicate definition
def delete_replicate(change=None):
    # Hide the cover parameters
    model_widgets.children = []
    
    # Enable the button
    replicate_button.disabled = False
    
    # Enable the other buttons
    cover_button.disabled = False
    add_section_button.disabled = False
    add_patch_layer_button.disabled = False
    refresh_button.disabled = False
    video_button.disabled = False
    code_button.disabled = False
    CP_button.disabled = False
    material_button.disabled = False
    center_button.disabled = False
    edit_patch_layer_button.disabled = False
    edit_patch_layer_dropdown.disabled = False
    cancel_patch_layer_button.disabled = False
    section_params_output.disabled = False
    
    # Show the section
    with out:
        out.clear_output()
        show_section()
    
    # Update button description
    save_replicate_button.description = '-'


# Function to show the replicate instructions
def replicate_instructions(change=None):
    code_params_output.value =  "Define the parameters of the section to replicate."

# Function to show the section created
def show_section_replicate(change=None):
    try:
        params = eval(replicate_params_output.value)
        if not isinstance(params, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = replicate_params_output.value
        replicate_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return
    
    # Remove unit annotations from the plot parameters
    unit_factors_new = {
        'm': {'m': 1, 'cm': 0.01, 'mm': 0.001, 'ft': 0.3048, 'IN': 0.0254},
        'cm': {'m': 100, 'cm': 1, 'mm': 0.1, 'ft': 30.48, 'IN': 2.54},
        'mm': {'m': 1000, 'cm': 10, 'mm': 1, 'ft': 304.8, 'IN': 25.4},
        'ft': {'m': 3.2808399, 'cm': 0.032808399, 'mm': 0.00328084, 'ft': 1, 'IN': 0.0833333},
        'IN': {'m': 39.370079, 'cm': 0.39370079, 'mm': 0.039370079, 'ft': 12, 'IN': 1}
    }
    graphic_unit = graphic_unit_dropdown.value
    
    for param in params:
        for i in range(len(param)):
            if isinstance(param[i], str) and '*' in param[i]:
                # Split the string into value and unit
                parts = param[i].split('*')
                # Convert the value to float
                value = float(parts[0])
                # Get the conversion factor for the unit
                unit_str = parts[1]
                factor = unit_factors_new[graphic_unit][unit_str]
                # Check if the unit is squared
                if '**2' in param[i]:
                    factor = factor ** 2
                # Convert the value to the desired unit
                param[i] = value * factor
                
    with out:
        # See list to plot programmer window
        # programmer_output.value = str(params)
        out.clear_output(wait=True)
        xlabel_x = f'z [{graphic_unit}]'
        ylabel_x = f'y [{graphic_unit}]'
        zoom = float(zoom_dropdown.value)
        fibers = True if fiber_plot_dropdown.value == 'On' else False
        opsv1.plot_fiber_section(params, xlabel_x, ylabel_x, fibers=fibers, zoom=zoom)
        plt.axis('equal')
        plt.savefig(r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones/Replicate_Fib_Sec_GUI01.png')
        plt.close()
        display(Image(filename=r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones/Replicate_Fib_Sec_GUI01.png'))
    code_params_output.value = "Section created successfully"


# Function auxiliar to modify the fiber section with replicate element
def fiber_section_replicate(change=None):
    # This function is similar to fiber_section cover.
    # Get displacements parameters
    dis_y_value = float(dis_y.value)
    dis_z_value = float(dis_z.value)
    num_copies_value = int(num_copies.value)
    
    # Get the patch or layer to edit
    patch_layer_original = edit_patch_layer_dropdown.value
    patch_layer_original_recover = patch_layer_original  # Save the patch or layer to edit to recover it later
    # Transform the string to a list
    patch_layer_original = eval(patch_layer_original)
    
    # Obtain the units of the patch or layer
    if graphic_unit_dropdown.value == '-':
        unit = '-'
    else:
        parts = patch_layer_original[6].split('*')
        unit = parts[1]
    
    # Function to add unit to the section definition.
    def unit_patch_layer(value, unit_x, coef):
        if unit_x == "-":
            return value
        else:
            if coef == 1:
                return str(value) + f"*{unit_x}"
            if coef >= 2:
                return str(value) + f"*{unit_x}**{coef}"
    
    # Delete the unit from the values of the patch or layer to operate
    for term in patch_layer_original:
        if isinstance(term, str) and '*' in term:
            parts = term.split('*')
            patch_layer_original[patch_layer_original.index(term)] = parts[0]
    
    # Add the replicate element to the section
    patch_layer_type = patch_layer_original[0]
    type_element = patch_layer_original[1]
    
    if patch_layer_type == 'patch' and type_element == 'rect':
        matTag = int(patch_layer_original[2])
        nFibY = int(patch_layer_original[3])
        nFibZ = int(patch_layer_original[4])
        y0 = float(patch_layer_original[5])
        z0 = float(patch_layer_original[6])
        y1 = float(patch_layer_original[7])
        z1 = float(patch_layer_original[8])
        
        # Original section without replicate
        patch_replicate = [['patch', 'rect', matTag, nFibY, nFibZ, 
                            unit_patch_layer(y0, unit, 1), 
                            unit_patch_layer(z0, unit, 1),
                            unit_patch_layer(y1, unit, 1),
                            unit_patch_layer(z1, unit, 1)]]
        
        # Calculate the new patch
        y0_new, z0_new, y1_new, z1_new = y0, z0, y1, z1
        for i in range(num_copies_value):
            i += 1
            y0_new = y0 + i * dis_y_value
            z0_new = z0 + i * dis_z_value
            y1_new = y1 + i * dis_y_value
            z1_new = z1 + i * dis_z_value
            
            # Add the new patch to the section
            patch_replicate.append(['patch', 'rect', matTag, nFibY, nFibZ,                                     
                                    unit_patch_layer(y0_new, unit, 1),
                                    unit_patch_layer(z0_new, unit, 1),
                                    unit_patch_layer(y1_new, unit, 1),
                                    unit_patch_layer(z1_new, unit, 1)])
    
    elif patch_layer_type == 'patch' and type_element == 'quad':
        matTag = int(patch_layer_original[2])
        numSubdivIJ = int(patch_layer_original[3])
        numSubdivJK = int(patch_layer_original[4])
        yI = float(patch_layer_original[5])
        zI = float(patch_layer_original[6])
        yJ = float(patch_layer_original[7])
        zJ = float(patch_layer_original[8])
        yK = float(patch_layer_original[9])
        zK = float(patch_layer_original[10])
        yL = float(patch_layer_original[11])
        zL = float(patch_layer_original[12])
        
        # Original section without replicate
        patch_replicate = [['patch', 'quad', matTag, numSubdivIJ, numSubdivJK,
                            unit_patch_layer(yI, unit, 1),
                            unit_patch_layer(zI, unit, 1),
                            unit_patch_layer(yJ, unit, 1),
                            unit_patch_layer(zJ, unit, 1),
                            unit_patch_layer(yK, unit, 1),
                            unit_patch_layer(zK, unit, 1),
                            unit_patch_layer(yL, unit, 1),
                            unit_patch_layer(zL, unit, 1)]]
        
        # Calculate the new patch
        yI_new, zI_new, yJ_new, zJ_new, yK_new, zK_new, yL_new, zL_new = yI, zI, yJ, zJ, yK, zK, yL, zL
        for i in range(num_copies_value):
            i += 1
            yI_new = yI + i * dis_y_value
            zI_new = zI + i * dis_z_value
            yJ_new = yJ + i * dis_y_value
            zJ_new = zJ + i * dis_z_value
            yK_new = yK + i * dis_y_value
            zK_new = zK + i * dis_z_value
            yL_new = yL + i * dis_y_value
            zL_new = zL + i * dis_z_value
            
            # Add the new patch to the section
            patch_replicate.append(['patch', 'quad', matTag, numSubdivIJ, numSubdivJK,
                                    unit_patch_layer(yI_new, unit, 1),
                                    unit_patch_layer(zI_new, unit, 1),
                                    unit_patch_layer(yJ_new, unit, 1),
                                    unit_patch_layer(zJ_new, unit, 1),
                                    unit_patch_layer(yK_new, unit, 1),
                                    unit_patch_layer(zK_new, unit, 1),
                                    unit_patch_layer(yL_new, unit, 1),
                                    unit_patch_layer(zL_new, unit, 1)])
    
    elif patch_layer_type == 'patch' and type_element == 'circ':
        matTag = int(patch_layer_original[2])
        numSubdivCirc = int(patch_layer_original[3])
        numSubdivRad = int(patch_layer_original[4])
        yc = float(patch_layer_original[5])
        zc = float(patch_layer_original[6])
        r_ini = float(patch_layer_original[7])
        r_end = float(patch_layer_original[8])
        ang_ini = float(patch_layer_original[9])
        ang_end = float(patch_layer_original[10])
        
        # Original section without replicate
        patch_replicate = [['patch', 'circ', matTag, numSubdivCirc, numSubdivRad,
                            unit_patch_layer(yc, unit, 1),
                            unit_patch_layer(zc, unit, 1),
                            unit_patch_layer(r_ini, unit, 1),
                            unit_patch_layer(r_end, unit, 1),
                            unit_patch_layer(ang_ini, unit, 1),
                            unit_patch_layer(ang_end, unit, 1)]]
        
        # Calculate the new patch
        yc_new, zc_new, r_ini_new, r_end_new, ang_ini_new, ang_end_new = yc, zc, r_ini, r_end, ang_ini, ang_end
        for i in range(num_copies_value):
            i += 1
            yc_new = yc + i * dis_y_value
            zc_new = zc + i * dis_z_value
            r_ini_new = r_ini
            r_end_new = r_end
            ang_ini_new = ang_ini
            ang_end_new = ang_end
            
            # Add the new patch to the section
            patch_replicate.append(['patch', 'circ', matTag, numSubdivCirc, numSubdivRad,
                                    unit_patch_layer(yc_new, unit, 1),
                                    unit_patch_layer(zc_new, unit, 1),
                                    unit_patch_layer(r_ini_new, unit, 1),
                                    unit_patch_layer(r_end_new, unit, 1),
                                    unit_patch_layer(ang_ini_new, unit, 1),
                                    unit_patch_layer(ang_end_new, unit, 1)])
    
    elif patch_layer_type == 'layer' and type_element == 'straight':
        matTag = int(patch_layer_original[2])
        numFiber = int(patch_layer_original[3])
        areaFiber = float(patch_layer_original[4])
        y1 = float(patch_layer_original[5])
        z1 = float(patch_layer_original[6])
        y2 = float(patch_layer_original[7])
        z2 = float(patch_layer_original[8])
        
        # Original section without replicate
        patch_replicate = [['layer', 'straight', matTag, numFiber, 
                            unit_patch_layer(areaFiber, unit, 2),
                            unit_patch_layer(y1, unit, 1),
                            unit_patch_layer(z1, unit, 1),
                            unit_patch_layer(y2, unit, 1),
                            unit_patch_layer(z2, unit, 1)]]
        
        # Calculate the new patch
        y1_new, z1_new, y2_new, z2_new = y1, z1, y2, z2
        for i in range(num_copies_value):
            i += 1
            y1_new = y1 + i * dis_y_value
            z1_new = z1 + i * dis_z_value
            y2_new = y2 + i * dis_y_value
            z2_new = z2 + i * dis_z_value
            
            # Add the new patch to the section
            patch_replicate.append(['layer', 'straight', matTag, numFiber, 
                                    unit_patch_layer(areaFiber, unit, 2),
                                    unit_patch_layer(y1_new, unit, 1),
                                    unit_patch_layer(z1_new, unit, 1),
                                    unit_patch_layer(y2_new, unit, 1),
                                    unit_patch_layer(z2_new, unit, 1)])
    
    elif patch_layer_type == 'layer' and type_element == 'circ':
        matTag = int(patch_layer_original[2])
        numFiber = int(patch_layer_original[3])
        areaFiber = float(patch_layer_original[4])
        yc = float(patch_layer_original[5])
        zc = float(patch_layer_original[6])
        radius = float(patch_layer_original[7])
        ang_ini = float(patch_layer_original[8])
        ang_end = float(patch_layer_original[9])
        
        # Original section without replicate
        patch_replicate = [['layer', 'circ', matTag, numFiber,
                            unit_patch_layer(areaFiber, unit, 2),
                            unit_patch_layer(yc, unit, 1),
                            unit_patch_layer(zc, unit, 1),
                            unit_patch_layer(radius, unit, 1),
                            unit_patch_layer(ang_ini, unit, 1),
                            unit_patch_layer(ang_end, unit, 1)]]
        
        # Calculate the new patch
        yc_new, zc_new = yc, zc
        for i in range(num_copies_value):
            i += 1
            yc_new = yc + i * dis_y_value
            zc_new = zc + i * dis_z_value
            
            # Add the new patch to the section
            patch_replicate.append(['layer', 'circ', matTag, numFiber,
                                    unit_patch_layer(areaFiber, unit, 2),
                                    unit_patch_layer(yc_new, unit, 1),
                                    unit_patch_layer(zc_new, unit, 1),
                                    unit_patch_layer(radius, unit, 1),
                                    unit_patch_layer(ang_ini, unit, 1),
                                    unit_patch_layer(ang_end, unit, 1)])
    
    else:
        code_params_output.value = "Error: The replicate element is not a rectangular patch"
        return
    
    # Delete the patch or layer to edit from the section
    try:
        params = eval(section_params_output.value)
        if not isinstance(params, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = section_params_output.value
        section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return

    for item in params:
        if str(item) == patch_layer_original_recover:
            params.remove(item)
            break
    
    # Add the replicate element to the section
    params = params + patch_replicate
    
    # Show the section with the replicate element
    params_string = str(params).replace("[[", "[\n[")
    params_string = params_string.replace("], [", "],\n[")
    params_string = params_string.replace("]]", "]\n]")
    
    replicate_params_output.value = params_string
    
    # Show the section with replicate element
    show_section_replicate()


# Function to add replicate definition
def replicate(change=None):
    # Verify that the element selected is a element
    selected_patch_layer = edit_patch_layer_dropdown.value
    if selected_patch_layer == '-':
        code_params_output.value = "Error: Select a rect patch to replicate."
        return
    
    # Disable the button
    replicate_button.disabled = True
    
    # Disable the other buttons
    cover_button.disabled = True
    add_section_button.disabled = True
    add_patch_layer_button.disabled = True
    refresh_button.disabled = True
    video_button.disabled = True
    code_button.disabled = True
    CP_button.disabled = True
    material_button.disabled = True
    center_button.disabled = True
    edit_patch_layer_button.disabled = True
    edit_patch_layer_dropdown.disabled = True
    cancel_patch_layer_button.disabled = True
    section_params_output.disabled = True
    
    # Update button description
    save_replicate_button.description = 'Save'
    
    # Show widgets of interest
    button_box_cover = widgets.HBox([save_replicate_button, cancel_replicate_button])
    text_box_repli_1 = widgets.VBox([num_copies], layout=widgets.Layout(width='100px'))
    text_box_repli_2 = widgets.VBox([dis_y, dis_z], layout=widgets.Layout(width='100px'))
    text_box_repli = widgets.HBox([text_box_repli_1, text_box_repli_2])
    text_replicate_out = widgets.HTML(value="Section with Replicates:", layout=widgets.Layout(margin="9px 0 0 2px"))
    text_replicate_out.style.font_size = '14px'
    model_widgets.children = [replicate_instructions_button, text_box_repli,
        button_box_cover, text_replicate_out, replicate_params_output]
    
    # Calculate the section with the replicate element and show it
    fiber_section_replicate()


# %%%% [03-02-03] COVER 
# Function to save the cover definition
def save_cover(change=None):
    # Copy the value in the cover parameters output into the section parameters output
    section_params_output.value = cover_params_output.value

    # Hide the cover parameters
    model_widgets.children = []
    
    # Enable the button
    cover_button.disabled = False
    
    # Enable the other buttons
    replicate_button.disabled = False
    add_section_button.disabled = False
    add_patch_layer_button.disabled = False
    refresh_button.disabled = False
    video_button.disabled = False
    code_button.disabled = False
    CP_button.disabled = False
    material_button.disabled = False
    center_button.disabled = False
    edit_patch_layer_button.disabled = False
    edit_patch_layer_dropdown.disabled = False
    cancel_patch_layer_button.disabled = False
    section_params_output.disabled = False
    
    # Show the section
    with out:
        out.clear_output()
        show_section()

    # Update button description
    save_cover_button.description = '-'


# Function to cancel the cover definition
def delete_cover(change=None):
    # Hide the cover parameters
    model_widgets.children = []
    
    # Enable the button
    cover_button.disabled = False
    
    # Enable the other buttons
    replicate_button.disabled = False
    add_section_button.disabled = False
    add_patch_layer_button.disabled = False
    refresh_button.disabled = False
    video_button.disabled = False
    code_button.disabled = False
    CP_button.disabled = False
    material_button.disabled = False
    center_button.disabled = False
    edit_patch_layer_button.disabled = False
    edit_patch_layer_dropdown.disabled = False
    cancel_patch_layer_button.disabled = False
    section_params_output.disabled = False
    
    # Show the section
    with out:
        out.clear_output()
        show_section()
    
    # Update button description
    save_cover_button.description = '-'


# Function to show the cover instructions
def cover_instructions(change=None):
    code_params_output.value = "Define the cover parameters"


# Function to show the section created
def show_section_cover(change=None):
    try:
        params = eval(cover_params_output.value)
        if not isinstance(params, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = cover_params_output.value
        cover_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return

    # Remove unit annotations from the plot parameters
    unit_factors_new = {
        'm': {'m': 1, 'cm': 0.01, 'mm': 0.001, 'ft': 0.3048, 'IN': 0.0254},
        'cm': {'m': 100, 'cm': 1, 'mm': 0.1, 'ft': 30.48, 'IN': 2.54},
        'mm': {'m': 1000, 'cm': 10, 'mm': 1, 'ft': 304.8, 'IN': 25.4},
        'ft': {'m': 3.2808399, 'cm': 0.032808399, 'mm': 0.00328084, 'ft': 1, 'IN': 0.0833333},
        'IN': {'m': 39.370079, 'cm': 0.39370079, 'mm': 0.039370079, 'ft': 12, 'IN': 1}
    }
    graphic_unit = graphic_unit_dropdown.value

    for param in params:
        for i in range(len(param)):
            if isinstance(param[i], str) and '*' in param[i]:
                # Split the string into value and unit
                parts = param[i].split('*')
                # Convert the value to float
                value = float(parts[0])
                # Get the conversion factor for the unit
                unit_str = parts[1]
                factor = unit_factors_new[graphic_unit][unit_str]
                # Check if the unit is squared
                if '**2' in param[i]:
                    factor = factor ** 2
                # Convert the value to the desired unit
                param[i] = value * factor

    with out:
        # See list to plot programmer window
        # programmer_output.value = str(params)
        out.clear_output(wait=True)
        xlabel_x = f'z [{graphic_unit}]'
        ylabel_x = f'y [{graphic_unit}]'
        zoom = float(zoom_dropdown.value)
        fibers = True if fiber_plot_dropdown.value == 'On' else False
        opsv1.plot_fiber_section(params, xlabel_x, ylabel_x, fibers=fibers, zoom=zoom)
        plt.axis('equal')
        plt.savefig(r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones/Cover_Fib_Sec_GUI01.png')
        plt.close()
        display(Image(filename=r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones/Cover_Fib_Sec_GUI01.png'))
    code_params_output.value = "Section created successfully"


# Function auxiliar to modify the fiber section with cover
def fiber_section_cover(change=None):
    
    # Get the patch to edit
    patch_original = edit_patch_layer_dropdown.value
    patch_original_recover = patch_original  # Save the patch or layer to edit to recover it later
    # Transform the string to a list
    patch_original = eval(patch_original)
    
    # Obtain the units of the patch or layer
    if graphic_unit_dropdown.value == '-':
        unit = '-'
    else:
        parts = patch_original[6].split('*')
        unit = parts[1]
    
    # Function to add unit to the section definition.
    def unit_patch_layer(value, unit_x, coef):
        if unit_x == "-":
            return value
        else:
            if coef == 1:
                return str(value) + f"*{unit_x}"
            if coef >= 2:
                return str(value) + f"*{unit_x}**{coef}"
    
    # Delete the unit from the values of the patch or layer to operate
    for term in patch_original:
        if isinstance(term, str) and '*' in term:
            parts = term.split('*')
            patch_original[patch_original.index(term)] = parts[0]
    
    # Add cover to the patch rect
    patch_layer_type = patch_original[0]
    type_element = patch_original[1]
    
    if patch_layer_type == 'patch' and type_element == 'rect':
        # Get cover parameters
        cov_Left = float(cov_L.value)
        cov_Right = float(cov_R.value)
        cov_Up = float(cov_U.value)
        cov_Below = float(cov_B.value)
        
        # Get the original rect patch parameters
        matTag = int(patch_original[2])
        nFibY = int(patch_original[3])
        nFibZ = int(patch_original[4])
        y0 = float(patch_original[5])
        z0 = float(patch_original[6])
        y1 = float(patch_original[7])
        z1 = float(patch_original[8])
        
        # Modify the original rect patch
        patch_modificado = [['patch', 'rect', matTag, nFibY, nFibZ, 
                             unit_patch_layer(y0 + cov_Below, unit, 1), 
                             unit_patch_layer(z0 + cov_Left, unit, 1), 
                             unit_patch_layer(y1 - cov_Up, unit, 1), 
                             unit_patch_layer(z1 - cov_Right, unit, 1)]]

        # Add the cover to the rect patch
        # Left
        if cov_Left > 0:
            patch_modificado.append(['patch', 'rect', matTag+1, nFibY, 1, 
                                    unit_patch_layer(y0 + cov_Below, unit, 1), 
                                    unit_patch_layer(z0, unit, 1), 
                                    unit_patch_layer(y1 - cov_Up, unit, 1), 
                                    unit_patch_layer(z0 + cov_Left, unit, 1)])
        # Rigth
        if cov_Right > 0:
            patch_modificado.append(['patch', 'rect', matTag+1, nFibY, 1, 
                                    unit_patch_layer(y0 + cov_Below, unit, 1), 
                                    unit_patch_layer(z1 - cov_Right, unit, 1), 
                                    unit_patch_layer(y1 - cov_Up, unit, 1), 
                                    unit_patch_layer(z1, unit, 1)])
        # Below
        if cov_Below > 0:
            patch_modificado.append(['patch', 'rect', matTag+1, 1, nFibZ, 
                                    unit_patch_layer(y0, unit, 1), 
                                    unit_patch_layer(z0, unit, 1), 
                                    unit_patch_layer(y0 + cov_Below, unit, 1), 
                                    unit_patch_layer(z1, unit, 1)])
        # Up
        if cov_Up > 0:
            patch_modificado.append(['patch', 'rect', matTag+1, 1, nFibZ, 
                                    unit_patch_layer(y1 - cov_Up, unit, 1), 
                                    unit_patch_layer(y0, unit, 1), 
                                    unit_patch_layer(y1, unit, 1), 
                                    unit_patch_layer(z1, unit, 1)])


    elif patch_layer_type == 'patch' and type_element == 'quad':
        # Get cover parameters
        cov_Left = float(cov_L.value)
        cov_Right = float(cov_R.value)
        cov_Up = float(cov_U.value)
        cov_Below = float(cov_B.value)
        
        # Get the original quad patch parameters
        matTag = int(patch_original[2])
        numSubdivIJ = int(patch_original[3])
        numSubdivJK = int(patch_original[4])
        yI = float(patch_original[5])
        zI = float(patch_original[6])
        yJ = float(patch_original[7])
        zJ = float(patch_original[8])
        yK = float(patch_original[9])
        zK = float(patch_original[10])
        yL = float(patch_original[11])
        zL = float(patch_original[12])
        
        # Calculate the points of cover between the original points.
        # The quad element is defined by the point I, J, K, L draw
        # in the counter-clockwise direction.
        # The left cover is between the points I and J.
        # The up cover is between the points J and K.
        # The right cover is between the points K and L.
        # The below cover is between the points L and I.
        # The coordinates of the points are (y, z).
        # Function to calculate the distance between two points.
        def distance_between_points(y1, z1, y2, z2):
            return ((y2 - y1)**2 + (z2 - z1)**2)**0.5
        # Calculate the coordinate of a point between two points, and a distance dist to the first point.
        def point_between_points(y1, z1, y2, z2, dist):
            total_dist = distance_between_points(y1, z1, y2, z2)
            y = y1 + (y2 - y1) * dist / total_dist
            z = z1 + (z2 - z1) * dist / total_dist
            return y, z
        # Calculate the coordinates of the points of the cover.
        # Points in the IJ side
        dist_IJ = distance_between_points(yI, zI, yJ, zJ)
        yIJ_U, zIJ_U = point_between_points(yI, zI, yJ, zJ, dist_IJ-cov_Up)
        yIJ_B, zIJ_B = point_between_points(yI, zI, yJ, zJ, cov_Below)
        # Points in the LK side
        dist_LK = distance_between_points(yL, zL, yK, zK)
        yLK_U, zLK_U = point_between_points(yL, zL, yK, zK, dist_LK-cov_Up)
        yLK_B, zLK_B = point_between_points(yL, zL, yK, zK, cov_Below)
        
        # Points between the IJ_U and LK_U points
        dist_IJ_LK_U = distance_between_points(yIJ_U, zIJ_U, yLK_U, zLK_U)
        yIJ_LK_U_L, zIJ_LK_U_L = point_between_points(yIJ_U, zIJ_U, yLK_U, zLK_U, cov_Left)
        yIJ_LK_U_R, zIJ_LK_U_R = point_between_points(yIJ_U, zIJ_U, yLK_U, zLK_U, dist_IJ_LK_U-cov_Right)
        # Points between the IJ_B and LK_B points
        dist_IJ_LK_B = distance_between_points(yIJ_B, zIJ_B, yLK_B, zLK_B)
        yIJ_LK_B_L, zIJ_LK_B_L = point_between_points(yIJ_B, zIJ_B, yLK_B, zLK_B, cov_Left)
        yIJ_LK_B_R, zIJ_LK_B_R = point_between_points(yIJ_B, zIJ_B, yLK_B, zLK_B, dist_IJ_LK_B-cov_Right)

        # Round the coordinates
        num_decimals = 4
        yIJ_U = round(yIJ_U, num_decimals)
        zIJ_U = round(zIJ_U, num_decimals)
        yIJ_B = round(yIJ_B, num_decimals)
        zIJ_B = round(zIJ_B, num_decimals)
        yLK_U = round(yLK_U, num_decimals)
        zLK_U = round(zLK_U, num_decimals)
        yLK_B = round(yLK_B, num_decimals)
        zLK_B = round(zLK_B, num_decimals)
        yIJ_LK_U_L = round(yIJ_LK_U_L, num_decimals)
        zIJ_LK_U_L = round(zIJ_LK_U_L, num_decimals)
        yIJ_LK_U_R = round(yIJ_LK_U_R, num_decimals)
        zIJ_LK_U_R = round(zIJ_LK_U_R, num_decimals)
        yIJ_LK_B_L = round(yIJ_LK_B_L, num_decimals)
        zIJ_LK_B_L = round(zIJ_LK_B_L, num_decimals)
        yIJ_LK_B_R = round(yIJ_LK_B_R, num_decimals)
        zIJ_LK_B_R = round(zIJ_LK_B_R, num_decimals)

        
        # Modify the original quad patch
        patch_modificado = [['patch', 'quad', matTag, numSubdivIJ, numSubdivJK,
                            unit_patch_layer(yIJ_LK_B_L, unit, 1),
                            unit_patch_layer(zIJ_LK_B_L, unit, 1),
                            unit_patch_layer(yIJ_LK_U_L, unit, 1), 
                            unit_patch_layer(zIJ_LK_U_L, unit, 1), 
                            unit_patch_layer(yIJ_LK_U_R, unit, 1), 
                            unit_patch_layer(zIJ_LK_U_R, unit, 1),
                            unit_patch_layer(yIJ_LK_B_R, unit, 1),
                            unit_patch_layer(zIJ_LK_B_R, unit, 1)]]
        
        # Add the cover to the quad patch
        # Left
        if cov_Left > 0:
            patch_modificado.append(['patch', 'quad', matTag+1, numSubdivIJ, 1, 
                                    unit_patch_layer(yIJ_B, unit, 1),
                                    unit_patch_layer(zIJ_B, unit, 1),
                                    unit_patch_layer(yIJ_U, unit, 1),
                                    unit_patch_layer(zIJ_U, unit, 1),
                                    unit_patch_layer(yIJ_LK_U_L, unit, 1),
                                    unit_patch_layer(zIJ_LK_U_L, unit, 1),
                                    unit_patch_layer(yIJ_LK_B_L, unit, 1),
                                    unit_patch_layer(zIJ_LK_B_L, unit, 1)])
                                    
        # Rigth
        if cov_Right > 0:
            patch_modificado.append(['patch', 'quad', matTag+1, numSubdivIJ, 1, 
                                    unit_patch_layer(yIJ_LK_B_R, unit, 1),
                                    unit_patch_layer(zIJ_LK_B_R, unit, 1),
                                    unit_patch_layer(yIJ_LK_U_R, unit, 1),
                                    unit_patch_layer(zIJ_LK_U_R, unit, 1),
                                    unit_patch_layer(yLK_U, unit, 1),
                                    unit_patch_layer(zLK_U, unit, 1),
                                    unit_patch_layer(yLK_B, unit, 1),
                                    unit_patch_layer(zLK_B, unit, 1)])
                                     
        # Below
        if cov_Below > 0:
            patch_modificado.append(['patch', 'quad', matTag+1, 1, numSubdivJK,
                                    unit_patch_layer(yI, unit, 1), 
                                    unit_patch_layer(zI, unit, 1), 
                                    unit_patch_layer(yIJ_B, unit, 1),
                                    unit_patch_layer(zIJ_B, unit, 1),
                                    unit_patch_layer(yLK_B, unit, 1),
                                    unit_patch_layer(zLK_B, unit, 1),
                                    unit_patch_layer(yL, unit, 1),
                                    unit_patch_layer(zL, unit, 1)])
                                    
        # Up
        if cov_Up > 0:
            patch_modificado.append(['patch', 'quad', matTag+1, 1, numSubdivJK,
                                    unit_patch_layer(yIJ_U, unit, 1),
                                    unit_patch_layer(zIJ_U, unit, 1),
                                    unit_patch_layer(yJ, unit, 1),
                                    unit_patch_layer(zJ, unit, 1),
                                    unit_patch_layer(yK, unit, 1),
                                    unit_patch_layer(zK, unit, 1),
                                    unit_patch_layer(yLK_U, unit, 1),
                                    unit_patch_layer(zLK_U, unit, 1)])
    
    elif patch_layer_type == 'patch' and type_element == 'circ':
        
        # Get cover parameters
        cover_ini = float(cover_i.value)
        cover_end = float(cover_e.value)
        
        # Get the original circ patch parameters
        matTag = int(patch_original[2])
        numSubdivCirc = int(patch_original[3])
        numSubdivRad = int(patch_original[4])
        yc = float(patch_original[5])
        zc = float(patch_original[6])
        r_ini = float(patch_original[7])
        r_end = float(patch_original[8])
        ang_ini = float(patch_original[9])
        ang_end = float(patch_original[10])
        
        # Modify the original circ patch
        patch_modificado = [['patch', 'circ', matTag, numSubdivCirc, numSubdivRad, 
                             unit_patch_layer(yc, unit, 1), 
                             unit_patch_layer(zc, unit, 1), 
                             unit_patch_layer(r_ini + cover_ini, unit, 1),
                             unit_patch_layer(r_end - cover_end, unit, 1),
                             unit_patch_layer(ang_ini, unit, 1),
                             unit_patch_layer(ang_end, unit, 1)]]
        
        # Add the cover to the circ patch
        # Inner cover
        if cover_ini > 0:
            patch_modificado.append(['patch', 'circ', matTag+1, numSubdivCirc, 1, 
                                    unit_patch_layer(yc, unit, 1), 
                                    unit_patch_layer(zc, unit, 1), 
                                    unit_patch_layer(r_ini, unit, 1),
                                    unit_patch_layer(r_ini + cover_ini, unit, 1),
                                    unit_patch_layer(ang_ini, unit, 1),
                                    unit_patch_layer(ang_end, unit, 1)])
        # Outer cover
        if cover_end > 0:
            patch_modificado.append(['patch', 'circ', matTag+1, numSubdivCirc, 1, 
                                    unit_patch_layer(yc, unit, 1), 
                                    unit_patch_layer(zc, unit, 1), 
                                    unit_patch_layer(r_end - cover_end, unit, 1),
                                    unit_patch_layer(r_end, unit, 1),
                                    unit_patch_layer(ang_ini, unit, 1),
                                    unit_patch_layer(ang_end, unit, 1)])
        
    else:
        cover_params_output.value = "Error: The cover can only be added to a patch."
        return
    
    # Delete the patch or layer to edit from the section
    try:
        params = eval(section_params_output.value)
        if not isinstance(params, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = section_params_output.value
        section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return

    for item in params:
        if str(item) == patch_original_recover:
            params.remove(item)
            break
    
    # Add the new patch or layer to the section
    params = params + patch_modificado
    
    # Show the actual section with the new patch or layer
    params_string = str(params).replace("[[", "[\n[")
    params_string = params_string.replace("], [", "],\n[")
    params_string = params_string.replace("]]", "]\n]")
    
    cover_params_output.value = params_string
    
    # Show the section with cover
    show_section_cover()


# Function to add cover to the section
def Cover(change=None):
    # Verify that the element selected is a element
    selected_patch = edit_patch_layer_dropdown.value
    if selected_patch == '-':
        code_params_output.value = "Error: Select a rect patch to add the cover."
        return
    
    # Verify that the element is a rect patch.
    selected_patch = eval(selected_patch)
    patch_layer_type = selected_patch[0]
    type_element = selected_patch[1]
    # If the element is not a rect patch or quad patch, show an error message
    if (patch_layer_type, type_element) not in [('patch', 'rect'), ('patch', 'quad'), ('patch', 'circ')]:
        code_params_output.value = "Error: The cover can only be added to a patch."
        return
    
    # CREATE COVER
    # Disable the button
    cover_button.disabled = True
    
    # Disable the other buttons
    replicate_button.disabled = True
    add_section_button.disabled = True
    add_patch_layer_button.disabled = True
    refresh_button.disabled = True
    video_button.disabled = True
    code_button.disabled = True
    CP_button.disabled = True
    material_button.disabled = True
    center_button.disabled = True
    edit_patch_layer_button.disabled = True
    edit_patch_layer_dropdown.disabled = True
    cancel_patch_layer_button.disabled = True
    section_params_output.disabled = True
    
    # Update description of the button
    save_cover_button.description = 'Save'
    
    # Show widgets of interest
    button_box_cover = widgets.HBox([save_cover_button, delete_cover_button])
    if type_element == 'rect' or type_element == 'quad':
        text_box_cover_1 = widgets.VBox([cov_L, cov_R], layout=widgets.Layout(width='100px'))
        text_box_cover_2 = widgets.VBox([cov_U, cov_B], layout=widgets.Layout(width='100px'))
        text_box_cover = widgets.HBox([text_box_cover_1, text_box_cover_2])
        text_cover_out = widgets.HTML(value="Section with Cover:", layout=widgets.Layout(margin="9px 0 0 2px"))
        text_cover_out.style.font_size = '14px'
        model_widgets.children = [cover_instructions_button, text_box_cover,
            button_box_cover, text_cover_out, cover_params_output]
    
    elif type_element == 'circ':
        text_box_cover_1 = widgets.VBox([cover_i], layout=widgets.Layout(width='100px'))
        text_box_cover_2 = widgets.VBox([cover_e], layout=widgets.Layout(width='100px'))
        text_box_cover = widgets.HBox([text_box_cover_1, text_box_cover_2])
        text_cover_out = widgets.HTML(value="Section with Cover:", layout=widgets.Layout(margin="9px 0 0 2px"))
        text_cover_out.style.font_size = '14px'
        model_widgets.children = [cover_instructions_button, text_box_cover,
            button_box_cover, text_cover_out, cover_params_output]
    
    # Calculate the section with cover and show it
    fiber_section_cover()


# %%%% [03-02-03] SHOW_VIDEO
# Function to show video of the section
def show_video(change=None):
    try:
        params = eval(section_params_output.value)
        if not isinstance(params, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = section_params_output.value
        section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return

    # Remove unit annotations from the plot parameters
    unit_factors_new = {
        'm': {'m': 1, 'cm': 0.01, 'mm': 0.001, 'ft': 0.3048, 'IN': 0.0254},
        'cm': {'m': 100, 'cm': 1, 'mm': 0.1, 'ft': 30.48, 'IN': 2.54},
        'mm': {'m': 1000, 'cm': 10, 'mm': 1, 'ft': 304.8, 'IN': 25.4},
        'ft': {'m': 3.2808399, 'cm': 0.032808399, 'mm': 0.00328084, 'ft': 1, 'IN': 0.0833333},
        'IN': {'m': 39.370079, 'cm': 0.39370079, 'mm': 0.039370079, 'ft': 12, 'IN': 1}
    }
    graphic_unit = graphic_unit_dropdown.value

    for param in params:
        for i in range(len(param)):
            if isinstance(param[i], str) and '*' in param[i]:
                # Split the string into value and unit
                parts = param[i].split('*')
                # Convert the value to float
                value = float(parts[0])
                # Get the conversion factor for the unit
                unit_str = parts[1]
                factor = unit_factors_new[graphic_unit][unit_str]
                # Check if the unit is squared
                if '**2' in param[i]:
                    factor = factor ** 2
                # Convert the value to the desired unit
                param[i] = value * factor

    with out:
        # See list to plot programmer window
        # programmer_output.value = str(params)
        out.clear_output(wait=True)

        add_section_button.description = '-'
        add_patch_layer_button.description = '-'
        refresh_button.description = '-'
        code_button.description = '-'
        cover_button.description = '-'
        replicate_button.description = '-'
        CP_button.description = '-'
        material_button.description = '-'
        center_button.description = '-'
        cancel_patch_layer_button.description = '-'
        edit_patch_layer_button.description = '-'
        video_button.description = '>>Frames...'
        code_params_output.value = "Creating frames..."
        add_section_button.disabled = True
        add_patch_layer_button.disabled = True
        refresh_button.disabled = True
        code_button.disabled = True
        cover_button.disabled = True
        replicate_button.disabled = True
        CP_button.disabled = True
        center_button.disabled = True
        material_button.disabled = True
        cancel_patch_layer_button.disabled = True
        edit_patch_layer_button.disabled = True
        element_type_dropdown.disabled = True
        patch_layer_type_dropdown.disabled = True
        unit_dropdown.disabled = True
        secTag_input.disabled = True
        GJ_input.disabled = True
        model_widgets.children = []

        xlabel_x = f'z [{graphic_unit}]'
        ylabel_x = f'y [{graphic_unit}]'
        opsv1.foto_fiber_section(params,
                                 r"C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Fotogramas_Video", xlabel_x, ylabel_x)  # Crea fotogramas para video.
        FPS = 15
        video_button.description = '>>Video...'
        code_params_output.value = "Creating video..."
        vid.video(r"C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Fotogramas_Video",
                  r"C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Fib_Sec_GUI01_fps_" + f"{FPS}.mp4",
                  FPS)
        display(Video(filename=f"C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Fib_Sec_GUI01_fps_{FPS}.mp4", width=640,
                      height=450))

        add_section_button.description = 'Delete Section'
        add_patch_layer_button.description = 'Add'
        refresh_button.description = 'MatTag'
        video_button.description = video_button.description = 'Video'
        code_button.description = 'Code'
        cover_button.description = 'Cover'
        replicate_button.description = 'Replicate'
        material_button.description = 'Strength'
        center_button.description = 'Center'
        CP_button.description = 'Calculate CP'
        cancel_patch_layer_button.description = 'Copy'
        edit_patch_layer_button.description = 'Edit'
        add_section_button.disabled = False
        add_patch_layer_button.disabled = False
        refresh_button.disabled = False
        code_button.disabled = False
        cover_button.disabled = False
        replicate_button.disabled = False
        CP_button.disabled = False
        material_button.disabled = False
        center_button.disabled = False
        cancel_patch_layer_button.disabled = False
        edit_patch_layer_button.disabled = False
        element_type_dropdown.disabled = False
        patch_layer_type_dropdown.disabled = False
        unit_dropdown.disabled = False
        update_input_widgets()
        code_params_output.value = "Video created successfully"


# %%%% [03-02-03] SHOW_CODE
# Function to update code for section
def show_code(change=None):
    try:
        section = eval(section_params_output.value)
        if not isinstance(section, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = section_params_output.value
        section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return
    # Find all unique units in the section list
    units = set()
    for item in section:
        for subitem in item:
            if isinstance(subitem, str) and '*' in subitem:
                unit = subitem.split('*')[1]
                units.add(unit)

    # Create a dictionary for each unique unit with an empty placeholder
    unit_placeholders = {unit: '' for unit in units}

    # Add a string "$" for recover ' in special elements.
    special = ['section', 'Fiber', 'patch', 'rect', 'quad', 'circ', 'layer', 'straight', '-GJ']
    for item in section:
        for i in range(len(item)):
            if item[i] in special:
                item[i] = str('$' + item[i].replace("'", "") + '$')

    # Remove unit annotations from the plot parameters
    unit_factors_new = {
        'm': {'m': 1, 'cm': 0.01, 'mm': 0.001, 'ft': 0.3048, 'IN': 0.0254},
        'cm': {'m': 100, 'cm': 1, 'mm': 0.1, 'ft': 30.48, 'IN': 2.54},
        'mm': {'m': 1000, 'cm': 10, 'mm': 1, 'ft': 304.8, 'IN': 25.4},
        'ft': {'m': 3.2808399, 'cm': 0.032808399, 'mm': 0.00328084, 'ft': 1, 'IN': 0.0833333},
        'IN': {'m': 39.370079, 'cm': 0.39370079, 'mm': 0.039370079, 'ft': 12, 'IN': 1}
    }
    graphic_unit = graphic_unit_dropdown.value

    # Create the template
    template = """import opsvis as opsv
import matplotlib.pyplot as plt
"""
    # Write the units to use in the definition of the section.
    for unit in unit_placeholders:
        factor = unit_factors_new[graphic_unit][unit]
        template += f"{unit} = {factor} # Complete this field according the units of your code.\n"

    # Write the section parameters
    for index, item in enumerate(section):
        item_str = str(item).replace("'", "")
        item_str = item_str.replace("$", "'")
        if index == 0:
            template += f"\nsection = [{item_str},\n"
        elif index != 0 and index != len(section) - 1:
            template += " " * 11 + f"{item_str},\n"
        else:
            template += " " * 11 + f"{item_str}]\n"

    # Template code
    template += """
opsv.plot_fiber_section(section)        # Display section
plt.axis('equal')
plt.savefig(r'img_CP.png')              # Save image

# Define section in Openseespy. Remember define materials before define the section
opsv.fib_sec_list_to_cmds(section_CP)"""
    code_params_output.value = template


# %%%% [03-02-04] DEFINE_MATERIAL
# Function to define material strength
def define_material(change=None):
    if material_button.description == 'Strength':
        material_button.description = 'Save'
        material_button.style.button_color = 'green'
        element_type_dropdown.disabled = True
        patch_layer_type_dropdown.disabled = True
        add_section_button.disabled = True
        add_patch_layer_button.disabled = True
        refresh_button.disabled = True
        video_button.disabled = True
        code_button.disabled = True
        cover_button.disabled = True
        replicate_button.disabled = True
        CP_button.disabled = True
        center_button.disabled = True
        secTag_input.disabled = True
        GJ_input.disabled = True
        unit_dropdown.disabled = True

        # Widgets to define model
        text_strength = widgets.HTML(value="Material Strength (MatTag): ")
        text_strength.style.font_size = '14px'
        new_widgets = [f_1_input, f_2_input, f_3_input, f_4_input, f_5_input, f_6_input, f_7_input, f_8_input,
                       f_9_input, f_10_input, f_11_input, f_12_input, f_13_input, f_14_input, f_15_input, f_16_input,
                       f_17_input, f_18_input, f_19_input, f_20_input, f_21_input]
        model_widgets.children = [text_strength] + new_widgets
        # Message to user
        code_params_output.value = "Define the material strength in the input boxes"

    else:
        material_button.description = 'Strength'
        material_button.style.button_color = None
        # Save the material strength in a .txt file how a dictionary
        strength_dict = {
            '1': float(f_1_input.value),
            '2': float(f_2_input.value),
            '3': float(f_3_input.value),
            '4': float(f_4_input.value),
            '5': float(f_5_input.value),
            '6': float(f_6_input.value),
            '7': float(f_7_input.value),
            '8': float(f_8_input.value),
            '9': float(f_9_input.value),
            '10': float(f_10_input.value),
            '11': float(f_11_input.value),
            '12': float(f_12_input.value),
            '13': float(f_13_input.value),
            '14': float(f_14_input.value),
            '15': float(f_15_input.value),
            '16': float(f_16_input.value),
            '17': float(f_17_input.value),
            '18': float(f_18_input.value),
            '19': float(f_19_input.value),
            '20': float(f_20_input.value),
            '21': float(f_21_input.value)
        }
        with open(r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Material_Strength.txt', 'w') as outFile:
            outFile.write(str(strength_dict))

        element_type_dropdown.disabled = False
        patch_layer_type_dropdown.disabled = False
        add_section_button.disabled = False
        add_patch_layer_button.disabled = False
        refresh_button.disabled = False
        video_button.disabled = False
        code_button.disabled = False
        cover_button.disabled = False
        replicate_button.disabled = False
        CP_button.disabled = False
        center_button.disabled = False
        unit_dropdown.disabled = False
        
        # Clear the widgets
        model_widgets.children = []
        
        # Message to the user
        code_params_output.value = "Material strength saved successfully"


# %%%% [03-02-05] CALCULATE_CP
# Function to calculate the plastic centroid
def call_calculate_cp(fib_sec, materials):
    adjusted_fib_sec = CP.Seccion_CP(fib_sec, materials)
    return adjusted_fib_sec


# Function to calculate the plastic centroid
def calculate_CP(change=None):
    # Get the section defined by the user using the GUI, and transform it into a list
    try:
        section = eval(section_params_output.value)
        if not isinstance(section, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = section_params_output.value
        section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return

    # Remove unit annotations from the plot parameters
    unit_factors_new = {
        'm': {'m': 1, 'cm': 0.01, 'mm': 0.001, 'ft': 0.3048, 'IN': 0.0254},
        'cm': {'m': 100, 'cm': 1, 'mm': 0.1, 'ft': 30.48, 'IN': 2.54},
        'mm': {'m': 1000, 'cm': 10, 'mm': 1, 'ft': 304.8, 'IN': 25.4},
        'ft': {'m': 3.2808399, 'cm': 0.032808399, 'mm': 0.00328084, 'ft': 1, 'IN': 0.0833333},
        'IN': {'m': 39.370079, 'cm': 0.39370079, 'mm': 0.039370079, 'ft': 12, 'IN': 1}
    }
    graphic_unit = graphic_unit_dropdown.value

    # Replace the string of the unit with a conversion factor
    section_values = section
    for item in section_values:
        for i in range(len(item)):
            if isinstance(item[i], str) and '*' in item[i]:
                parts = item[i].split('*')  # Split the string into value and unit
                value = float(parts[0])  # Convert the value to float
                unit_str = parts[1]  # Get the conversion factor for the unit
                factor = unit_factors_new[graphic_unit][unit_str]
                # Check if the unit is squared
                if '**2' in item[i]:
                    factor = factor ** 2
                item[i] = value * factor  # Convert the value to the desired unit

    # Get the material strength from the dictionary defined in the .txt file
    with open(r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Material_Strength.txt', 'r') as file:
        strength_dict = eval(file.read())

    # Obtain the section in the CP
    cp_section = call_calculate_cp(section_values, strength_dict)

    # Add the units to the cp_section. The units are in the same place that was in the original section.
    try:
        section = eval(section_params_output.value)
        if not isinstance(section, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        raise ValueError("Invalid list format")

    for item in section:
        for i in range(len(item)):
            if isinstance(item[i], str) and '*' in item[i]:
                value = cp_section[section.index(item)][i]  # Get the value from the cp_section
                unit_str = '*' + graphic_unit
                # Check if the unit is squared
                if '**2' in item[i]:
                    unit_str = '*' + graphic_unit + '**2'
                cp_section[section.index(item)][i] = str(value) + unit_str

    # Display the section around the plastic centroid
    cp_section_string = str(cp_section).replace("[[", "[\n[")
    cp_section_string = cp_section_string.replace("], [", "],\n[")
    cp_section_string = cp_section_string.replace("]]", "]\n]")
    code_params_output.value = f"""Section in PC: (Copy & paste in 'Fiber Section'. Then press 'MatTag')
{cp_section_string}"""


# %%%% [03-02-06] SHOW_INSTRUCTIONS
# Function to show instructions
def show_instructions(change=None):
    code_params_output.value = """Instructions:
1.- Choose the units for the graphic (Graphic Unit).
2.- Choose a section tag (secTag) and a value for GJ
3.- Add a section definition using the button 'Add Section'
4.- Choose the element type (patch or layer) and the type (rect, quad, circ, straight)
5.- Choose the units (Units) of each element type
6.- Complete each parameter
7.- Add a patch or layer using the button 'Add'
Note:
N.1.- You can modify the section directly from the box Fiber Section.
N.2.- Show the section using the button 'MatTag'
N.3.- Show the section video using the button 'Video'
N.4.- Define the material strength using the button 'Strength'. 
N.5.- You can draw the section using any point as origin. 
N.6.- Subsequently calculate the location of the plastic centroid with the button 'Solve PC'.
N.7.- Copy the section created and paste in the box Fiber Section. Then, show the section at PC using the button 'MatTag'.
N.8.- Show the section code using the button 'Code'
N.9.- Show the center of the fiber section using the button 'Center'.
N.10.- 'Center' also create a .txt file with the center of the fiber section.
"""


# %%%% [03-02-07] SHOW_CENTER_SECTION
# Function to show the center fiber section
def show_center_section(change=None):
    try:
        params = eval(section_params_output.value)
        if not isinstance(params, list):
            raise ValueError("Invalid list format")
    except Exception as e:
        actual = section_params_output.value
        section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
        return

    # Remove unit annotations from the plot parameters
    unit_factors_new = {
        'm': {'m': 1, 'cm': 0.01, 'mm': 0.001, 'ft': 0.3048, 'IN': 0.0254},
        'cm': {'m': 100, 'cm': 1, 'mm': 0.1, 'ft': 30.48, 'IN': 2.54},
        'mm': {'m': 1000, 'cm': 10, 'mm': 1, 'ft': 304.8, 'IN': 25.4},
        'ft': {'m': 3.2808399, 'cm': 0.032808399, 'mm': 0.00328084, 'ft': 1, 'IN': 0.0833333},
        'IN': {'m': 39.370079, 'cm': 0.39370079, 'mm': 0.039370079, 'ft': 12, 'IN': 1}
    }
    graphic_unit = graphic_unit_dropdown.value

    for param in params:
        for i in range(len(param)):
            if isinstance(param[i], str) and '*' in param[i]:
                # Split the string into value and unit
                parts = param[i].split('*')
                # Convert the value to float
                value = float(parts[0])
                # Get the conversion factor for the unit
                unit_str = parts[1]
                factor = unit_factors_new[graphic_unit][unit_str]
                # Check if the unit is squared
                if '**2' in param[i]:
                    factor = factor ** 2
                # Convert the value to the desired unit
                param[i] = value * factor

    with out:
        # See list to plot programmer window
        # programmer_output.value = str(params)
        out.clear_output(wait=True)
        xlabel_x = f'z [{graphic_unit}]'
        ylabel_x = f'y [{graphic_unit}]'
        center_fiber_patch, center_fiber_straight, center_fiber_circle, center_fiber_wedge = CF.plot_center_fiber_section(params, xlabel_x, ylabel_x)
        plt.axis('equal')
        plt.savefig(r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones/Center_Fib_Sec_GUI01.png')
        plt.close()
        display(Image(filename=r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones/Center_Fib_Sec_GUI01.png'))

    # Create a dictionary in a .txt file with the center of the fiber section
    center_fiber_dict = {
        'center_fiber_patch': center_fiber_patch,
        'center_fiber_straight': center_fiber_straight,
        'center_fiber_circle': center_fiber_circle,
        'center_fiber_wedge': center_fiber_wedge
    }
    with open(r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Center_Fiber_Section.txt', 'w') as file:
        file.write(str(center_fiber_dict))

    code_params_output.value = """Section created successfully.
Center of the fiber section saved in the file 'Center_Fiber_Section.txt'"""


# %% [04] WIDGETS
# Dimension para ingresar datos numericos.
layout_var_1 = widgets.Layout(width='195px')
layout_var = widgets.Layout(width='185px')
layout_var_2 = widgets.Layout(width='175px')

# %%% [04-00] Dropdown
# Interactive widget to choose Patch or Layer
element_type_dropdown = Dropdown(
    options=['patch', 'layer'],
    value='patch',
    description='Element Type:',
    disabled=True,
    layout=layout_var_1
)

# Interactive widget for patch or layer type
patch_layer_type_dropdown = Dropdown(
    options=['rect', 'quad', 'circ'],
    value='rect',
    description='Type:',
    disabled=True,
    layout=layout_var_1
)

# Interactive widget for units
unit_dropdown = Dropdown(
    options=['-'],
    value='-',
    description='Units:',
    disabled=True,
    layout=layout_var_1
)

# New dropdown widget for graphic unit
graphic_unit_dropdown = Dropdown(
    options=['-', 'm', 'cm', 'mm', 'ft', 'IN'],
    value='-',
    description='Graphic Unit:',
    disabled=False,
    layout=layout_var_1
)

# Dropdown for modify the patch or layer in fiber section
edit_patch_layer_dropdown = Dropdown(
    options=['-'],
    value='-',
    disabled=True,
    layout=widgets.Layout(width='424px', margin='-3px 0 0 6px')
)

# Dropdown for set the zoom in the fiber section
zoom_dropdown = Dropdown(
    options=['1', '1.25', '1.50', '1.75', '2', '2.25', '2.50', '2.75', '3'],
    value='1',
    description='Zoom:',
    disabled=True,
    layout=widgets.Layout(width='144px', height='20px', margin='2px 0 0 -30px')
) # (width='155px', height='20px', margin='2px 0 0 120px')

# Dropdown for set the fiber plot
fiber_plot_dropdown = Dropdown(
    options=['On', 'Off'],
    value='On',
    description='Fibers:',
    disabled=True,
    layout=widgets.Layout(width='138px', height='20px', margin='2px 0 0 23px')
)


# %%% [04-01] Text - IntText
# Interactive widgets for section parameters
secTag_input = IntText(value=1, description='secTag:', layout=layout_var_1)
GJ_input = Text(value='1000000', description='GJ:', continuous_update=False, layout=layout_var_1)

# Interactive widgets for patch parameters
material_tag_input = IntText(value=1, description='Material Tag:', layout=layout_var)
nFibY_input = IntText(value=5, description='nFibY:', layout=layout_var)
nFibZ_input = IntText(value=2, description='nFibZ:', layout=layout_var)
y1_input = Text(value='0.0', description='y1:', continuous_update=False, layout=layout_var)
z1_input = Text(value='0.0', description='z1:', continuous_update=False, layout=layout_var)
y2_input = Text(value='40.0', description='y2:', continuous_update=False, layout=layout_var)
z2_input = Text(value='40.0', description='z2:', continuous_update=False, layout=layout_var)

# Extra widgets for different patch types
numSubdivIJ_input = IntText(value=4, description='numSubdivIJ:', layout=layout_var)
numSubdivJK_input = IntText(value=4, description='numSubdivJK:', layout=layout_var)
yI_input = Text(value='0.0', description='yI:', continuous_update=False, layout=layout_var)
zI_input = Text(value='60.0', description='zI:', continuous_update=False, layout=layout_var)
yJ_input = Text(value='90.0', description='yJ:', continuous_update=False, layout=layout_var)
zJ_input = Text(value='30.0', description='zJ:', continuous_update=False, layout=layout_var)
yK_input = Text(value='90.0', description='yK:', continuous_update=False, layout=layout_var)
zK_input = Text(value='110.0', description='zK:', continuous_update=False, layout=layout_var)
yL_input = Text(value='0.0', description='yL:', continuous_update=False, layout=layout_var)
zL_input = Text(value='80.0', description='zL:', continuous_update=False, layout=layout_var)

numSubdivCirc_input = IntText(value=2, description='#SdivAng:', layout=layout_var)
numSubdivRad_input = IntText(value=2, description='#SdivRad:', layout=layout_var)
yc_input = Text(value='0.0', description='yc:', continuous_update=False, layout=layout_var)
zc_input = Text(value='0.0', description='zc:', continuous_update=False, layout=layout_var)
r_ini_input = Text(value='0.0', description='r_ini:', continuous_update=False, layout=layout_var)
r_end_input = Text(value='20.0', description='r_end:', continuous_update=False, layout=layout_var)
ang_ini_input = Text(value='0.0', description='ang_ini: [°]', continuous_update=False, layout=layout_var)
ang_end_input = Text(value='360.0', description='ang_end: [°]', continuous_update=False, layout=layout_var)

numFiber_input = IntText(value=5, description='numFiber:', layout=layout_var)
areaFiber_input = Text(value='1.0', description='As:', continuous_update=False, layout=layout_var)
radius_input = Text(value='20.0', description='radius:', continuous_update=False, layout=layout_var)

# Extra widgets for material strength
f_1_input = Text(value='250.0', description='f_1:', continuous_update=False, layout=layout_var_2)
f_2_input = Text(value='0.0', description='f_2:', continuous_update=False, layout=layout_var_2)
f_3_input = Text(value='0.0', description='f_3:', continuous_update=False, layout=layout_var_2)
f_4_input = Text(value='0.0', description='f_4:', continuous_update=False, layout=layout_var_2)
f_5_input = Text(value='0.0', description='f_5:', continuous_update=False, layout=layout_var_2)
f_6_input = Text(value='0.0', description='f_6:', continuous_update=False, layout=layout_var_2)
f_7_input = Text(value='0.0', description='f_7:', continuous_update=False, layout=layout_var_2)
f_8_input = Text(value='0.0', description='f_8:', continuous_update=False, layout=layout_var_2)
f_9_input = Text(value='0.0', description='f_9:', continuous_update=False, layout=layout_var_2)
f_10_input = Text(value='0.0', description='f_10:', continuous_update=False, layout=layout_var_2)
f_11_input = Text(value='0.0', description='f_11:', continuous_update=False, layout=layout_var_2)
f_12_input = Text(value='0.0', description='f_12:', continuous_update=False, layout=layout_var_2)
f_13_input = Text(value='0.0', description='f_13:', continuous_update=False, layout=layout_var_2)
f_14_input = Text(value='0.0', description='f_14:', continuous_update=False, layout=layout_var_2)
f_15_input = Text(value='0.0', description='f_15:', continuous_update=False, layout=layout_var_2)
f_16_input = Text(value='0.0', description='f_16:', continuous_update=False, layout=layout_var_2)
f_17_input = Text(value='0.0', description='f_17:', continuous_update=False, layout=layout_var_2)
f_18_input = Text(value='0.0', description='f_18:', continuous_update=False, layout=layout_var_2)
f_19_input = Text(value='0.0', description='f_19:', continuous_update=False, layout=layout_var_2)
f_20_input = Text(value='0.0', description='f_20:', continuous_update=False, layout=layout_var_2)
f_21_input = Text(value='0.0', description='f_21:', continuous_update=False, layout=layout_var_2)

# Widgets to define the cover in rect patch and quad
layout_cover = widgets.Layout(width='135px', margin='0 0 0 -40px')
cov_L = Text(value='1.0', description='cov_L:', continuous_update=False, layout=layout_cover)
cov_R = Text(value='1.0', description='cov_R:', continuous_update=False, layout=layout_cover)
cov_U = Text(value='1.0', description='cov_U:', continuous_update=False, layout=layout_cover)
cov_B = Text(value='1.0', description='cov_B:', continuous_update=False, layout=layout_cover)

# Widgets to define the cover in circ patch
cover_e = Text(value='1.0', description='cov_e:', continuous_update=False, layout=layout_cover)
cover_i = Text(value='1.0', description='cov_i:', continuous_update=False, layout=layout_cover)

# Widgets to define the replicate in straight layer
layout_replicate = widgets.Layout(width='135px', margin='0 0 0 -40px')
num_copies = IntText(value=1, description='#_rep:', layout=layout_replicate)
dis_y = Text(value='40.0', description='dis_y:', continuous_update=False, layout=layout_replicate)
dis_z = Text(value='0.0', description='dis_z:', continuous_update=False, layout=layout_replicate)



# %%% [04-02] ZIP WDGT
# Define a VBox to zip widgets associated with the parameters of the Patch/Layer/Material strength
model_widgets = VBox(layout=widgets.Layout(width='215px', height='395px', padding='5px'))
# Define a VBox to zip widgets associated with the parameters of the section and patch/layer
section_widgets = VBox(layout=widgets.Layout(width='215px', padding='5px'))

# %%% [04-03] OBSERVE DROPDOWNS
# Observe changes in the dropdowns and modify the options in related widgets
element_type_dropdown.observe(update_patch_layer_type_options, names='value')
patch_layer_type_dropdown.observe(update_input_widgets, names='value')
graphic_unit_dropdown.observe(update_unit_options, names='value')
unit_dropdown.observe(update_input_widgets, names='value')


# %%% [04-05] BUTTONS

# ADD SECTION
# Button to add section.
add_section_button_layout = widgets.Layout(width='197px', height='27px', margin='3px 0 9px 0')
add_section_button = widgets.Button(description='Add Section', layout=add_section_button_layout)
add_section_button.style.button_color = 'green'
add_section_button.on_click(add_section_definition)

# ADD PATCH/LAYER
# Button to add patch/layer.
add_patch_layer_button_layout = widgets.Layout(width='63px')
add_patch_layer_button = widgets.Button(description='-', layout=add_patch_layer_button_layout)
add_patch_layer_button.disabled = True
add_patch_layer_button.on_click(add_patch_layer)
# Button to cancel patch/layer add.
cancel_patch_layer_button_layout = widgets.Layout(width='63px')
cancel_patch_layer_button = widgets.Button(description='-', layout=cancel_patch_layer_button_layout)
cancel_patch_layer_button.disabled = True
cancel_patch_layer_button.on_click(cancel_patch_layer)
# Button to edit patch/layer.
edit_patch_layer_button_layout = widgets.Layout(width='62px')
edit_patch_layer_button = widgets.Button(description='-', layout=edit_patch_layer_button_layout)
edit_patch_layer_button.disabled = True
edit_patch_layer_button.on_click(edit_patch_layer)

# CALCULATE COVER IN PATCH RECT
# Button to save the cover definition.
save_cover_button_layout = widgets.Layout(width='95px')
save_cover_button = widgets.Button(description='-', layout=save_cover_button_layout)
save_cover_button.style.button_color = 'green'
save_cover_button.on_click(save_cover)
# Button to delete the cover definition.
delete_cover_button_layout = widgets.Layout(width='95px')
delete_cover_button = widgets.Button(description='Cancel', layout=delete_cover_button_layout)
delete_cover_button.style.button_color = 'red'
delete_cover_button.on_click(delete_cover)
# Button with instructions about use of cover definition.
cover_instructions_button_layout = widgets.Layout(width='197px', height='27px', margin='3px 0 9px 0')
cover_instructions_button = widgets.Button(description='Cover Instructions', layout=cover_instructions_button_layout)
cover_instructions_button.on_click(cover_instructions)
# Button to calculate covers in section.
cover_button_layout = widgets.Layout(width='66px')  # con 5 82px
cover_button = widgets.Button(description='-', layout=cover_button_layout)
cover_button.disabled = True
cover_button.on_click(Cover)

# REPLICATE LAYER STRAIGHT
# Button to replicate layer straight.
replicate_instructions_button_layout = widgets.Layout(width='197px', height='27px', margin='3px 0 9px 0')
replicate_instructions_button = widgets.Button(description='Replicate Instructions', layout=replicate_instructions_button_layout)
replicate_instructions_button.on_click(replicate_instructions)
# Button to replicate layer straight.
replicate_button_layout = widgets.Layout(width='75px')
replicate_button = widgets.Button(description='-', layout=replicate_button_layout)
replicate_button.disabled = True
replicate_button.on_click(replicate)
# Button to save the replicate layer straight.
save_replicate_button_layout = widgets.Layout(width='95px')
save_replicate_button = widgets.Button(description='-', layout=save_replicate_button_layout)
save_replicate_button.style.button_color = 'green'
save_replicate_button.on_click(save_replicate)
# Button to cancel the replicate layer straight.
cancel_replicate_button_layout = widgets.Layout(width='95px')
cancel_replicate_button = widgets.Button(description='Cancel', layout=cancel_replicate_button_layout)
cancel_replicate_button.style.button_color = 'red'
cancel_replicate_button.on_click(delete_replicate)

# DISPLAY SECTION
# Button to refresh plot.
refresh_button_layout = widgets.Layout(width='66px')  # con 5 82px
refresh_button = widgets.Button(description='-', layout=refresh_button_layout)
refresh_button.disabled = True
refresh_button.on_click(show_material_section)
# Button to generate video of section.
video_button_layout = widgets.Layout(width='66px')  # con 5 82px
video_button = widgets.Button(description='-', layout=video_button_layout)
video_button.disabled = True
video_button.on_click(show_video)
# Button to generate text to code
code_button_layout = widgets.Layout(width='66px')  # con 5 82px
code_button = widgets.Button(description='-', layout=code_button_layout)
code_button.disabled = True
code_button.on_click(show_code)
# Button to generate graphic and dictionary with the center of the section
center_button_layout = widgets.Layout(width='66px')  # con 5 82px
center_button = widgets.Button(description='-', layout=center_button_layout)
center_button.disabled = True
center_button.on_click(show_center_section)

# PLASTIC CENTROID
# Button to calculate the plastic centroid
CP_button_layout = widgets.Layout(width='101px')  # con 5 82px
CP_button = widgets.Button(description='-', layout=CP_button_layout)
CP_button.disabled = True
CP_button.on_click(calculate_CP)
# Button to define the material strength
materia_button_layout = widgets.Layout(width='101px')  # con 5 82px
material_button = widgets.Button(description='-', layout=materia_button_layout)
material_button.disabled = True
material_button.on_click(define_material)

# INSTRUCTIONS
# Button to see instructions
instructions_button_layout = widgets.Layout(width='197px', margin='0 0 9px 0')
instructions_button = widgets.Button(description='Show Instructions', layout=instructions_button_layout)
instructions_button.on_click(show_instructions)

# %%% [04-06] TEXTAREA
# Display section parameters
section_params_output = Textarea(value='', layout=widgets.Layout(width='427px', height='237px'))
# Display code parameter
code_params_output = Textarea(value='', layout=widgets.Layout(width='1088px', height='300px'))
# Display for cover definition. Save the original section.
cover_params_output = Textarea(value='', disabled=True, layout=widgets.Layout(width='195px', height='205px'))
# Display for replicate definition. Save the original section.
replicate_params_output = Textarea(value='', disabled=True, layout=widgets.Layout(width='195px', height='205px'))


# %%% [04-07] OUTPUT
# Output widget to contain the plot
layout_rigth = widgets.Layout(width='630px', height='806px')
out = Output(layout=layout_rigth)  # Output


# %%% [04-08] MATH IN WIDGETS & DYNAMIC GRAPHICS
# Widgets in the GUI
widgets_list = [
    GJ_input, y1_input, z1_input, y2_input, z2_input,
    yI_input, zI_input, yJ_input, zJ_input, yK_input,
    zK_input, yL_input, zL_input, yc_input, zc_input,
    r_ini_input, r_end_input, ang_ini_input, ang_end_input,
    areaFiber_input, radius_input,
    f_1_input, f_2_input, f_3_input, f_4_input, f_5_input, f_6_input, f_7_input, f_8_input,
    f_9_input, f_10_input, f_11_input, f_12_input, f_13_input, f_14_input, f_15_input, f_16_input,
    f_17_input, f_18_input, f_19_input, f_20_input, f_21_input,
    cov_L, cov_R, cov_U, cov_B,
    cover_i, cover_e,
    num_copies, dis_y, dis_z
]

# Widgets in the GUI that affect the graphic
widgets_section_patch_layer = [
    y1_input, z1_input, y2_input, z2_input,
    yI_input, zI_input, yJ_input, zJ_input, yK_input,
    zK_input, yL_input, zL_input, yc_input, zc_input,
    r_ini_input, r_end_input, ang_ini_input, ang_end_input,
    areaFiber_input, radius_input
]

# Dropdowns in the GUI that affect the graphic
dropdowns_list = [
    element_type_dropdown, patch_layer_type_dropdown, unit_dropdown
]

# Dropdowns in the GUI that affect the visualization of the fiber section
dropdowns_visualization = [
    zoom_dropdown, fiber_plot_dropdown
]


# Widgets in the GUI that affect the graphic and must be integers
int_widgets_list = [
    nFibY_input, nFibZ_input, numSubdivIJ_input, 
    numSubdivJK_input, numSubdivCirc_input, numSubdivRad_input,
    numFiber_input, material_tag_input
]

# Widgets in the GUI that affect the cover graphic
widgets_cover = [
    cov_L, cov_R, cov_U, cov_B, cover_i, cover_e
]

# Widgets in the GUI that affect the replicate graphic
widgets_replicate = [
    num_copies, dis_y, dis_z
]

    
# Helper function to observe the widgets that must be integers
def observe_int_widget(widget_x):
    def handler_int(change):
        show_section_update()
    widget_x.observe(handler_int, names='value')


# Helper function to observe the widgets with mathematical expressions 
def observe_widget(widget_x):
    def handler(change):
        # Create a safe environment with only allowed names
        safe_env = {
            'pi': math.pi,
            'e': math.e,
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'log': math.log,  # Natural logarithm
            'log10': math.log10,  # Base-10 logarithm
            'exp': math.exp
        }
        try:
            # Evaluate the expression within the safe environment
            widget_x.value = str(eval(change['new'], {"__builtins__": None}, safe_env))
        except Exception as e:
            pass
    widget_x.observe(handler, names='value')


# Helper function to observe the widgets for fiber section plot
def observe_widget_fiber_section(widget_x):
    def handler_2(change):
        # Check if 'change['new']' is a mathematical expression or already a number
        try:
            # Attempt to convert 'change['new']' to float
            new_value = float(change['new'])
            # If successful, it's already a number, so no need to eval
            is_number = True
        except ValueError:
            # If conversion fails, it's not a simple number
            is_number = False

        # Only graph if 'change['new']' is already a number:
        if is_number:
            if add_patch_layer_button.description == 'Save':
                show_section_update()
        # Only evaluate if 'change['new']' is not already a number
        if not is_number:
            # Create a safe environment with only allowed names
            safe_env = {
                'pi': math.pi,
                'e': math.e,
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                'log': math.log,  # Natural logarithm
                'log10': math.log10,  # Base-10 logarithm
                'exp': math.exp
            }
            try:
                # Evaluate the expression within the safe environment
                widget_x.value = str(eval(change['new'], {"__builtins__": None}, safe_env))
            except Exception as e:
                pass   
    widget_x.observe(handler_2, names='value')


# Helper function to observe the dropdowns for fiber section plot
def observe_dropdown_fiber_section(dropdown_x):
    def handler_3(change):
        if add_patch_layer_button.description == 'Save':
            show_section_update()
    dropdown_x.observe(handler_3, names='value')


# Helper function to observe the widgets for cover fiber section plot
def observe_widget_cover_fiber_section(widget_x):
    def handler_4(change):
        # Check if 'change['new']' is a mathematical expression or already a number
        try:
            # Attempt to convert 'change['new']' to float
            new_value = float(change['new'])
            # If successful, it's already a number, so no need to eval
            is_number = True
        except ValueError:
            # If conversion fails, it's not a simple number
            is_number = False

        # Only graph if 'change['new']' is already a number:
        if is_number:
            fiber_section_cover()
        # Only evaluate if 'change['new']' is not already a number
        if not is_number:
            # Create a safe environment with only allowed names
            safe_env = {
                'pi': math.pi,
                'e': math.e,
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                'log': math.log,  # Natural logarithm
                'log10': math.log10,  # Base-10 logarithm
                'exp': math.exp
            }
            try:
                # Evaluate the expression within the safe environment
                widget_x.value = str(eval(change['new'], {"__builtins__": None}, safe_env))
            except Exception as e:
                pass   
    widget_x.observe(handler_4, names='value')


# Helper function to observe the widgets for cover fiber section plot
def observe_widget_replicate_fiber_section(widget_x):
    def handler_5(change):
        # Check if 'change['new']' is a mathematical expression or already a number
        try:
            # Attempt to convert 'change['new']' to float
            new_value = float(change['new'])
            # If successful, it's already a number, so no need to eval
            is_number = True
        except ValueError:
            # If conversion fails, it's not a simple number
            is_number = False

        # Only graph if 'change['new']' is already a number:
        if is_number:
            fiber_section_replicate()
        # Only evaluate if 'change['new']' is not already a number
        if not is_number:
            # Create a safe environment with only allowed names
            safe_env = {
                'pi': math.pi,
                'e': math.e,
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                'log': math.log,  # Natural logarithm
                'log10': math.log10,  # Base-10 logarithm
                'exp': math.exp
            }
            try:
                # Evaluate the expression within the safe environment
                widget_x.value = str(eval(change['new'], {"__builtins__": None}, safe_env))
            except Exception as e:
                pass   
    widget_x.observe(handler_5, names='value')


# Helper function to observe the dropdown with zoom
def observe_dropdown_zoom(dropdown_x):
    def handler_6(change):
        if add_patch_layer_button.description == 'Save':
            show_section_update()
        elif save_cover_button.description == 'Save':
            show_section_cover()
        elif save_replicate_button == 'Save':
            show_section_replicate()
        else:
            show_section()
    dropdown_x.observe(handler_6, names='value')


# Apply the observation to all integer widgets
for widget in int_widgets_list:
    observe_int_widget(widget)


# Apply the observation to all widgets
for widget in widgets_list:
    if widget in widgets_section_patch_layer:
        observe_widget_fiber_section(widget)
    elif widget in widgets_cover:
        observe_widget_cover_fiber_section(widget)
    elif widget in widgets_replicate:
        observe_widget_replicate_fiber_section(widget)
    else:
        observe_widget(widget)

# Apply the observation to all dropdowns
for dropdown in dropdowns_list:
    observe_dropdown_fiber_section(dropdown)

# Apply the observation in the zoom dropdown
for dropdown in dropdowns_visualization:
    observe_dropdown_zoom(dropdown)


# %%% [04-09] OBSERVE DROPDOWN EDIT PATCH/LAYER
# Observe changes in the textareas and modify the options in related widgets
section_params_output.observe(update_edit_patch_layer_options, names='value')

# Function to identify the patch or layer selected in the edit_patch_layer_dropdown
def update_patch_layer_image(change):

    # Higligth the patch or layer selected in the edit_patch_layer_dropdown
    if edit_patch_layer_dropdown.value != '-':
        
        # Make a list with the actual fiber section
        try:
            params = eval(section_params_output.value)
            if not isinstance(params, list):
                raise ValueError("Invalid list format")
        except Exception as e:
            actual = section_params_output.value
            section_params_output.value = str(actual) + "\nError: Check the actual section parameters."
            return
        
        # Find the element that is selected in the edit_patch_layer_dropdown
        patch_layer_higligth = eval(edit_patch_layer_dropdown.value)
        for item in params:
            if item == patch_layer_higligth:
                
                # Assign material tag = 21 to higligth the patch or layer 
                item[2] = 21
                # The 21 element of matcolor define the color of the patch or layer highlight
        
        # Graph the section with the patch or layer higligth equal to show_section()
        
        # Remove unit annotations from the plot parameters
        unit_factors_new = {
            'm': {'m': 1, 'cm': 0.01, 'mm': 0.001, 'ft': 0.3048, 'IN': 0.0254},
            'cm': {'m': 100, 'cm': 1, 'mm': 0.1, 'ft': 30.48, 'IN': 2.54},
            'mm': {'m': 1000, 'cm': 10, 'mm': 1, 'ft': 304.8, 'IN': 25.4},
            'ft': {'m': 3.2808399, 'cm': 0.032808399, 'mm': 0.00328084, 'ft': 1, 'IN': 0.0833333},
            'IN': {'m': 39.370079, 'cm': 0.39370079, 'mm': 0.039370079, 'ft': 12, 'IN': 1}
        }
        graphic_unit = graphic_unit_dropdown.value

        for param in params:
            for i in range(len(param)):
                if isinstance(param[i], str) and '*' in param[i]:
                    # Split the string into value and unit
                    parts = param[i].split('*')
                    # Convert the value to float
                    value = float(parts[0])
                    # Get the conversion factor for the unit
                    unit_str = parts[1]
                    factor = unit_factors_new[graphic_unit][unit_str]
                    # Check if the unit is squared
                    if '**2' in param[i]:
                        factor = factor ** 2
                    # Convert the value to the desired unit
                    param[i] = value * factor

        with out:
            # See list to plot programmer window
            # programmer_output.value = str(params)
            out.clear_output(wait=True)
            xlabel_x = f'z [{graphic_unit}]'
            ylabel_x = f'y [{graphic_unit}]'
            zoom = float(zoom_dropdown.value)
            opsv1.plot_fiber_section(params, xlabel_x, ylabel_x, zoom=zoom)
            plt.axis('equal')
            plt.savefig(r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones/Fib_Sec_GUI01.png')
            plt.close()
            display(Image(filename=r'C_GUI01_Fiber_Section/C_GUI01_Fiber_Section/Secciones/Fib_Sec_GUI01.png'))
        code_params_output.value = "Section created successfully"
        
            
        
# Observe changes in the edit_patch_layer_dropdown if there are change, update the image 
# to show the patch or layer selected
edit_patch_layer_dropdown.observe(update_patch_layer_image, names='value')

# %% [05] LAYOUT
# Layout of the interface

# %%% [05-00] TEXT
title = widgets.HTML(value="<b>Fiber Section - Openseespy</b>",
                     layout=widgets.Layout(width='285px', display="flex", justify_content="center",
                                           margin="0px 0px 9px 0px"))
title.style.font_size = '22px'
text = widgets.HTML(value="Actions in Fiber Section:", layout=widgets.Layout(margin="4px 0 0 7px"))
text.style.font_size = '14px'
text2 = widgets.HTML(value="Output window:", layout=widgets.Layout(width='249px', margin="5px 0 0 4px"))
text2.style.font_size = '14px'
text3 = widgets.HTML(
    value="<i>Inspired by plotSection matlab function (D. Vamvatsikos) and Opsvis library (S. Kokot). GUI developed by M. Ortiz.<i>",
    layout=widgets.Layout(width='700px', margin="0 0 0 2px"))
text3.style.font_size = '14px'
text_section_pc = widgets.HTML(value="<i>Calculate Plastic Centroid:</i>", layout=widgets.Layout(width='164px', margin="4px 0 0 57px"))
text_section_pc.style.font_size = '14px'
text_section = widgets.HTML(value="Define Section:", layout=widgets.Layout(margin="0px 0 0 2px"))
text_section.style.font_size = '14px'
text_patch_layer = widgets.HTML(value="Define Patch/Layer:", layout=widgets.Layout(margin="0px 0 0 2px"))
text_patch_layer.style.font_size = '14px'
text_edit_fiber_section = widgets.HTML(value="Edit Patch/Layer in Fiber Section:", layout=widgets.Layout(margin="9px 0 0 2px"))
text_edit_fiber_section.style.font_size = '14px'

# %%% [05-01] INTERFACE
button_box_1 = HBox([add_patch_layer_button, cancel_patch_layer_button, edit_patch_layer_button])
button_box_2 = HBox([text_section_pc, material_button, CP_button])
section_inputs_list = [instructions_button, text_section, graphic_unit_dropdown, secTag_input, GJ_input,
                       add_section_button, text_patch_layer, element_type_dropdown, patch_layer_type_dropdown, 
                       unit_dropdown, button_box_1, text_edit_fiber_section]
section_widgets.children = section_inputs_list

title_input = HBox([title], layout=widgets.Layout(justify_content='center'))
upper_input = HBox([section_widgets, model_widgets])
medium_input_2 = HBox([cover_button, replicate_button, code_button, refresh_button, center_button, video_button], layout=widgets.Layout(margin="0 0 0 2px"))

zoom_dropdown_box = HBox([zoom_dropdown], layout=widgets.Layout(margin="0 0 0 0"))
fiber_plot_dropdown_box = HBox([fiber_plot_dropdown], layout=widgets.Layout(margin="0 0 0 0"))
text_box = HBox([text, fiber_plot_dropdown_box, zoom_dropdown_box])
left_side = VBox([title_input, upper_input, edit_patch_layer_dropdown, text_box, medium_input_2, button_box_2, section_params_output])
right_side = VBox([out], layout=widgets.Layout(width='660px', height='806px'))
interface = HBox([left_side, right_side])
interface2 = VBox([interface, text2, code_params_output, text3])
display(interface2)

# %% [06] DEVELOPER 
# Layout programer
aux_programmer_view = False
if aux_programmer_view:
    import inspect
    programer_output = Textarea(value='', layout=widgets.Layout(width='1072px', height='380px'))  # 
    display(programer_output)

    # # Function to display in GUI variable in certain line of code
    def GUI_info(Text_in_string, line_of_code,  variable):
        """
        Function to display in GUI certain line of code
        :param Text_in_string: Variable in string
        :param line_of_code: Line of code
        :param variable: Variable to display
        :return: None
        
        Calling using:
        current_line = inspect.currentframe().f_lineno
        GUI_info('load_args = ', current_line, load_args)
        """
        template_message = f"""
    Line of Code: {line_of_code}
    {Text_in_string}
    """
        template_close_message = f"""
    --------------------------------------------
    """
        programer_output.value = programer_output.value + template_message + str(variable) + template_close_message

