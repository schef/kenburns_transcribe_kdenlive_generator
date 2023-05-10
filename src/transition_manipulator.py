#!/usr/bin/python3


from typing import Optional

class TransitionManipulator:
    resolution = Size(0,0)

    def __init__(self, position: Position, size: Size):
        self.position = position
        self.size = size

    def get_zoom_percent(self):
        return self.size.w / self.resolution.w

    def change_size(self, zoom):
        current_zoom = self.get_zoom_percent()
        next_zoom = current_zoom + zoom
        w = int(int(self.size.w / current_zoom) * next_zoom)
        h = int(int(self.size.h / current_zoom) * next_zoom)
        return Size(w, h)

def change_zoom(params, zoom):
    position, size = get_position_size_from_params(params)
    tm = TransitionManipulator(position, size)
    changed_size = tm.change_size(zoom) 
    return get_params_from_position_size(tm.position, changed_size)

if __name__ == "__main__":
    tm = TransitionManipulator(position=Position(0, 0), size=Size(200, 200))
    print(tm.change_size(-0.1))
