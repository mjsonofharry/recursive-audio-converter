# recursive-audio-converter
Simple script that uses FFmpeg to recursively convert audio files

## Setup

- Get the latest version of [Python 3](https://www.python.org/) (also available on the [Windows Store](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7))
- Get [FFmpeg](https://www.ffmpeg.org/) and put the executable somewhere on your system
- Refer to the usage instructions below

## Usage

```
usage: converter.py [-h] -i INPUT -o OUTPUT -f FORMAT -b BINARY [-d]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        File system path to the input directory
  -o OUTPUT, --output OUTPUT
                        File system path to the output directory
  -f FORMAT, --format FORMAT
                        File extension for conversion (run 'ffmpeg -formats' for a list of supported extensions)
  -b BINARY, --binary BINARY
                        File system path to FFmpeg executable (e.g. ffmpeg.exe)
  -d, --dry-run         Show a list of conversions without performing them
```