# jpkgchanger

Change java project package name easily with CLI tool `jpkgchanger`!

[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]
[![Code Coverage][coverage-image]][coverage-url]

## Install
```bash
pip install jpkgchanger
```

### Usage
To change package name for java project source code from `com.examole` to `com.another` 
run in the project root directory:
```bash
jpkgchanger --current com.example --target com.another
```

To ignore some folders or files you can use `--protected_dirs` or `--protected_files`
arguments:

```bash
jpkgchanger --current com.example --target com.another \ 
    --protected_dirs .git \ 
    --protected_files .gitignore \
    /
```

<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/jpkgchanger
[pypi-url]: https://pypi.org/project/jpkgchanger/
[build-image]: https://github.com/intermedia-net/jpkgchanger/actions/workflows/build.yml/badge.svg
[build-url]: https://github.com/intermedia-net/jpkgchanger/actions/workflows/build.yml
[coverage-image]: https://codecov.io/gh/intermedia-net/jpkgchanger/branch/main/graph/badge.svg
[coverage-url]: https://codecov.io/gh/intermedia-net/jpkgchanger
