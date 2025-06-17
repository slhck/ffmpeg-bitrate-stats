# Always prefer setuptools over distutils
import os

# To use a consistent encoding
from codecs import open

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Versioning
with open(os.path.join(here, "ffmpeg_bitrate_stats", "__init__.py")) as version_file:
    for line in version_file:
        if line.startswith("__version__"):
            version = eval(line.split(" = ")[1])
            break

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ffmpeg_bitrate_stats",
    version=version,
    description="Calculate bitrate statistics using FFmpeg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slhck/ffmpeg-bitrate-stats",
    author="Werner Robitza",
    author_email="werner.robitza@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "MIT",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    packages=["ffmpeg_bitrate_stats"],
    install_requires=["numpy", "pandas", "plotille"],
    include_package_data=True,
    package_data={
        "ffmpeg_bitrate_stats": ["py.typed"],
    },
    entry_points={
        "console_scripts": [
            "ffmpeg-bitrate-stats=ffmpeg_bitrate_stats.__main__:main",
        ],
    },
)
