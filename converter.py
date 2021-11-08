from argparse import ArgumentParser
from enum import Enum
from dataclasses import dataclass
import os
import subprocess
from typing import List


class Strategy(Enum):
    ABORT = "abort"
    SKIP = "skip"
    OVERWRITE = "overwrite"
    ASK = "ask"


def yes_no_prompt(message: str) -> bool:
    while True:
        response: str = input(f"{message} [y/n] ")
        if response.lower() == "y":
            return True
        elif response.lower() == "n":
            return False


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

    def convert(self, input_path: str, output_path: str, extra_args: List[str]) -> None:
        self.__exec("-i", input_path, *extra_args, output_path)


@dataclass(frozen=True)
class Converter:
    root_input_path: str
    root_output_path: str
    input_format: str
    output_format: str
    ffmpeg: Ffmpeg
    extra_args: List[str]
    strategy: Strategy
    dry_run: bool

    def compute_output_path(self, input_file_path: str) -> str:
        relative_file_path = os.path.relpath(
            path=input_file_path, start=self.root_input_path
        )
        output_file_path = os.path.join(self.root_output_path, relative_file_path)
        return f"{os.path.splitext(output_file_path)[0]}.{self.output_format}"

    def should_convert(self, input_file_path: str, output_file_path: str):
        if self.dry_run:
            print("   Result: Dry run, no actions allowed")
            return False
        if not os.path.exists(input_file_path):
            print("   WARNING: Input file does not exist")
            return False
        if not input_file_path.endswith(f".{self.input_format}"):
            print("   WARNING: Input file has wrong extension")
            return False
        if os.path.exists(output_file_path):
            if self.strategy == Strategy.ABORT:
                raise RuntimeError(f"   Result: Refusing to overwrite, aborting")
            elif self.strategy == Strategy.SKIP:
                print(f"   Result: Refusing to overwrite, skipping")
                return False
            elif self.strategy == Strategy.OVERWRITE:
                print("   Result: overwriting output file")
                return True
            else:
                return yes_no_prompt("Overwrite?")
        return True

    def process_file(self, directory_path: str, file_name: str):
        if not file_name.endswith(f".{self.input_format}"):
            return
        input_file_path: str = os.path.join(directory_path, file_name)
        output_file_path: str = self.compute_output_path(
            input_file_path=input_file_path
        )
        print(f" - Input:  {input_file_path}")
        print(f"   Output: {output_file_path}")
        if self.should_convert(
            input_file_path=input_file_path, output_file_path=output_file_path
        ):
            assert not self.dry_run
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            if os.path.exists(output_file_path):
                assert self.strategy not in [Strategy.SKIP, Strategy.ABORT]
                os.remove(output_file_path)
            self.ffmpeg.convert(
                input_path=input_file_path, output_path=output_file_path, extra_args=self.extra_args
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
        "--input", required=True, help="File system path to the input directory"
    )
    parser.add_argument(
        "--output", required=True, help="File system path to the output directory"
    )
    parser.add_argument(
        "--input-format",
        required=True,
        help="Input file format, e.g. 'flac' (run 'ffmpeg -formats' for a list of supported extensions)",
    )
    parser.add_argument(
        "--output-format",
        required=True,
        help="Output file format, e.g. 'mp3' (run 'ffmpeg -formats' for a list of supported extensions)",
    )
    parser.add_argument(
        "--binary",
        required=True,
        help="File system path to FFmpeg executable, e.g. 'Downloads\\ffmpeg.exe'",
    )
    parser.add_argument(
        "--extra-args",
        required=False,
        default="",
        help="Extra arguments to pass to FFmpeg",
    )
    parser.add_argument(
        "--strategy",
        choices=[
            Strategy.ABORT.value,
            Strategy.SKIP.value,
            Strategy.OVERWRITE.value,
            Strategy.ASK.value,
        ],
        required=True,
        help="",
    )
    parser.add_argument(
        "--dry-run",
        required=False,
        help="Show a list of planned conversions without performing them",
        action="store_true",
    )
    args = parser.parse_args()

    converter = Converter(
        root_input_path=os.path.abspath(args.input),
        root_output_path=os.path.abspath(args.output),
        input_format=args.input_format,
        output_format=args.output_format,
        ffmpeg=Ffmpeg(binary_path=args.binary),
        extra_args=args.extra_args.split(" "),
        strategy=Strategy(args.strategy),
        dry_run=args.dry_run,
    )
    converter.run()
