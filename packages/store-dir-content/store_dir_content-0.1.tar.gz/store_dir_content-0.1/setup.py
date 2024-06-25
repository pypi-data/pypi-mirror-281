from setuptools import find_packages, setup

setup(
    name="store_dir_content",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pathspec",
    ],
    entry_points={
        "console_scripts": [
            "store-dir-content=store_dir_content.cli:main",
        ],
    },
    author="Lukas Ramroth",
    author_email="",
    description="A CLI tool to read files and extract content based on extensions.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lukasramroth/store_dir_content",  # Update with your repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
