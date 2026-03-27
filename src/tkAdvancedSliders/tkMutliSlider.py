from tkinter import *
from tkinter.ttk import *

from typing import Callable, Optional

from .common_typing import Numeric, KnobFormatOptions, \
      LineFormatOptions, KnobCompIds, KnobInfo

class Slider(Frame):
    LINE_COLOR = "#476b6b"
    LINE_WIDTH = 3

    # I think this is the bubble head
    SLIDER_LEFT_PADDING = 10
    
    DIGIT_PRECISION = ".1f"  # for showing in the canvas

    # relative step size in 0 to 1, set to 0 for no step size restiction
    # may be override by the step_size argument in __init__
    STEP_SIZE: float = 0.0

    def __init__(
        self,
        master,

        width: int = 400,
        height: int = 80,
        min_val: Numeric = 0,
        max_val: Numeric = 1,

        step_size: Optional[float] = None,
        
        init_lis: Optional[list[Numeric]] = None,

        show_value_label = True,
        removable = False,
        addable = False,

        *,
        value_display: Callable[[Numeric], str] | None = None,
        knob_format: KnobFormatOptions | None = None,
        allow_empty_bar: bool = False,

        line_format: LineFormatOptions | None = None,
    ):
        if step_size == None:
            # inherit from class variable
            step_size = self.STEP_SIZE
        assert step_size >= 0, "step size must be positive"
        assert step_size <= max_val - min_val, "step size must be smaller than range"
        assert min_val < max_val, "min value must be smaller than max value"

        self._value_display = value_display
        self._knob_format = knob_format if knob_format else KnobFormatOptions()
        self._line_format = line_format if line_format else LineFormatOptions()

        Frame.__init__(self, master, height=height, width=width)
        self.master = master

        init_lis = init_lis if init_lis is not None else []

        if allow_empty_bar and len(init_lis) == 0:
            init_lis = [min_val]

        self.init_lis = init_lis
        self.max_val = max_val
        self.min_val = min_val
        self.step_size_frac = step_size / float(max_val - min_val)  # step size fraction

        self.show_value = show_value_label
        self.H = height
        self.W = width
        self.canv_H = self.H
        self.canv_W = self.W
        if not show_value_label:
            self.slider_y = self.canv_H / 2  # y pos of the slider
        else:
            self.slider_y = self.canv_H * 2 / 5
        
        # TODO - Make this dynamic, should probs use the max slider size?
        self.slider_x = Slider.SLIDER_LEFT_PADDING  # x pos of the slider (left side)

        self._val_change_callback = lambda lis: None

        self.knobs: list[KnobInfo] = []
        self.selected_idx: int | None = None  # current selection bar index
        for value in self.init_lis:
            pos = (value - min_val) / (max_val - min_val)
            knob: KnobInfo = {
                "norm_pos": pos, 
                "ids": (None, None, None), # type: ignore 
                "value": value, 
                "fmt_options": self._knob_format
            } 
            self.knobs.append(knob)

        self.canv = Canvas(self, height=self.canv_H, width=self.canv_W)
        self.canv.pack()
        self.canv.bind("<Motion>", self._mouse_motion)
        self.canv.bind("<B1-Motion>", self._move_knob)
        
        # Add / Remove Bindings
        if removable:
            self.canv.bind("<3>", self._remove_knob)
        if addable:
            self.canv.bind("<ButtonRelease-1>", self._add_knob)

        self._track_idx = self.__add_track(
                self.slider_x, self.slider_y, # Start 
                self.canv_W - self.slider_x, self.slider_y # End
            )
        for knob in self.knobs:
            knob["ids"] = self.__add_knob(knob["norm_pos"])

    def get_values(self) -> list[float]:
        values = [bar["value"] for bar in self.knobs]
        return sorted(values)
    
    def set_value_change_callback(self, callback: Callable[[list[float]], None]):
        self._val_change_callback = callback

    def _mouse_motion(self, event):
        x = event.x
        y = event.y
        selection = self.__check_selection(x, y)
        if selection[0]:
            self.canv.config(cursor="hand2")
            self.selected_idx = selection[1]
        else:
            self.canv.config(cursor="")
            self.selected_idx = None

    def _move_knob(self, event):
        x = event.x
        y = event.y
        if self.selected_idx == None:
            return False
        pos = self._calc_pos(x)
        idx = self.selected_idx
        if self.step_size_frac > 0:
            curr_pos = self.knobs[idx]["norm_pos"]
            if abs(curr_pos - pos) < (self.step_size_frac * 0.75):
                return
            pos = round(pos / self.step_size_frac) * self.step_size_frac
        self.__move_knob(idx, pos)

    def _remove_knob(self, event):
        x = event.x
        y = event.y
        if self.selected_idx == None:
            return False
        idx = self.selected_idx
        ids = self.knobs[idx]["ids"]
        for id in ids:
            if id is None: continue
            self.canv.delete(id)
        self.knobs.pop(idx)

    # Event Wrapper for Tkinter
    def _add_knob(self, event: Event[Canvas]):
        x = event.x

        if self.selected_idx == None:
            pos = self._calc_pos(x)
            self._add_new_knob(pos, self._knob_format)

    def _add_new_knob(
            self, 
            pos: float, 
            head_format_options: KnobFormatOptions
        ) -> KnobCompIds:
        
        bar: KnobInfo = {
            "ids": (None, None, None), # type: ignore
            "norm_pos": pos,
            "value": pos,
            "fmt_options": head_format_options
        }
        self.knobs.append(bar)

        for i in self.knobs:
            ids = i["ids"]
            for id in ids:
                if id is None: continue
                self.canv.delete(id)

        for bar in self.knobs:
            bar["ids"] = self.__add_knob(bar["norm_pos"], bar["fmt_options"])

        return self.knobs[-1]["ids"]

    def __add_track(self, startx, starty, endx, endy):
        id1 = self.canv.create_line(
            startx, starty, endx, endy, 
            fill=self._line_format.colour, width=self._line_format.width
        )
        return id1

    def __add_knob(
            self, 
            pos: float, 
            head_format_options: KnobFormatOptions = KnobFormatOptions(),
        ) -> KnobCompIds:
        """@ pos: position of the bar, ranged from (0,1)"""
        if pos < 0 or pos > 1:
            raise Exception("Pos error - Pos: " + str(pos))
        
        R = head_format_options.outer_radius
        r = head_format_options.inner_radius
        L = self.canv_W - 2 * self.slider_x
        y = self.slider_y
        x = self.slider_x + pos * L

        id_outer, id_inner, id_value = None, None, None

        # Create Knob
        # Draw Outer Oval
        if True: #TODO Add logic
            id_outer = self.canv.create_oval(
                x - R,
                y - R,
                x + R,
                y + R,
                fill = head_format_options.outer_colour,
                width = head_format_options.line_width,
                outline="",
            )

        # Draw Inner Oval
        if True: #TODO Add logic
            id_inner = self.canv.create_oval(
                x - r, 
                y - r, 
                x + r, 
                y + r, 
                fill = head_format_options.inner_colour, 
                outline=""
            )

        # Show Text Formatter 
        if (head_format_options.show_text_label is None and self.show_value) or \
            head_format_options.show_text_label:

            y_value = y + head_format_options.outer_radius + 8
            value = pos * (self.max_val - self.min_val) + self.min_val
            id_value = self.canv.create_text(
                x, y_value, text=(self._value_display(value) if self._value_display else format(value, Slider.DIGIT_PRECISION))
            )

        return id_outer, id_inner, id_value

    def __move_knob(self, idx, pos):
        ids = self.knobs[idx]["ids"]
        
        # Loop over bar component ids
        for bc_id in ids:
            if bc_id is None: continue
            self.canv.delete(bc_id)

        self.knobs[idx]["ids"] = self.__add_knob(pos, self.knobs[idx]["fmt_options"])
        self.knobs[idx]["norm_pos"] = pos
        self.knobs[idx]["value"] = pos * (self.max_val - self.min_val) + self.min_val
        self._val_change_callback(self.get_values())

    def _calc_pos(self, x):
        """calculate position from x coordinate"""
        pos = (x - self.slider_x) / (self.canv_W - 2 * self.slider_x)
        if pos < 0:
            return 0
        elif pos > 1:
            return 1
        else:
            return pos

    def __check_selection(self, x, y):
        """
        To check if the position is inside the bounding rectangle of a Bar
        Return [True, bar_index] or [False, None]
        """
        for idx in range(len(self.knobs)):
            id = self.knobs[idx]["ids"][0]
            bbox = self.canv.bbox(id)
            if bbox[0] < x and bbox[2] > x and bbox[1] < y and bbox[3] > y:
                return [True, idx]
        return [False, None]
