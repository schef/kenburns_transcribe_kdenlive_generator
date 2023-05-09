#!/usr/bin/python3

from re import split
import sys
from datetime import datetime, timedelta

class TranscribeTimestamp:
    #M,-1,1,1,0,0:00:00.933250
    def __init__(self, line):
        self.line = line
        splited = self.line.strip().split(",")
        self.mark_type = splited[0]
        self.label = splited[3]
        self.timestamp = splited[5]

    def get_label(self):
        return self.label

    def get_timestamp(self):
        return self.timestamp

    def get_timedelta(self):
        t = datetime.strptime(self.timestamp, '%H:%M:%S.%f')
        return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)

    def get_kdenlive_timestamp(self):
        return str(self.get_timedelta())[:-3]

    def __repr__(self):
        return f"[{self.label}] {self.get_timedelta()}"

class TranscribeFile:
    def __init__(self, path):
        self.path = path

    def get_file_lines(self):
        with open(self.path, "r") as file:
            return file.readlines()

    def get_timestamps(self):
        timestamps = []
        lines = self.get_file_lines()
        for l in lines:
            if len(l) >= 2 and l[0] == "M" and l[1] == ",":
                timestamps.append(TranscribeTimestamp(l))
        return timestamps

if __name__ == "__main__":
    tf = TranscribeFile(sys.argv[1])
    timestamps = tf.get_timestamps()
    timestamp = timestamps[0]
