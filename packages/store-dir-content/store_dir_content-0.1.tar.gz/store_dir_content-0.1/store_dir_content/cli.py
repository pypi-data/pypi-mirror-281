import argparse
import json
import os
from typing import List, TextIO

import pathspec


def read_files_in_directories(
    directories: List[str],
    file_extensions: str,
    output_file: str,
    ignore_folders: str,
    respect_gitignore: bool,
) -> None:
    """
    Reads files in the specified directories and writes their content to an output file.

    Args:
        directories (List[str]): A list of directory paths to read files from.
        file_extensions (str): A comma-separated string of file extensions to include. Use "." to include all files.
        output_file (str): The path to the output file where the content will be written.
        ignore_folders (str): A comma-separated string of folder names to ignore.
        respect_gitignore (bool): Whether to respect the .gitignore file in each directory.

    Returns:
        None
    """
    extensions: List[str] = file_extensions.split(",")
    ignore_folders_list: List[str] = ignore_folders.split(",") if ignore_folders else []
    with open(output_file, "w", encoding="utf-8") as out_file:
        for directory in directories:
            gitignore_spec = (
                load_gitignore_spec(directory) if respect_gitignore else None
            )
            for root, dirs, files in os.walk(directory):
                # Skip the directories that need to be ignored
                dirs[:] = [d for d in dirs if d not in ignore_folders_list]
                for file in files:
                    file_path: str = os.path.join(root, file)
                    if gitignore_spec and gitignore_spec.match_file(
                        os.path.relpath(file_path, directory)
                    ):
                        continue
                    if file_extensions == "." or any(
                        file.endswith(ext) for ext in extensions
                    ):
                        relative_path: str = os.path.relpath(file_path, directory)
                        out_file.write(f"##### START OF FILE: {relative_path} #####\n")
                        if file.endswith(".ipynb"):
                            extract_ipynb_content(file_path, out_file)
                        else:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content: str = f.read()
                                out_file.write(content + "\n")
                        out_file.write(f"##### END OF FILE: {relative_path} #####\n\n")


def extract_ipynb_content(file_path: str, out_file: TextIO) -> None:
    """
    Extracts the content from an IPython notebook file and writes it to the specified output file.

    Args:
        file_path (str): The path to the IPython notebook file.
        out_file (TextIO): The output file to write the extracted content to.

    Returns:
        None
    """
    with open(file_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)
        for cell in notebook.get("cells", []):
            if cell["cell_type"] in ("code", "markdown"):
                cell_content = "".join(cell.get("source", []))
                out_file.write(cell_content + "\n\n")


def load_gitignore_spec(directory: str):
    """
    Load the gitignore specification from the given directory.

    Args:
        directory (str): The directory path.

    Returns:
        pathspec.PathSpec or None: The gitignore specification as a pathspec.PathSpec object,
        or None if the .gitignore file does not exist in the directory.
    """
    gitignore_path = os.path.join(directory, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            return pathspec.PathSpec.from_lines("gitwildmatch", f)
    return None


def main() -> None:
    """
    Read files with specific extensions in directories and write their contents to an output file.

    Args:
        directories (List[str]): The directories to search for files.
        file_extensions (str): Comma-separated list of file extensions to include (default: .txt).
        output_file (str): The path of the output file where the results will be written (default: output.txt).
        ignore_folders (str): Comma-separated list of folder names to ignore (default: none).
        respect_gitignore (bool): Whether to respect .gitignore files in the directories.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Read files with specific extensions in directories and write their contents to an output file.",
    )
    parser.add_argument(
        "directories", type=str, nargs="+", help="The directories to search for files."
    )
    parser.add_argument(
        "-e",
        "--file_extensions",
        type=str,
        default=".txt",
        help="Comma-separated list of file extensions to include (default: .txt).",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        default="output.txt",
        help="The path of the output file where the results will be written (default: output.txt).",
    )
    parser.add_argument(
        "-i",
        "--ignore_folders",
        type=str,
        default="",
        help="Comma-separated list of folder names to ignore (default: none).",
    )
    parser.add_argument(
        "-g",
        "--respect_gitignore",
        action="store_true",
        help="Respect .gitignore files in the directories.",
    )

    args = parser.parse_args()

    read_files_in_directories(
        args.directories,
        args.file_extensions,
        args.output_file,
        args.ignore_folders,
        args.respect_gitignore,
    )


if __name__ == "__main__":
    main()
