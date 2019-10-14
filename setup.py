# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
import os

here = os.path.abspath(os.path.dirname(__file__))

# Versioning
with open(os.path.join(here, 'stream_bitrate_stats', '__init__.py')) as version_file:
    version = eval(version_file.read().split("\n")[0].split("=")[1].strip())

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

try:
    import pypandoc
    long_description = pypandoc.convert_text(long_description, 'rst', format='md')
except ImportError:
    print("pypandoc module not found, could not convert Markdown to RST")

setup(
    name='stream_bitrate_stats',
    version=version,
    description='Calculate bitrate statistics using FFmpeg',
    long_description=long_description,
    url='https://github.com/slhck/ffmpeg-bitrate-stats',
    author='Werner Robitza',
    author_email='werner.robitza@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Video',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=[
        'numpy',
    ],
    packages=['stream_bitrate_stats'],
    entry_points={
        'console_scripts': [
            'stream_bitrate_stats=stream_bitrate_stats.__main__:main',
        ],
    },
)
