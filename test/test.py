import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from ffmpeg_bitrate_stats import __main__ as main
from ffmpeg_bitrate_stats.__main__ import run_command

test_files = {
    "test.mp4": {
        "stream_type": "video",
        "avg_fps": 26.042,
        "num_frames": 25,
        "avg_bitrate": 61.4,
        "avg_bitrate_over_chunks": 61.4,
        "max_bitrate": 61.4,
        "min_bitrate": 61.4,
        "max_bitrate_factor": 1.0,
        "bitrate_per_chunk": [61.4],
        "aggregation": "time",
        "chunk_size": 1.0,
        "duration": 0.96,
    },
    "without_timestamps.mp4": {
        "stream_type": "video",
        "avg_fps": 26.042,
        "num_frames": 25,
        "avg_bitrate": 115.758,
        "avg_bitrate_over_chunks": 115.758,
        "max_bitrate": 115.758,
        "min_bitrate": 115.758,
        "max_bitrate_factor": 1.0,
        "bitrate_per_chunk": [115.758],
        "aggregation": "time",
        "chunk_size": 1.0,
        "duration": 0.96,
    },
}


class TestBitrates:
    def test_output(self):
        """
        Simple test for CLI functionality
        """

        for test_filename, expected_output in test_files.items():
            test_file = os.path.abspath(
                os.path.join(os.path.dirname(__file__), test_filename)
            )

            stdout, _ = run_command(
                ["python3", "-m", "ffmpeg_bitrate_stats", test_file]
            )
            output = json.loads(stdout)

            assert test_filename in output["input_file"]

            del output["input_file"]

            assert output == expected_output
