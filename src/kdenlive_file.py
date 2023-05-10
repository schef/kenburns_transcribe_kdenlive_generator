#!/usr/bin/python3

import sys
import os

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"x[{self.x}], y[{self.y}]"

class Size:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __repr__(self):
        return f"w[{self.w}], h[{self.h}]"

class Keyframe:
    def __init__(self, position, size):
        self.position = position
        self.size = size

    @staticmethod
    def get_keyframe_from_transition_string(s):
        _, s = s.split("=")
        splited = s.split(" ")
        return Position(int(splited[0]), int(splited[1])), Size(int(splited[2]), int(splited[3]))

    @staticmethod
    def get_transition_string_from_position_size(position, size):
        return " ".join([str(position.x), str(position.y), str(size.w), str(size.h)])

    @staticmethod
    def get_transition_string_from_keyframe(keyframe):
        return " ".join([str(keyframe.position.x), str(keyframe.position.y), str(keyframe.size.w), str(keyframe.size.h)])

class KdenliveFile:
    LSTRIP = '    <property name="transition.rect">'
    RSTRIP = '</property>'

    def __init__(self, path):
        self.path = path

    @staticmethod
    def _get_full_path(path):
        return os.path.realpath(os.path.expanduser(path))

    @staticmethod
    def _write_lines_to_file(lines, filename, newline_at_end=True):
        filename = KdenliveFile._get_full_path(filename)
        sufix = ("", "\n")[newline_at_end]
        with open(filename, 'w') as f:
            f.write("\n".join(lines) + sufix)

    @staticmethod
    def _read_lines_from_file(filename):
        filename = KdenliveFile._get_full_path(filename)
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
        return lines

    def _get_new_name(self):
        splited = self.path.split(".")
        return ".".join(splited[:-1]) + "_edited" + "." + splited[-1]

    def _get_lines(self):
        return KdenliveFile._read_lines_from_file(self.path)

    def _set_lines(self, lines):
        KdenliveFile._write_lines_to_file(lines, f"{self._get_new_name()}")

    def get_transition_rect_line(self):
        lines = self._get_lines()
        for l in lines:
            if "transition.rect" in l:
                return l
        return ""

    def get_keyframes(self):
        keyframes = []
        transition_rect_line = self.get_transition_rect_line()
        transition_rect_line = transition_rect_line.lstrip(self.LSTRIP)
        transition_rect_line = transition_rect_line.rstrip(self.RSTRIP)
        for transition_string in transition_rect_line.split(";"):
            keyframes.append(Keyframe.get_keyframe_from_transition_string(transition_string))
        return keyframes

    def generate_transition_string(self, timestamp, keyframe):
        return f"{timestamp}={Keyframe.get_transition_string_from_keyframe(keyframe)}"

    def generate_transition_rect_line(self, transition_string):
        return self.LSTRIP + ";".join(transition_string) + self.RSTRIP

    def replace_transition_rect_line(self, transition_rect_line):
        lines = self._get_lines()
        index = -1
        for e,l in enumerate(lines):
            if self.LSTRIP in l:
                index = e
        lines[index] = transition_rect_line
        self._set_lines(lines)

    def set_transition_positions(self, transition_positions):
        transition_rect_line = self.generate_transition_rect_line(transition_positions)
        self.replace_transition_rect_line(transition_rect_line)


if __name__ == "__main__":
    kf = KdenliveFile(sys.argv[1])
