# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

### Added

- `Makefile` at the project root added for development operations command
- Generate `stubfiles` from `make stubgen` command
- `make clean` command for cleaning clickgen cache
- `make dev` command for development purpose
- `make docs_gen` command for generating docs
- Build `xcursorgen` with extra flags
- `xcursorgen.c` formatted with tool **[indent](https://www.gnu.org/software/indent/)**
- Linting & typing fixes inside `clickgen.builders`
- `Linting`, `pip package caching`, and `stubgen` commands inside [workflows/app-publish.yml](./.github/workflows/app-publish.yml)
- `ConfigFrame` typing added inside `WindowsCursor` class
- `clickgen.builders` module docs init
- docstring `param type` and `rtype` typing with **"or"** inside `Optional` and `Union`
- `WindowsCursor` docstring init
- `tests` module docstring init
- use built-in typing inside `clickgen.*`
- `from_bitmap` classmethod init inside `XCursor` class
- `from_bitmap` classmethod init inside `WindowsCursor` class
- GitHub Sponsorships added
- feat: uninstall script added in `WindowsPackager` ful1e5/apple_cursor#79

### Changed

- clean `xcursorgen` build cache automatically on `make` command
- `CI` pip caching system key changed to `setup.py`
- Proper typing inheritation inside `clickgen/core.pyi`
- Linting & Typing fixed in `XCursor` Class `clickgen/builder.py`
- `xcursorgen/makefile` renamed to `xcursorgen/Makefile`
- WindowsCursor support `options` instead of `args`
- clickgen pip dependencies _installation_ method changed inside [workflows/app-ci.yml](./.github/workflows/app-ci.yml)
- Only `python3` syntax (removed `(object) inheritation`)
- `clickgen.utils.timer` & `clickgen.utils.debug` removed
- formatting inside `CHANGELOG.md`
- CI: run ci on every branch push
- refactor: init `setup.cfg`
- lsp warning fixed in `tests` module
- removed emoji from `README.md`

## [1.1.9] - 22 Mar 2021

### Added

- Couple of **linting** problem fixes
- **Bitmap** and **CursorsAlias** memember access outside the context manager
- Check `make` command in `setup.py`
- Better typing experience
- Configure readthedocs with `sphinx`
- Added **docs** badge in `README.md`

### Changed

- Fixed Pillow vulnerabilities by bumped it to `8.1.1`
- python caching updated in `app-ci.yml`
- `Literal` typing removed from `clickgen.util` & `clickgen.core`
- Fixed #23 packaging issue of `XPackager`
- Fixed #22 Inside `util.PNGProvider`

## [1.1.8] - 24 Jan 2021

### Added

- Code Coverage ~100%
- The new CLI
- New `XCursor` & `Windows Cursor` building approach
- python `.pyi` static type file (stub file) init
- X11 & Windows themes _packaging_ compatibility
- **Semi-animated** theme supports for Windows & X11
- `timer` & `debug` development utility init.

### Changed

- Handle **Cursor config file** in `tmp` directory
- Cursor's database in python `Dict` format
- Vast changes in `clickgen` importing.
- GitHub workflow with `matrix`
- fixed #12

## [1.1.7] - 5 Oct 2020

### Added

- New Stable version **v1.1.7**
- Archlinux/Manjaro installation docs
- CLI usage in [README.md](./README.md)

### Changed

- skip `Pillow` is already installed

## [1.1.6] - 24 Sept 2020

### Changed

- `vertical resize` wrong implementation fix (KDE Cursor) #13
- Remove unnecessary cursors from `left_ptr`
- Remove `./` from all **symbolic link** cursors
- Untraced `pkginfo.in` file
- Update `Pillow` to 7.2.0

### Added

- clickgen **info** in [README.md](./README.md)

## [1.1.5-beta] - 29 July 2020

### Changed

- Typo fixed

## [1.1.4-beta] - 20 July 2020

### Added

- **configsgen** - _a tool for automating cursor `configs` generation from images._
- **build function** - _a shortcut functions for build a `cursor theme`._

### Changed

- individual `logging` support
- added more _logs_
- fixed _built-in_ **conflicts**
- `import` packages manner changed

## [1.1.3-alpha] - 24 June 2020

- docker image **publishing workflow** fixed

## [1.1.2-alpha] - 23 June 2020

### Added

- Docker image available on **Github Docker Registry**
- `clickgen CLI` added with the pip package

### Changed

- Remove default command-line arguments in `win.py` aka **anicursorgen**
- Exited with an error if `exception` occurred.
- Empty cursor theme `archive` generation **fixed**.

## [1.1.1-alpha] - 12 June 2020

### Changed

- Windows cursors extension `null` to `.ani` or `.cur` in linker module.
- Restructure **test** 🧪
- Logo **Alignment fix** in `README.md`
- CI Pipeline
- GitHub workflow name changed
- badges in `README.md`

## [1.1.0-alpha] - 9 June 2020

### Added

- Initial release 🎊
- Logo and badges
- CI/CD Pipelines
- **auto-install** `pip requirements`
- `xcursorgen.so` file included in the packaging
- auto-generated **symlinks** based on input configs
- `.tar` archive & `directory` as out **package**.

<<<<<<< HEAD
[unreleased]: https://github.com/ful1e5/clickgen/compare/v1.1.8...main
=======
[unreleased]: https://github.com/ful1e5/clickgen/compare/v1.1.9...main
[1.1.9]: https://github.com/ful1e5/clickgen/compare/v1.1.8...v1.1.9
