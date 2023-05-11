#!/usr/bin/python3

import sys
import os
from datetime import datetime, timedelta

class Timestamp:
    def __init__(self, timestamp_string):
        self.timedelta = self.get_timedelta_from_timestamp_string(timestamp_string)

    @staticmethod
    def get_timedelta_from_timestamp_string(timestamp_string):
        t = datetime.strptime(timestamp_string, '%H:%M:%S.%f')
        return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)

    def get_timestamp_string(self):
        return str(self.timedelta)


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
    def __init__(self, timestamp, position, size):
        self.timestamp = timestamp
        self.position = position
        self.size = size

    @staticmethod
    def get_keyframe_from_keyframe_string(keyframe_string):
        timestamp_string, position_size_string = keyframe_string.split("=")
        timestamp = Timestamp(timestamp_string)
        position_size_list = position_size_string.split(" ")
        position = Position(int(position_size_list[0]), int(position_size_list[1]))
        size = Size(int(position_size_list[2]), int(position_size_list[3]))
        return Keyframe(timestamp, position, size) 

    @staticmethod
    def get_keyframe_string_from_keyframe(keyframe):
        timestamp_string = keyframe.timestamp.get_timestamp_string()
        position_size_string = " ".join([str(keyframe.position.x), str(keyframe.position.y), str(keyframe.size.w), str(keyframe.size.h)])
        return timestamp_string + "=" + position_size_string

    def __repr__(self):
        return Keyframe.get_keyframe_string_from_keyframe(self)



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

    def _get_path_with_edited_name(self):
        splited = self.path.split(".")
        return ".".join(splited[:-1]) + "_edited" + "." + splited[-1]

    def _get_lines(self):
        return KdenliveFile._read_lines_from_file(self.path)

    def _set_lines(self, lines):
        KdenliveFile._write_lines_to_file(lines, f"{self._get_path_with_edited_name()}")

    def _get_transition_rect_line(self):
        lines = self._get_lines()
        for l in lines:
            if "transition.rect" in l:
                return l
        return ""

    def _set_transition_rect_line(self, transition_rect_line):
        lines = self._get_lines()
        index = -1
        for e,l in enumerate(lines):
            if self.LSTRIP in l:
                index = e
        lines[index] = transition_rect_line
        self._set_lines(lines)


    def _generate_transition_rect_line_from_keyframes(self, keyframes):
        return self.LSTRIP + ";".join([Keyframe.get_keyframe_string_from_keyframe(k) for k in keyframes]) + self.RSTRIP

    def get_keyframes(self):
        keyframes = []
        transition_rect_line = self._get_transition_rect_line()
        transition_rect_line = transition_rect_line.lstrip(self.LSTRIP)
        transition_rect_line = transition_rect_line.rstrip(self.RSTRIP)
        for keyframe_string in transition_rect_line.split(";"):
            keyframes.append(Keyframe.get_keyframe_from_keyframe_string(keyframe_string))
        return keyframes

    def set_keyframes(self, keyframes):
        transition_rect_line = self._generate_transition_rect_line_from_keyframes(keyframes)
        self._set_transition_rect_line(transition_rect_line)


if __name__ == "__main__":
    kf = KdenliveFile(sys.argv[1])
