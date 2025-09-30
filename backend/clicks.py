import autoit
from . import template_matching


def left_click_location(location: tuple):
    if location is None:
        print("Click skipped, no location found")
        return
    x, y = location
    autoit.mouse_click("left", x, y, clicks=1)

def left_hardcoded_clicks(coordinates: tuple, rect):
    if coordinates is None:
        print("Click skipped, no hardcoded coordinates found.")
        return
    x, y = coordinates
    absolute_x, absolute_y = (rect[0] + x), (rect[1] + y)
    autoit.mouse_click("left", absolute_x, absolute_y, clicks=1)