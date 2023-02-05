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
import sys

from .__init__ import __version__ as version
from .bitrate_stats import BitrateStats
from .log import CustomLogFormatter

logger = logging.getLogger("ffmpeg-bitrate-stats")


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
        "-of",
        "--output-format",
        type=str,
        default="json",
        choices=["json", "csv"],
        help="output in which format",
    )

    cli_args = parser.parse_args()

    setup_logger(logging.DEBUG if cli_args.verbose else logging.INFO)

    br = BitrateStats(
        cli_args.input,
        cli_args.stream_type,
        cli_args.aggregation,
        cli_args.chunk_size,
        cli_args.dry_run,
    )
    br.calculate_statistics()
    br.print_statistics(cli_args.output_format)


if __name__ == "__main__":
    main()
