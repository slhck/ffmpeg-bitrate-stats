import importlib.metadata

from .bitrate_stats import BitrateStats, BitrateStatsSummary, run_command

__version__ = importlib.metadata.version("ffmpeg_bitrate_stats")

__all__ = ["BitrateStats", "BitrateStatsSummary", "run_command"]
