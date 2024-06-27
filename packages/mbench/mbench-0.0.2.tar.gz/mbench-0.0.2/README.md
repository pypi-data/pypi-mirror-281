# mbodied-data

[![PyPI - Version](https://img.shields.io/pypi/v/mbodied-data.svg)](https://pypi.org/project/mbodied-data)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mbodied-data.svg)](https://pypi.org/project/mbodied-data)

-----

## Table of Contents

- [mbodied-data](#mbodied-data)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## Installation

```console
pip install mbench
```

## Usage

```python
from mbench import profileme
profileme()

def some_function():
    print("Hello")

```

```console
Hello
Function: some_function
  Duration: 0.000706 seconds
  CPU time: 0.000668 seconds
  Memory usage: 2.80 MB
  GPU usage: 0.00 MB
  I/O usage: 0.00 MB
  Avg Duration: 0.000527 seconds
  Avg CPU time: 0.000521 seconds
  Avg Memory usage: 0.35 MB
  Avg GPU usage: 0.00 MB
  Avg I/O usage: 0.00 MB
  Total calls: 8
-----------------------------
Profiling data saved to profiling_data.csv
```

## License

`mbench` is distributed under the terms of the [MIT License](LICENSE).
