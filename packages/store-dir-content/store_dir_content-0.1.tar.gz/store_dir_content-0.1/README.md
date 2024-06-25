# store-dir-content

`store-dir-content` is a CLI tool to read files with specific extensions in multiple directories and write their contents to an output file. It supports ignoring specific folders and respecting `.gitignore` files.

## Features

- Read files with specified extensions from multiple directories
- Option to ignore specified folders
- Option to respect `.gitignore` files
- Outputs the contents to a single file with clear dividers between files

## Installation

To install `store-dir-content`, use `pip`:

```bash
pip install store-dir-content
```

## Usage

You can use `store-dir-content` from the command line:

```bash
store-dir-content [directories] [-e file_extensions] [-o output_file] [-i ignore_folders] [--respect_gitignore]
```

### Arguments

- `directories`: One or more directories to search for files.
- `-e, --file_extensions`: Comma-separated list of file extensions to include (default: `.txt`).
- `-o, --output_file`: Path of the output file where the results will be written (default: `output.txt`).
- `-i, --ignore_folders`: Comma-separated list of folder names to ignore.
- `--respect_gitignore`: Respect `.gitignore` files in the directories.

### Examples

#### Basic Usage

```bash
store-dir-content ./dir1 ./dir2
```

This command reads all `.txt` files in `./dir1` and `./dir2`, writing their relative paths and contents to `output.txt`.

#### Custom File Extensions and Output File

```bash
store-dir-content ./dir1 ./dir2 -e .txt,.md -o my_output.txt
```

This command reads all `.txt` and `.md` files in `./dir1` and `./dir2`, writing their relative paths and contents to `my_output.txt`.

#### Ignoring Specific Folders

```bash
store-dir-content ./dir1 ./dir2 -e .txt,.md -o my_output.txt -i folder1,folder2
```

This command reads all `.txt` and `.md` files in `./dir1` and `./dir2`, excluding any files in `folder1` and `folder2`, and writes their relative paths and contents to `my_output.txt`.

#### Respecting `.gitignore`

```bash
store-dir-content ./dir1 ./dir2 -e .txt,.md -o my_output.txt --respect_gitignore
```

This command reads all `.txt` and `.md` files in `./dir1` and `./dir2`, respecting the `.gitignore` rules, and writes their relative paths and contents to `my_output.txt`.

## Development

To contribute to `store-dir-content`, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/store-dir-content.git
    ```

2. Navigate to the project directory:

    ```bash
    cd store-dir-content
    ```

3. Install the package in editable mode with the development dependencies:

    ```bash
    pip install -e .[dev]
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
