# recursive-audio-converter
Simple script that uses FFmpeg to recursively convert audio files

## Setup

- Get the latest version of [Python 3](https://www.python.org/) (also available on the [Windows Store](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7))
- Get [FFmpeg](https://www.ffmpeg.org/) and put the executable somewhere on your system
- Refer to the usage instructions below

## Usage

```
usage: converter.py [-h] --input INPUT --output OUTPUT --input-format INPUT_FORMAT --output-format OUTPUT_FORMAT --binary BINARY --strategy {abort,skip,overwrite,ask} [--dry-run]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         File system path to the input directory
  --output OUTPUT       File system path to the output directory
  --input-format INPUT_FORMAT
                        Input file format, e.g. 'flac' (run 'ffmpeg -formats' for a list of supported extensions)
  --output-format OUTPUT_FORMAT
                        Output file format, e.g. 'mp3' (run 'ffmpeg -formats' for a list of supported extensions)
  --binary BINARY       File system path to FFmpeg executable, e.g. 'Downloads\ffmpeg.exe'
  --strategy {abort,skip,overwrite,ask}
  --dry-run             Show a list of planned conversions without performing them
```

## Example

```
python .\converter.py `
  --input .\data\input\ `
  --output .\data\output\ `
  --input-format flac `
  --output-format mp3 `
  --binary .\lib\bin\ffmpeg.exe `
  --strategy overwrite `
  --extra-args "-ab 320k -map_metadata 0 -id3v2_version 3"
```