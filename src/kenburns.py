#!/usr/bin/python3

import sys
import random
from transcribe_file import TranscribeFile
from kdenlive_file import KdenliveFile
from keyframe_manipulator import *

position_overrides = {
    "W": 0,
    "BW": 1,
    "BC": 2,
    "MW": 3,
    "MC": 4,
    "SW": 5,
    "SC": 6,
    "RW": 7,
    "RC": 8,
}

if __name__ == "__main__":
    tf = TranscribeFile(sys.argv[1])
    kf = KdenliveFile(sys.argv[2])

    marks = tf.get_marks()
    keyframes = kf.get_keyframes()
    keyframes = []
    for mark in marks:
        keyframe = random.choice(keyframes)
        keyframe.timestamp.timedelta = mark.timedelta
        keyframes.append(keyframe)
    kf.set_keyframes(keyframes)
