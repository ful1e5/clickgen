# About

## Goals

The author’s goal is to create the automatic cursor theme through:

- Continuous integration testing via [GitHub Actions](https://github.com/ful1e5/clickgen/actions)
- Publicized development activity on [GitHub](https://github.com/ful1e5/clickgen)
- Regular releases to the [Python Package Index](https://pypi.org/project/clickgen/)
- Standardize cursor theme build approach.

## License

clickgen is [licensed under the open source MIT License](https://github.com/ful1e5/clickgen/blob/main/LICENSE)

## Why a clickgen?

xcursorgen and anicursorgen.py both are non-standardized CLI tools for building cursor. It means you need both tools for creating a cross-platform compilable cursor theme. Both tools lacking some key functionality, When you want to create a **fully-functional** cursor/s.

**Missing functionality in `xcursorgen` & `anicursorgen.py` :**

- Require _config file_ to built **XCursor**/**CUR**/**ANI**
- Missing _packaging_ compatibility
- We've to interact through CLI.
