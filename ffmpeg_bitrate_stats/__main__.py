#!/usr/bin/env python3
#
# Calculate bitrate stats from video
#
# Output is in kilobit per second unless specified otherwise.
#
# Author: Werner Robitza
# License: MIT

import argparse
import logging
import os
import sys
from typing import Tuple

from .__init__ import __version__ as version
from .bitrate_stats import BitrateStats
from .log import CustomLogFormatter

logger = logging.getLogger("ffmpeg-bitrate-stats")


def get_terminal_size() -> Tuple[int, int]:
    try:
        term_size = os.get_terminal_size()
        return (term_size.columns, term_size.lines)
    except OSError:
        return (80, 24)


def setup_logger(level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger("ffmpeg-bitrate-stats")
    logger.setLevel(level)

    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(level)

    ch.setFormatter(CustomLogFormatter())

    logger.addHandler(ch)

    return logger


def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="ffmpeg_bitrate_stats v" + version,
    )
    parser.add_argument("input", help="input file")

    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Do not run command, just show what would be done",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show verbose output"
    )

    parser.add_argument(
        "-s",
        "--stream-type",
        default="video",
        choices=["video", "audio"],
        help="Stream type to analyze",
    )

    parser.add_argument(
        "-a",
        "--aggregation",
        default="time",
        choices=["time", "gop"],
        help="Window for aggregating statistics, either time-based (per-second) or per GOP",
    )

    parser.add_argument(
        "-c",
        "--chunk-size",
        type=float,
        default=1.0,
        help="Custom aggregation window size in seconds",
    )

    parser.add_argument(
        "-r",
        "--read-length",
        type=int,
        default=None,
        help="Length of time to sample stream (in seconds)",
    )

    parser.add_argument(
        "-of",
        "--output-format",
        type=str,
        default="json",
        choices=["json", "csv"],
        help="output in which format",
    )

    parser.add_argument(
        "-p",
        "--plot",
        action="store_true",
        help="Plot the bitrate over time (to STDERR)",
    )

    parser.add_argument(
        "-pw",
        "--plot-width",
        type=int,
        default=max(get_terminal_size()[0] - 10, 10),
        help="Plot width",
    )
    parser.add_argument(
        "-ph",
        "--plot-height",
        type=int,
        default=max(get_terminal_size()[1] - 6, 10),
        help="Plot height",
    )

    cli_args = parser.parse_args()

    setup_logger(logging.DEBUG if cli_args.verbose else logging.INFO)

    br = BitrateStats(
        cli_args.input,
        stream_type=cli_args.stream_type,
        aggregation=cli_args.aggregation,
        chunk_size=cli_args.chunk_size,
        read_length=cli_args.read_length,
        dry_run=cli_args.dry_run,
    )
    br.calculate_statistics()
    br.print_statistics(cli_args.output_format)

    if cli_args.plot:
        br.plot(
            width=cli_args.plot_width,
            height=cli_args.plot_height,
        )


if __name__ == "__main__":
    main()
