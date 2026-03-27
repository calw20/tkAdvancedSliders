from tkinter import Tk
from . import RangeSlider, RangeSliderNew, Slider
from tkinter import ttk

if __name__ == "__main__":
    # Short demo with two sliders - one with numbers 0.0-1.0, the other with timestamps 0:00 - 51:05
    DEMO_MAXIMUM_TIME_IN_SECONDS = 3065  # 51:05

    root = Tk()
    slider = RangeSlider(root)
    slider.grid(row=0)

    timestamp_slider = RangeSlider(root, value_min=0, value_max=DEMO_MAXIMUM_TIME_IN_SECONDS)
    timestamp_slider.grid(row=1)
    timestamp_slider.change_display(*RangeSlider.timestamp_display_builder(DEMO_MAXIMUM_TIME_IN_SECONDS))

    slider_original = Slider(
        root,
        width=400,
        height=60,
        min_val=-100,
        max_val=100,
        init_lis=[-50, 0, 75],
        show_value_label=True,
        removable=True,
        addable=True,
    )
    slider_original.grid(row=2)

    slider_new = RangeSliderNew(root)
    slider_new.grid(row=3)

    slider_new_new_3 = RangeSliderNew(root, num_knobs=3, step_size=0.1)
    slider_new_new_3.grid(row=4)

    slider_new_new = RangeSliderNew(root, num_knobs=5, width=300)
    slider_new_new.grid(row=5)

    spinbox = ttk.Spinbox(root)
    spinbox.grid(row=6)

    # Bind right-clicking on the window to return the values of 'in' and 'out'.
    # These are the primary outputs of this widget and what you would use in your code.
    # Note that the second widget returns the values in seconds because of the specific setup and not through necessity.

    def log_values(*args):
        print(f"New slider values: {slider_new.get_min_max_knobs()}")
        print(f"Top slider values: {slider.get_in_and_out()}")
        print(f"Bottom slider values: {timestamp_slider.get_in_and_out()}")
        print(f"Original Slider: {slider_original.get_values()}")
    root.bind('<Button-3>', log_values)

    root.title("tkAdvancedSliders Demo")
    root.mainloop()