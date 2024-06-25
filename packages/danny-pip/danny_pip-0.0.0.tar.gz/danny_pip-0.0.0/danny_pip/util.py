import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import numpy as np

def show_slider(ufunc, **kwargs):
    '''
    rewritten slider function that take in ufunc and update
    '''
    min = kwargs["min"] if "min" in kwargs else 0                # default min to 0
    max = kwargs["max"]
    step = kwargs["step"] if "step" in kwargs else 25            # default to 25
    
    # Create a slider widget
    slider = widgets.IntSlider(
        value=0,
        min=min,
        max=max,
        step=step,
        description='Slider:',
        continuous_update=True
    )

    # Define a function that reacts to slider value changes
    def on_slider_change(change):
        clear_output(wait=True)
        value = change['new']
        ufunc(value)                        # here is the actual function to plot, arg only, kwarg on demand
        display(slider)                     # Redisplay the slider to keep it visible

    # Attach the function to the slider
    slider.observe(on_slider_change, names='value')

    # Display the slider and initial plot
    display(slider)
    on_slider_change({'new': slider.value})

