from argparse import ArgumentParser
from dataclasses import dataclass
import os
import subprocess
from typing import List


class Ffmpeg:
    def __init__(self, binary_path: str) -> None:
        self.binary_path: str = binary_path

    def __exec(self, *args) -> None:
        subprocess.call(
            [self.binary_path, *args],
            stdout=open(os.devnull, "w"),
            stderr=subprocess.STDOUT,
        )

    def test(self) -> None:
        self.__exec("--help")

    def convert(self, input_path: str, output_path: str) -> None:
        self.__exec("-i", input_path, output_path)


@dataclass(frozen=True)
class Converter:
    root_input_path: str
    root_output_path: str
    output_extension: str
    dry_run: bool
    ffmpeg: Ffmpeg

    def compute_output_path(self, input_file_path: str) -> str:
        relative_file_path = os.path.relpath(
            path=input_file_path, start=self.root_input_path
        )
        output_file_path = os.path.join(self.root_output_path, relative_file_path)
        return f"{os.path.splitext(output_file_path)[0]}.{self.output_extension}"

    def process_file(self, directory_path: str, file_name: str):
        input_file_path: str = os.path.join(directory_path, file_name)
        output_file_path: str = self.compute_output_path(
            input_file_path=input_file_path
        )
        would_overwrite = os.path.exists(output_file_path)
        print(f" - Input:  {input_file_path}")
        print(f" {' !' if would_overwrite else ' '} Output: {output_file_path}")
        if not self.dry_run:
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            if would_overwrite:
                raise RuntimeError(f"Refusing to overwrite: '{output_file_path}'")
            self.ffmpeg.convert(
                input_path=input_file_path, output_path=output_file_path
            )

    def process_folder(self, directory_path: str, file_names: List[str]):
        print(f"Current folder: {directory_path}")
        for name in file_names:
            self.process_file(directory_path=directory_path, file_name=name)

    def run(self):
        self.ffmpeg.test()
        if not self.dry_run:
            os.makedirs(name=self.root_output_path, exist_ok=True)
        for step in os.walk(self.root_input_path):
            directory_path, subdirectory_names, file_names = step
            self.process_folder(directory_path=directory_path, file_names=file_names)


if __name__ == "__main__":
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

    converter = Converter(
        root_input_path=os.path.abspath(args.input),
        root_output_path=os.path.abspath(args.output),
        output_format=args.format,
        dry_run=args.dry_run,
        fmpeg=Ffmpeg(binary_path=args.binary),
    )
    converter.run()
