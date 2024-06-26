[![Unit Tests](https://github.com/mediacatch/mediacatch/actions/workflows/test.yaml/badge.svg)](https://github.com/mediacatch/mediacatch/actions/workflows/test.yaml)
[![Quality Check](https://github.com/mediacatch/mediacatch/actions/workflows/check.yaml/badge.svg)](https://github.com/mediacatch/mediacatch/actions/workflows/check.yaml)
[![Publish](https://github.com/mediacatch/mediacatch/actions/workflows/publish.yaml/badge.svg)](https://github.com/mediacatch/mediacatch/actions/workflows/publish.yaml)

# MediaCatch

Python package for easily interfacing with MediaCatch APIs and data formats.

## Requirements

- Python >= 3.10
- MediaCatch API key (contact support@medicatch.io)

## Installation

Install with pip

```bash
pip install mediacatch
```

Or install from source

```bash
pip install git+ssh://git@github.com/mediacatch/mediacatch
```

Or install locally

```bash
git clone git@github.com:mediacatch/mediacatch.git
cd mediacatch
pip install -e .
```

## Getting Started

Firstly, add your MediaCatch API key to your environment variables

```bash
export MEDIACATCH_API_KEY=<your-api-key-here>
```

Then you can start using the command line interface

```bash
mediacatch --help
usage: mediacatch <command> [<args>]

MediaCatch CLI tool

positional arguments:
  {vision}    mediacatch command helpers
    vision    CLI tool to run inference with MediaCatch Vision API

options:
  -h, --help  show this help message and exit
```

Upload a file to MediaCatch vision API and get the results

```bash
mediacatch vision path/to/file ocr --save-result path/to/save/result.json
# or to see options
mediacatch vision --help
```
