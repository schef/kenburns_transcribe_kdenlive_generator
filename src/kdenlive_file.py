#!/usr/bin/python3

import sys
import os
import random

class TransitionParams:
    def __init__(self, params):
        self.params = params
        splited = self.params.split(" ")
        self.x = splited[0]
        self.y = splited[1]
        self.w = splited[2]
        self.h = splited[3]

    def get_zoom_percent(self, root_transition_params):
        return int(self.w) / int(root_transition_params.w)

    def get_params(self, x, y, w, h):
        return " ".join([x, y, w, h])

    def zoom_transition(self, zoom, root_transition_params):
        current_zoom = self.get_zoom_percent(root_transition_params)
        next_zoom = current_zoom + zoom
        w = int(self.w) / int(current_zoom) * int(next_zoom)
        h = int(self.h) / int(current_zoom) * int(next_zoom)
        return self.get_params(self.x, self.y, str(w), str(h))

class KdenliveFile:
    LSTRIP = '    <property name="transition.rect">'
    RSTRIP = '</property>'

    def __init__(self, path):
        self.path = path
        self.root_transition_params = TransitionParams(self.get_transition_positions()[0])

    @staticmethod
    def get_full_path(path):
        return os.path.realpath(os.path.expanduser(path))

    @staticmethod
    def write_lines_to_file(lines, filename, newline_at_end=True):
        filename = KdenliveFile.get_full_path(filename)
        sufix = ("", "\n")[newline_at_end]
        with open(filename, 'w') as f:
            f.write("\n".join(lines) + sufix)

    @staticmethod
    def read_lines_from_file(filename):
        filename = KdenliveFile.get_full_path(filename)
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
        return lines

    def get_new_name(self):
        splited = self.path.split(".")
        return ".".join(splited[:-1]) + "_edited" + "." + splited[-1]

    def get_lines(self):
        return KdenliveFile.read_lines_from_file(self.path)

    def set_lines(self, lines):
        KdenliveFile.write_lines_to_file(lines, f"{self.get_new_name()}")

    def get_transition_rect_line(self):
        lines = self.get_lines()
        for l in lines:
            if "transition.rect" in l:
                return l
        return ""

    def get_transitions(self):
        transition_line = self.get_transition_rect_line()
        transition_line = transition_line.lstrip(self.LSTRIP)
        transition_line = transition_line.rstrip(self.RSTRIP)
        return transition_line.split(";")

    def get_transition_positions(self):
        transitions = self.get_transitions()
        transition_positions = []
        for t in transitions:
            transition_positions.append(t.split("=")[1])
        return transition_positions

    def generate_transition_position(self, timestamp, position):
        return f"{timestamp}={position}"

    def generate_transition_rect_line(self, transition_positions):
        return self.LSTRIP + ";".join(transition_positions) + self.RSTRIP

    def replace_transition_rect_line(self, transition_rect_line):
        lines = self.get_lines()
        index = -1
        for e,l in enumerate(lines):
            if self.LSTRIP in l:
                index = e
        lines[index] = transition_rect_line
        self.set_lines(lines)

    def set_transition_positions(self, transition_positions):
        transition_rect_line = self.generate_transition_rect_line(transition_positions)
        self.replace_transition_rect_line(transition_rect_line)

    def zoom_transition(self, zoom, transition):
        tp = TransitionParams(transition)
        return tp.zoom_transition(zoom, self.root_transition_params)

if __name__ == "__main__":
    kf = KdenliveFile(sys.argv[1])
