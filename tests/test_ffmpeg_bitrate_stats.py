#!/usr/bin/env pytest

import contextlib
import io
import json
import os
import sys
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ffmpeg_bitrate_stats import BitrateStats, run_command  # noqa: E402
from ffmpeg_bitrate_stats import bitrate_stats as bitrate_stats_module  # noqa: E402

test_files = {
    "test.mp4": {
        "params": [],
        "results": {
            "stream_type": "video",
            "avg_fps": 25.0,
            "num_frames": 25,
            "avg_bitrate": 58.944,
            "avg_bitrate_over_chunks": 61.4,
            "max_bitrate": 61.4,
            "min_bitrate": 61.4,
            "max_bitrate_factor": 1.042,
            "bitrate_per_chunk": [61.4],
            "aggregation": "time",
            "chunk_size": 1.0,
            "duration": 1.0,
        },
    },
    "without_timestamps.mp4": {
        "params": [],
        "results": {
            "stream_type": "video",
            "avg_fps": 25.0,
            "num_frames": 25,
            "avg_bitrate": 111.128,
            "avg_bitrate_over_chunks": 115.758,
            "max_bitrate": 115.758,
            "min_bitrate": 115.758,
            "max_bitrate_factor": 1.042,
            "bitrate_per_chunk": [115.758],
            "aggregation": "time",
            "chunk_size": 1.0,
            "duration": 1.0,
        },
    },
    "test_keyframes.mp4": {
        "params": ["-a", "gop"],
        "results": {
            "stream_type": "video",
            "avg_fps": 50.0,
            "num_frames": 5,
            "avg_bitrate": 14813.6,
            "avg_bitrate_over_chunks": 9258.5,
            "max_bitrate": 9258.5,
            "min_bitrate": 9258.5,
            "max_bitrate_factor": 0.625,
            "bitrate_per_chunk": [9258.5],
            "aggregation": "gop",
            "chunk_size": None,
            "duration": 0.1,
        },
    },
}


class TestBitrates:
    def test_output(self) -> None:
        """
        Simple test for CLI functionality
        """

        for test_filename, expected_output in test_files.items():
            test_file = os.path.abspath(
                os.path.join(os.path.dirname(__file__), test_filename)
            )

            stdout, _ = run_command(
                [
                    "python3",
                    "-m",
                    "ffmpeg_bitrate_stats",
                    test_file,
                    *expected_output["params"],
                ]
            )

            assert stdout is not None

            output = json.loads(stdout)

            assert test_filename in output["input_file"]

            del output["input_file"]

            assert output == expected_output["results"]

    def test_plot_fits_terminal(self) -> None:
        """
        The auto-detected plot must fit within the terminal without any line
        wrapping onto the next one (regression test for #17).
        """
        test_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "test.mp4"))
        br = BitrateStats(test_file, show_progress=False)
        br.calculate_statistics()

        for term_width, term_height in [(80, 24), (120, 40), (200, 50)]:
            with mock.patch.object(
                bitrate_stats_module,
                "get_terminal_size",
                return_value=(term_width, term_height),
            ):
                buf = io.StringIO()
                with contextlib.redirect_stderr(buf):
                    br.plot()  # auto-detect from the (mocked) terminal size

            lines = buf.getvalue().rstrip("\n").split("\n")
            assert max(len(line) for line in lines) <= term_width
            assert len(lines) <= term_height
