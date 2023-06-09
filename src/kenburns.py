#!/usr/bin/python3

import sys
import random
from copy import deepcopy
from transcribe_file import TranscribeFile
from kdenlive_file import KdenliveFile
from keyframe_manipulator import KeyframeManipulator

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
    return next_keyframe

if __name__ == "__main__":
    tf = TranscribeFile(sys.argv[1])
    kf = KdenliveFile(sys.argv[2])
    marks = tf.get_marks()
    keyframes_positions = kf.get_keyframes()
    keyframes = []
    km = KeyframeManipulator(keyframes_positions[0].size)
    last_keyframe = None
    repeat_keyframe = False
    for mark in marks:

        if mark.label in position_overrides.keys():
            print("mark")
            repeat_keyframe = True
            next_keyframe = keyframes_positions[position_overrides[mark.label]]
            keyframe = deepcopy(next_keyframe)
        elif repeat_keyframe:
            print("repeat")
            repeat_keyframe = False
            next_keyframe = last_keyframe
            keyframe = deepcopy(next_keyframe)
            km.change_size(keyframe, 0.05)
        else: 
            print("random")
            next_keyframe = get_next_random_unique_keyframe(last_keyframe, keyframes_positions)
            keyframe = deepcopy(next_keyframe)

        last_keyframe = next_keyframe

        print(keyframe)
        keyframe.timestamp.timedelta = mark.timedelta
        keyframes.append(keyframe)
    kf.set_keyframes(keyframes)
