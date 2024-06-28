# lib_version_group3

## Overview

`lib_version_group3` is a Python library designed to manage and retrieve software versions. This utility can be particularly useful for including verbose system information in logs, debugging, and ensuring compatibility in dependent systems.

## Features

- **Version Retrieval:** Provides an easy interface to retrieve the current version of the library.
- **Automated Versioning:** Integrates with Git version tags to automatically update the library version.
- **Simple Integration:** Can be easily incorporated into other Python projects to help manage version dependencies.

## Installation

Install `lib_version_group3` using pip:

```bash
pip install lib_version_group3
```

## Usage

To use the library, import and create an instance of `VersionUtil` and call the `get_version` method:

```python
from lib_version_group3.version import VersionUtil

version = VersionUtil.get_version()
print(f"The current library version is: {version}")
```

## Automated Build and Release Process

The library is automatically built and released through GitHub Actions. When a new tag is pushed to the repository, the GitHub workflow defined in `.github/workflows/python-package.yml` triggers, performing the following actions:

- Checks out the code.
- Sets up the Python environment.
- Installs dependencies.
- Runs linting and style checks.
- Builds the distribution.
- Publishes the package to PyPI, triggered only on release tags.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Support

If you have any questions or issues with `lib-version`, please open an issue on the project repository, and we will get back to you as soon as possible.