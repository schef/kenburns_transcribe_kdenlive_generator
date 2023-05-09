#!/usr/bin/python3

import sys
import random
from transcribe_file import TranscribeFile
from kdenlive_file import KdenliveFile

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
    timestamps = tf.get_timestamps()
    positions = kf.get_transition_positions()
    transition_positions = []
    for timestamp in timestamps:
        position = random.choice(positions)
        if "I" in timestamp.get_label():
            position = None
        if random.choice([True, False]):
            if position is not None:
                position = kf.zoom_transition(1.5, position)
        if timestamp.get_label() in position_overrides.keys():
            position = positions[position_overrides[timestamp.get_label()]]

        if position is not None: 
            time = timestamp.get_kdenlive_timestamp()
            transition_positions.append(kf.generate_transition_position(time, position))
            print(f"{timestamp.get_kdenlive_timestamp()} -> {timestamp.get_label()} - {position}")
        else:
            print(f"{timestamp.get_kdenlive_timestamp()} -> {timestamp.get_label()} - IGNORED")
    kf.set_transition_positions(transition_positions)
