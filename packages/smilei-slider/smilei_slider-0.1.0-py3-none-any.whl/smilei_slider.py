import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import numpy as np

def show_slider(diag, **kwargs):
    '''
    rewritten slider function that take in ufunc and update
    '''    
    # Create a slider widget
    slider = widgets.SelectionSlider(
        options=diag.getAvailableTimesteps(),
        description='Slider:',
        continuous_update=True
    )

    # Define a function that reacts to slider value changes
    def on_slider_change(change):
        clear_output(wait=True)
        value = change['new']
        diag.plot(value, **kwargs)          # diagnostic to be plotted
        display(slider)                     # Redisplay the slider to keep it visible

    # Attach the function to the slider
    slider.observe(on_slider_change, names='value')

    # Display the slider and initial plot
    display(slider)
    on_slider_change({'new': slider.value})