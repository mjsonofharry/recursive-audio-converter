from argparse import ArgumentParser
import os
import subprocess


def test_ffmpeg(ffmpeg_binary_path: str):
    subprocess.call(
        [ffmpeg_binary_path, "--help"],
        stdout=open(os.devnull, "w"),
        stderr=subprocess.STDOUT,
    )


def run_ffmpeg(ffmpeg_binary_path: str, input_path: str, output_path: str):
    if os.path.exists(output_path):
        raise RuntimeError(
            f"Conversion would overwrite file at the following location: '{output_path}'"
        )
    subprocess.call(
        [ffmpeg_binary_path, "-i", input_path, output_path],
        stdout=open(os.devnull, "w"),
        stderr=subprocess.STDOUT,
    )


def compute_output_path(
    input_file_path: str,
    root_input_path: str,
    root_output_path: str,
    output_extension: str,
):
    relative_file_path = os.path.relpath(path=input_file_path, start=root_input_path)
    output_file_path = os.path.join(root_output_path, relative_file_path)
    return (
        input_file_path,
        f"{os.path.splitext(output_file_path)[0]}.{output_extension}",
    )


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-i", "--input", required=True, help="File system path to the input directory"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="File system path to the output directory"
    )
    parser.add_argument(
        "-f",
        "--format",
        required=True,
        help="File extension for conversion (run 'ffmpeg -formats' for a list of supported extensions)",
    )
    parser.add_argument(
        "-b",
        "--binary",
        required=True,
        help="File system path to FFmpeg executable (e.g. ffmpeg.exe)",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        required=False,
        help="Show a list of conversions without performing them",
        action="store_true",
    )
    args = parser.parse_args()

    root_input_path: str = os.path.abspath(args.input)
    root_output_path: str = os.path.abspath(args.output)
    output_format: str = args.format
    ffmpeg_binary_path: str = args.binary
    dry_run: bool = args.dry_run

    test_ffmpeg(ffmpeg_binary_path=ffmpeg_binary_path)

    if not dry_run:
        os.makedirs(name=root_output_path, exist_ok=True)

    for step in os.walk(root_input_path):
        directory_path, subdirectory_names, file_names = step
        if len(file_names) == 0:
            continue
        input_file_paths = [os.path.join(directory_path, name) for name in file_names]
        output_file_paths = [
            compute_output_path(
                input_file_path=file_path,
                root_input_path=root_input_path,
                root_output_path=root_output_path,
                output_extension=output_format,
            )
            for file_path in input_file_paths
        ]
        print(f"Current folder: {directory_path}")
        for input_path, output_path in output_file_paths:
            print(f" - Input:  '{input_path}'")
            print(f"   Output: '{output_path}'")
            print()
            if not dry_run:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                run_ffmpeg(
                    ffmpeg_binary_path=ffmpeg_binary_path,
                    input_path=input_path,
                    output_path=output_path,
                )


if __name__ == "__main__":
    main()
