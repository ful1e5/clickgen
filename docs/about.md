# About

## Goals

The author’s goal is to build hustle free cursor theme through:

- Cross-Platform and Standardize cursor build approach without runtime dependencies.
- Continuous integration testing via [GitHub Actions](https://github.com/ful1e5/clickgen/actions)
- Publicized development activity on [GitHub](https://github.com/ful1e5/clickgen)
- Regular releases to the [Python Package Index](https://pypi.org/project/clickgen/)

## License

clickgen is [licensed under the open source MIT License](https://github.com/ful1e5/clickgen/blob/main/LICENSE)

## Why a clickgen?

xcursorgen and anicursorgen.py both are non-standardized CLI tools for building cursor. It means you need both tools for creating a cross-platform compilable cursor theme. Both tools lacking some key functionality, When you've limited amount of knowledge about cursor/s and it's types.

**Missing functionality in `xcursorgen` & `anicursorgen.py` :**

- Require _config file_ to built `XCursor`/`CUR`/`ANI`. (that takes ages for creating manually)
- You've to resize all cursor images individually, As we specified inside the config file.
- `xcursorgen` compiled binaries are hard to find on Cloud Images like **Amazon Linux 2**, Because it's dependents on smaller **runtime libraries**, Like *libpng* and *libxcursor*. So, We can't generate `XCursor` using web technologies.
- Missing _packaging_ compatibility.
- You've to interact through CLI / Write a script to automate the cursor building process.
- Finding and Calculating `hotspots` for each cursor's size is the next level of pain. (that's why there are a small number of cursor developers on [pling.com](https://www.pling.com/browse/cat/107/order/latest/) 🤫)