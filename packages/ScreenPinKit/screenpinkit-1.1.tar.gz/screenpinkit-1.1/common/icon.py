# coding: utf-8
from enum import Enum

from qfluentwidgets import FluentIconBase, getIconColor, Theme

class ScreenShotIcon(FluentIconBase, Enum):
    LOGO = "logo"
    SNAP = "snap"
    QUIT = "quit"
    SETTING = "setting"
    WHITE_BOARD = "whiteboard"
    COPY = "copy"
    TEXT = "text"
    ERASER = "eraser"
    PEN = "pen"
    SAVE_AS = "save_as"
    FINISHED = "finished"
    DELETE_ALL = "delete_all"
    BRUSH = "brush"
    UNDO = "undo"
    REDO = "redo"
    OCR = "ocr"
    GUIDE = "guide"
    CLICK_THROUGH = "click_through"

    ARROW = "arrow"
    MARKER_PEN = "marker_pen"
    STAR = "star"
    RECTANGLE = "rectangle"
    LINE_STRIP = "line_strip"
    POLYGON = "polygon"
    SELECT_ITEM = "select_item"
    MOSAIC = "mosaic"
    LOCKED = "locked"
    UNLOCKED = "unlocked"

    CIRCLE = "circle"
    SHAPE = "shape"
    FILL_REGION = "fill_region"
    TRIANGLE = "triangle"

    TEXT_BOLD = "bold"
    TEXT_ITALIC = "italic"
    FULL_Dot = "full_dot"
    FULL_RECTANGLE = "full_rectangle"
    BLUR = "blur"
    PIN = "pin"
    NUMBER_MARKER = "number_marker"

    WARNING_LIGHT = "warning"
    SUCCESS_LIGHT = "success"
    ERROR_LIGHT = "error"
    ROUNDED_CORNER = "rounded_corner"

    def path(self, theme=Theme.AUTO):
        return f':/ScreenPinKit/resource/icons/{self.value}.svg'