# FFmpeg Bitrate Stats

[![PyPI version](https://badge.fury.io/py/ffmpeg_bitrate_stats.svg)](https://badge.fury.io/py/ffmpeg_bitrate_stats)

Simple script for calculating bitrate statistics using FFmpeg.

Author: Werner Robitza <werner.robitza@gmail.com>

Contents:

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Output](#output)
- [License](#license)

------

## Requirements

- Python 3.6
- FFmpeg:
    - download a static build from [their website](http://ffmpeg.org/download.html)
    - put the `ffprobe` executable in your `$PATH`
- `pip3 install -r requirements.txt`

## Installation

    pip3 install ffmpeg_bitrate_stats

Or clone this repository, then run the tool with `python -m ffmpeg_bitrate_stats`

## Usage

The script outputs a bunch of bitrate statistics, including aggregations for pre-defined windows. These windows can either be time-based or GOP-based (for video streams). When choosing a time-based window, you can specify the size of the chunks in seconds.

Output is to STDOUT so you can redirect that to a file or another script.

See `ffmpeg_bitrate_stats -h`:

```
usage: ffmpeg_bitrate_stats [-h] [-n] [-v] [-s {video,audio}]
                               [-a {time,gop}] [-c CHUNK_SIZE]
                               [-of {json,csv}]
                               input

positional arguments:
  input                 input file

optional arguments:
  -h, --help            show this help message and exit
  -n, --dry-run         Do not run command, just show what would be done
                        (default: False)
  -v, --verbose         Show verbose output (default: False)
  -s {video,audio}, --stream-type {video,audio}
                        Stream type to analyze (default: video)
  -a {time,gop}, --aggregation {time,gop}
                        Window for aggregating statistics, either time-based
                        (per-second) or per GOP (default: time)
  -c CHUNK_SIZE, --chunk-size CHUNK_SIZE
                        Custom aggregation window size in seconds (default:
                        1.0)
  -of {json,csv}, --output-format {json,csv}
                        output in which format (default: json)
```

## Output

The output can be JSON, which includes individual fields for each chunk, or CSV, which repeats each line for each chunk. The CSV adheres to the “tidy” data concept, so it's a little redundant.

Rates are given in kilobit per second, using SI prefixes (i.e., kilo = 1000).

Explanation of the fields:

- `input_file`: Path to the input file
- `stream_type`: Type of stream used (video, audio)
- `avg_fps`: Average FPS (number of frames divided by duration)
- `num_frames`: Number of frames
- `avg_bitrate`: Average bitrate
- `avg_bitrate_over_chunks`: Average bitrate calculated over the chunks
- `max_bitrate`: Maximum bitrate calculated over the chunks
- `min_bitrate`: Minimum bitrate calculated over the chunks
- `max_bitrate_factor`: Relation between peak and average
- `bitrate_per_chunk`: Individual bitrates for each chunk
- `aggregation`: Type of aggregation used
- `chunk_size`: Size of the chunk (when aggregation is "time")
- `duration`: Total duration of the stream. It is the sum of all frame durations, where each frame's duration is either based on `duration_time` field in ffmpeg, or the difference between the current and previous frame's PTS.

JSON example:

```
➜ ffmpeg_bitrate_stats -a time -c 30 -of json BigBuckBunny.mp4
{
    "input_file": "BigBuckBunny.mp4",
    "stream_type": "video",
    "avg_fps": 60.002,
    "num_frames": 38072,
    "avg_bitrate": 8002.859,
    "avg_bitrate_over_chunks": 7849.263,
    "max_bitrate": 14565.117,
    "min_bitrate": 3876.533,
    "max_bitrate_factor": 1.82,
    "bitrate_per_chunk": [
        8960.89,
        8036.678,
        6099.959,
        4247.879,
        7276.979,
        5738.383,
        7740.339,
        7881.705,
        7572.594,
        8387.719,
        9634.343,
        9939.488,
        9365.104,
        5061.071,
        14565.117,
        9725.483,
        4573.873,
        7765.041,
        9796.135,
        12524.024,
        3876.533,
        3914.455
    ],
    "aggregation": "time",
    "chunk_size": 30.0,
    "duration": 634.517
}
```

CSV example:

```
➜  ffmpeg_bitrate_stats -a time -c 30 -of csv BigBuckBunny.mp4
input_file,chunk_index,stream_type,avg_fps,num_frames,avg_bitrate,avg_bitrate_over_chunks,max_bitrate,min_bitrate,max_bitrate_factor,bitrate_per_chunk,aggregation,chunk_size,duration
BigBuckBunny.mp4,0,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,8960.89,time,30.0,634.517
BigBuckBunny.mp4,1,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,8036.678,time,30.0,634.517
BigBuckBunny.mp4,2,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,6099.959,time,30.0,634.517
BigBuckBunny.mp4,3,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,4247.879,time,30.0,634.517
BigBuckBunny.mp4,4,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,7276.979,time,30.0,634.517
BigBuckBunny.mp4,5,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,5738.383,time,30.0,634.517
BigBuckBunny.mp4,6,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,7740.339,time,30.0,634.517
BigBuckBunny.mp4,7,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,7881.705,time,30.0,634.517
BigBuckBunny.mp4,8,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,7572.594,time,30.0,634.517
BigBuckBunny.mp4,9,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,8387.719,time,30.0,634.517
BigBuckBunny.mp4,10,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,9634.343,time,30.0,634.517
BigBuckBunny.mp4,11,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,9939.488,time,30.0,634.517
BigBuckBunny.mp4,12,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,9365.104,time,30.0,634.517
BigBuckBunny.mp4,13,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,5061.071,time,30.0,634.517
BigBuckBunny.mp4,14,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,14565.117,time,30.0,634.517
BigBuckBunny.mp4,15,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,9725.483,time,30.0,634.517
BigBuckBunny.mp4,16,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,4573.873,time,30.0,634.517
BigBuckBunny.mp4,17,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,7765.041,time,30.0,634.517
BigBuckBunny.mp4,18,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,9796.135,time,30.0,634.517
BigBuckBunny.mp4,19,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,12524.024,time,30.0,634.517
BigBuckBunny.mp4,20,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,3876.533,time,30.0,634.517
BigBuckBunny.mp4,21,video,60.002,38072,8002.859,7849.263,14565.117,3876.533,1.82,3914.455,time,30.0,634.517
```

## License

ffmpeg_bitrate_stats, Copyright (c) 2019 Werner Robitza

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
