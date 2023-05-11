#!/usr/bin/python3


from kdenlive_file import Keyframe, Timestamp, Position, Size

class KeyframeManipulator:
    def __init__(self, resolution):
        self.resolution = resolution
    
    def get_zoom_percent(self, keyframe):
        return keyframe.size.w / self.resolution.w

    def change_size(self, keyframe, zoom):
        current_zoom = self.get_zoom_percent(keyframe)
        next_zoom = current_zoom + zoom
        w = int(int(keyframe.size.w / current_zoom) * next_zoom)
        h = int(int(keyframe.size.h / current_zoom) * next_zoom)
        keyframe.size = Size(w, h)

if __name__ == "__main__":
    keyframe = Keyframe(timestamp=Timestamp("0:0:0.0"), position=Position(0, 0), size=Size(100, 100))
    km = KeyframeManipulator(resolution=Size(100, 100))
