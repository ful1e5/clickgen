# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

## [v2.2.3] - 25 May 2024

### What's New?

-   Clickgen now allows cursor bitmap re-canvasing by specifying size using the `cursor_size:canvas_size` format. See [changelog-05212024](https://github.com/ful1e5/clickgen/discussions/59#discussioncomment-9511166)

## [v2.2.2] - 24 April 2024

### Important Changes

-   Re-canvas all windows sizes to prevent blurry windows cursors f81ae4d2f4d63913f4ed60cdba351f74c5d9668b

### What's New?

-   Support python 3.12

### Changes

-   ci: exclude older python version(>3.10) on macOS runner

## [v2.2.1] - 02 March 2024

### Important Changes

-   aa9ea8a1102026d656c06ad28a40e9d781d9e124 Remove canvasing from lower resolution (>32px) in Windows Cursor

### Changes

-   ci: updated to `nodejs-20` in Github Actions

### Issue Fixes

-   Fixed python string template in Windows uninstallation script, reported on: https://github.com/ful1e5/clickgen/commit/4fbf21b1d04755c9a6bd2b77b5b69f9ad1c1b56b.

## [v2.2.0] - 21 December 2023

### Issues Fixes

-   Windows `install.inf` cursor registry in wrong order Fixed (more info https://github.com/ful1e5/Bibata_Cursor/issues/154)

## [v2.1.9] - 23 September 2023

### Issues Fixes

-   typo: Fixed typo in windows packaging registry `AppStarteng` -> `AppStarting`

## [v2.1.8] - 14 September 2023

### Changes

-   chore: `x11_name` is optional in cursor configs

### Issues Fixes

-   typo: Fixed typo in windows packaging registry `Unavailiable` -> `Unavailable`

## [v2.1.7] - 13 September 2023

### What's New?

-   Generate `install.inf` based on directory's cursor files dynamically.
    (Related to ful1e5/Bibata_Cursor#124, ful1e5/Bibata_Cursor#133)

### Changes

-   dev: include `clickgen.*` modules with `find` method in package

### Issues Fixes

-   Parse config files as `Path` in `configparser` module (Fixes ful1e5/Bibata_Cursor#143)

## [v2.1.6] - 01 September 2023

### Issues Fixes

-   Included `clickgen.libs` directory in distributing package #60

## [v2.1.5] - 31 August 2023

### Changes

-   ci: Use actions/checkout@v3
-   ci: Use `ubuntu-latest` in Linux Runner
-   ci: Use distributed local package from `dist/` directory for performing tests
-   ci: `test` operation renamed to `pytest`

### Issues Fixes

-   XCursor symlink generated in wrong directory bug fixed
-   Short parameter for `-v` added for `ctgen --version`

## [v2.1.4] - 29 August 2023

### Deprecation

-   In the `ctgen` configuration file, the `[config]` section no longer supports the `win_size` and `x11_sizes` options. Check [changelog-08172023](https://github.com/ful1e5/clickgen/discussions/59#discussioncomment-6747666)

### What's New?

-   Prettier Logs in `ctgen` CLI.
-   Change size of individual cursor assigning `win_sizes` and `x11_sizes` to individual cursor config in `ctgen` CLI
-   Support `.yaml` and `.json` manifest config files for `ctgen`
-   Support for `Python 3.11` has been added, along with test suites for it.

### Changes

-   Added 'attrs>=15.0.0' dependency for safely import `dataclass` class
-   Using `[build](https://pypa-build.readthedocs.io/en/stable/index.html)` instead of `wheel` for building pypi distributing packages
-   Updated ubuntu version in CI

## [v2.1.3] - 10 October 2022

### Changed

-   Fix blurry Windows Cursors ful1e5/Bibata_Cursor#119

## [v2.1.2] - 06 October 2022

### Changed

-   Fix distortion transparency in XCursors exports ful1e5/Bibata_Cursor#118

## [v2.1.1] - 30 August 2022

### Changed

-   Fix size argument type with **windows** platform in `ctgen` script

## [v2.1.0] - 19 August 2022

### Changed

-   Fixed sub modules error in `clickgen.*`

## [v2.0.0] - 16 August 2022

> **Warning**
> I removed all functionalities and modules from older versions in `v2.0.0`.

> **Warning**
> Docker Image support deprecated due to cross-platform compatibility.

### Added

-   Building logs added in `ctgen`
-   add: python 3.7 support
-   add: **Windows** and **macOS** support fixed #24
-   init: `cursor`, `configparser`, `packer`, `parser` and `writer` module
-   'Twitter' and 'Download' links added on PYPI page
-   Added cursor generator cli: `clickgen -h`
-   Added cursor theme generator cli: `ctgen -h` (supports config file)
-   Uninstall script added in Windows cursors theme.

### Changed

-   `KeyNotFound` Exception fixed while reading cursor configuration in `configparser` module
-   ctgen (cli): fixed platform assignment type in '-p/--platform' argument
-   windows-writer: fixed slow animation in `.ani` cursors (60jifs(1000ms) -> 2 jifs(33ms))
-   chore: updated template variables inside `packer.windows`
-   make: install all dependencies with `make install_deps` command
-   chore: directory renamed `examples` -> `samples`

## [v2.0.0-beta.2] - 09 July 2022

## [v2.0.0-beta.1] - 27 June 2022

## [v1.2.0] - 26 March 2022

### Added

-   python 3.10 support
-   `Makefile` at the project root added for development operations command
-   Generate `stubfiles` from `make stubgen` command
-   `make clean` command for cleaning clickgen cache
-   `make dev` command for development purpose
-   `make docs_gen` command for generating docs
-   Build `xcursorgen` with extra flags
-   `xcursorgen.c` formatted with tool **[indent](https://www.gnu.org/software/indent/)**
-   Linting & typing fixes inside `clickgen.builders`
-   `Linting`, `pip package caching`, and `stubgen` commands inside [workflows/app-publish.yml](./.github/workflows/app-publish.yml)
-   `ConfigFrame` typing added inside `WindowsCursor` class
-   `clickgen.builders` module docs init
-   docstring `param type` and `rtype` typing with **"or"** inside `Optional` and `Union`
-   `WindowsCursor` docstring init
-   `tests` module docstring init
-   use built-in typing inside `clickgen.*`
-   `from_bitmap` classmethod init inside `XCursor` class
-   `from_bitmap` classmethod init inside `WindowsCursor` class
-   GitHub Sponsorships added
-   feat: uninstall script added in `WindowsPackager` ful1e5/apple_cursor#79
-   feat: run `pip install` command according to make target (use for dev env setup)
-   chore: moved `package_data` config to `setup.cfg`
-   chore: removed `resample` parameter from `Bitmap.resize()`

### Changed

-   clean `xcursorgen` build cache automatically on `make` command
-   `CI` pip caching system key changed to `setup.py`
-   Proper typing inheritation inside `clickgen/core.pyi`
-   Linting & Typing fixed in `XCursor` Class `clickgen/builder.py`
-   `xcursorgen/makefile` renamed to `xcursorgen/Makefile`
-   WindowsCursor support `options` instead of `args`
-   clickgen pip dependencies _installation_ method changed inside [workflows/app-ci.yml](./.github/workflows/app-ci.yml)
-   Only `python3` syntax (removed `(object) inheritation`)
-   `clickgen.utils.timer` & `clickgen.utils.debug` removed
-   formatting inside `CHANGELOG.md`
-   CI: run ci on every branch push
-   refactor: init `setup.cfg`
-   lsp warning fixed in `tests` module
-   removed emoji from `README.md`
-   chore: compact `Makefile` with variables
-   coverage: assign default value of `data` parameter in `clickgen/util.py`
-   fix: updated donation link and fixed type warning in `setup.py`
-   refactor: source moved to `src/*` directory
-   chore: tox init
-   make-stubgen: generate type interface(.pyi) files without `MODULES` variable
-   refactor: `scripts` -> `src/clickgen/scripts`

## [v1.1.9] - 22 March 2021

### Added

-   Couple of **linting** problem fixes
-   **Bitmap** and **CursorsAlias** member access outside the context manager
-   Check `make` command in `setup.py`
-   Better typing experience
-   Configure readthedocs with `sphinx`
-   Added **docs** badge in `README.md`

### Changed

-   Fixed Pillow vulnerabilities by bumped it to `8.1.1`
-   python caching updated in `app-ci.yml`
-   `Literal` typing removed from `clickgen.util` & `clickgen.core`
-   Fixed #23 packaging issue of `XPackager`
-   Fixed #22 Inside `util.PNGProvider`

## [v1.1.8] - 24 January 2021

### Added

-   Code Coverage ~100%
-   The new CLI
-   New `XCursor` & `Windows Cursor` building approach
-   python `.pyi` static type file (stub file) init
-   X11 & Windows themes _packaging_ compatibility
-   **Semi-animated** theme supports for Windows & X11
-   `timer` & `debug` development utility init.

### Changed

-   Handle **Cursor config file** in `tmp` directory
-   Cursor's database in python `Dict` format
-   Vast changes in `clickgen` importing.
-   GitHub workflow with `matrix`
-   fixed #12

## [v1.1.7] - 5 October 2020

### Added

-   New Stable version **v1.1.7**
-   Archlinux/Manjaro installation docs
-   CLI usage in [README.md](./README.md)

### Changed

-   skip `Pillow` is already installed

## [v1.1.6] - 24 September 2020

### Changed

-   `vertical resize` wrong implementation fix (KDE Cursor) #13
-   Remove unnecessary cursors from `left_ptr`
-   Remove `./` from all **symbolic link** cursors
-   Untraced `pkginfo.in` file
-   Update `Pillow` to 7.2.0

### Added

-   clickgen **info** in [README.md](./README.md)

## [v1.1.5-beta] - 29 July 2020

### Changed

-   Typo fixed

## [1.1.4-beta] - 20 July 2020

### Added

-   **configsgen** - _a tool for automating cursor `configs` generation from images._
-   **build function** - _a shortcut functions for build a `cursor theme`._

### Changed

-   individual `logging` support
-   added more _logs_
-   fixed _built-in_ **conflicts**
-   `import` packages manner changed

## [v1.1.3-alpha] - 24 June 2020

-   docker image **publishing workflow** fixed

## [v1.1.2-alpha] - 23 June 2020

### Added

-   Docker image available on **Github Docker Registry**
-   `clickgen CLI` added with the pip package

### Changed

-   Remove default command-line arguments in `win.py` aka **anicursorgen**
-   Exited with an error if `exception` occurred.
-   Empty cursor theme `archive` generation **fixed**.

## [v1.1.1-alpha] - 12 June 2020

### Changed

-   Windows cursors extension `null` to `.ani` or `.cur` in linker module.
-   Restructure **test**
-   Logo **Alignment fix** in `README.md`
-   CI Pipeline
-   GitHub workflow name changed
-   badges in `README.md`

## [v1.1.0-alpha] - 9 June 2020

### Added

-   Initial release 🎊
-   Logo and badges
-   CI/CD Pipelines
-   **auto-install** `pip requirements`
-   `xcursorgen.so` file included in the packaging
-   auto-generated **symlinks** based on input configs
-   `.tar` archive & `directory` as out **package**.

[unreleased]: https://github.com/ful1e5/clickgen/compare/v2.2.3...main
[v2.2.3]: https://github.com/ful1e5/clickgen/compare/v2.2.2...v2.2.3
[v2.2.2]: https://github.com/ful1e5/clickgen/compare/v2.2.1...v2.2.2
[v2.2.1]: https://github.com/ful1e5/clickgen/compare/v2.2.0...v2.2.1
[v2.2.0]: https://github.com/ful1e5/clickgen/compare/v2.1.9...v2.2.0
[v2.1.9]: https://github.com/ful1e5/clickgen/compare/v2.1.8...v2.1.9
[v2.1.8]: https://github.com/ful1e5/clickgen/compare/v2.1.7...v2.1.8
[v2.1.7]: https://github.com/ful1e5/clickgen/compare/v2.1.6...v2.1.7
[v2.1.6]: https://github.com/ful1e5/clickgen/compare/v2.1.5...v2.1.6
[v2.1.5]: https://github.com/ful1e5/clickgen/compare/v2.1.4...v2.1.5
[v2.1.4]: https://github.com/ful1e5/clickgen/compare/v2.1.4...v2.1.3
[v2.1.3]: https://github.com/ful1e5/clickgen/compare/v2.1.3...v2.1.2
[v2.1.2]: https://github.com/ful1e5/clickgen/compare/v2.1.2...v2.1.1
[v2.1.1]: https://github.com/ful1e5/clickgen/compare/v2.1.1...v2.1.0
[v2.1.0]: https://github.com/ful1e5/clickgen/compare/v2.1.0...v2.0.0
[v2.0.0]: https://github.com/ful1e5/clickgen/compare/v2.0.0...v2.0.0-beta.2
[v2.0.0-beta.2]: https://github.com/ful1e5/clickgen/compare/v2.0.0-beta.2...v2.0.0-beta.1
[v2.0.0-beta.1]: https://github.com/ful1e5/clickgen/compare/v2.0.0-beta.1...v1.1.9
[v1.2.0]: https://github.com/ful1e5/clickgen/compare/v1.1.9...v1.2.0
[v1.1.9]: https://github.com/ful1e5/clickgen/compare/v1.1.8...v1.1.9
[v1.1.8]: https://github.com/ful1e5/clickgen/compare/v1.1.7...v1.1.8
[v1.1.7]: https://github.com/ful1e5/clickgen/compare/1.1.6...v1.1.7
[v1.1.6]: https://github.com/ful1e5/clickgen/compare/1.1.5-beta...1.1.6
[v1.1.5-beta]: https://github.com/ful1e5/clickgen/compare/1.1.4-alpha...1.1.5-beta
[v1.1.4-beta]: https://github.com/ful1e5/clickgen/compare/1.1.3-alpha...1.1.4-beta
[v1.1.3-alpha]: https://github.com/ful1e5/clickgen/compare/1.1.2-alpha...1.1.3-alpha
[v1.1.2-alpha]: https://github.com/ful1e5/clickgen/compare/1.1.1-alpha...1.1.2-alpha
[v1.1.1-alpha]: https://github.com/ful1e5/clickgen/compare/1.1.0-alpha...1.1.1-alpha
[v1.1.0-alpha]: https://github.com/ful1e5/clickgen/releases/tag/1.1.0-alpha
