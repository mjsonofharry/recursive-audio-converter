# recursive-audio-converter

This is a simple script that uses FFmpeg to recursively convert audio files. Give it the location of a music library along with a destination, and it will create a full mirror of that music library, preserving the folder structure.

## Setup

- Get the latest version of [Python 3](https://www.python.org/) (also available on the [Windows Store](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7))
- Get [FFmpeg](https://www.ffmpeg.org/) and put the executable somewhere on your system
- Refer to the usage instructions below

## Usage

```
usage: converter.py [-h] --input INPUT --output OUTPUT --input-format INPUT_FORMAT --output-format OUTPUT_FORMAT --binary BINARY [--extra-args EXTRA_ARGS]
                    --strategy {abort,skip,overwrite,ask} [--dry-run]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         File system path to the input directory
  --output OUTPUT       File system path to the output directory
  --input-format INPUT_FORMAT
                        Input file format, e.g. 'flac' (run 'ffmpeg -formats' for a list of supported extensions)
  --output-format OUTPUT_FORMAT
                        Output file format, e.g. 'mp3' (run 'ffmpeg -formats' for a list of supported extensions)
  --binary BINARY       File system path to FFmpeg executable, e.g. 'Downloads\ffmpeg.exe'
  --extra-args EXTRA_ARGS
                        Extra arguments to pass to FFmpeg
  --strategy {abort,skip,overwrite,ask}
  --dry-run             Show a list of planned conversions without performing them
```

## Example

Here is a command to convert `.\data\input\` from flac to mp3, outputting the results to `.\data\output\`:

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

And here are the results of running that command on a library:

```
data
├── input
│   └── deuteronomy
│       └── pure staircase
│           ├── cover.jpg
│           ├── deuteronomy - pure staircase - 01 establishing shot.flac
│           ├── deuteronomy - pure staircase - 02 late to pillow.flac
│           ├── deuteronomy - pure staircase - 03 staying in.flac
│           ├── deuteronomy - pure staircase - 04 starboarding.flac
│           ├── deuteronomy - pure staircase - 05 no vacations, please.flac
│           ├── deuteronomy - pure staircase - 06 pathway.flac
│           ├── deuteronomy - pure staircase - 07 rain curtain.flac
│           ├── deuteronomy - pure staircase - 08 in it.flac
│           ├── deuteronomy - pure staircase - 09 esteem.flac
│           ├── deuteronomy - pure staircase - 10 all hands.flac
│           ├── deuteronomy - pure staircase - 11 hopeful romantic.flac
│           └── deuteronomy - pure staircase - 12 clair de lune.flac
└── output
    └── deuteronomy
        └── pure staircase
            ├── deuteronomy - pure staircase - 01 establishing shot.mp3
            ├── deuteronomy - pure staircase - 02 late to pillow.mp3
            ├── deuteronomy - pure staircase - 03 staying in.mp3
            ├── deuteronomy - pure staircase - 04 starboarding.mp3
            ├── deuteronomy - pure staircase - 05 no vacations, please.mp3
            ├── deuteronomy - pure staircase - 06 pathway.mp3
            ├── deuteronomy - pure staircase - 07 rain curtain.mp3
            ├── deuteronomy - pure staircase - 08 in it.mp3
            ├── deuteronomy - pure staircase - 09 esteem.mp3
            ├── deuteronomy - pure staircase - 10 all hands.mp3
            ├── deuteronomy - pure staircase - 11 hopeful romantic.mp3
            └── deuteronomy - pure staircase - 12 clair de lune.mp3
```

The folder structure of `.\data\input\` is fully mirrored to `.\data\output\` with the all of the flac files converted. Note that the original library is untouched and all non-flac files are ignored.
