#!/usr/bin/python3

import sys
import random
from copy import deepcopy
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

def get_next_random_unique_keyframe(last_keyframe, keyframes_positions):
    next_keyframe = random.choice(keyframes_positions)
    while next_keyframe == last_keyframe:
        next_keyframe = random.choice(keyframes_positions)

if __name__ == "__main__":
    tf = TranscribeFile(sys.argv[1])
    kf = KdenliveFile(sys.argv[2])
    marks = tf.get_marks()
    keyframes_positions = kf.get_keyframes()
    keyframes = []
    km = KeyframeManipulator(keyframes_positions[0].size)
    last_keyframe = None
    for mark in marks:

        if len(keyframes) % 2 == 1:
            next_keyframe = last_keyframe
            keyframe = deepcopy(next_keyframe)
            km.change_size(keyframe, 0.1)
        else: 
            next_keyframe = get_next_random_unique_keyframe(last_keyframe, keyframes_positions)
            keyframe = deepcopy(next_keyframe)

        last_keyframe = next_keyframe

        keyframe.timestamp.timedelta = mark.timedelta
        keyframes.append(keyframe)
    kf.set_keyframes(keyframes)
