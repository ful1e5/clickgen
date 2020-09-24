# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

### Changed

- `vertical resize` wrong implementation fix (KDE Cursor) #13
- Remove unnecessary cursors from `left_ptr`
- Remove `./` from all **symbolic link** cursors
- Untraced `pkginfo.in` file
- Update `Pillow` to 7.2.0

### Added

- clickgen **info** in README.md(./README.md)

## [1.1.5-beta] - 29 July 2020 (Current)

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

[unreleased]: https://github.com/ful1ie5/clickgen/compare/1.1.5-beta...master
[1.1.5-beta]: https://github.com/ful1ie5/clickgen/compare/1.1.4-alpha...1.1.5-beta
[1.1.4-beta]: https://github.com/ful1ie5/clickgen/compare/1.1.3-alpha...1.1.4-beta
[1.1.3-alpha]: https://github.com/ful1ie5/clickgen/compare/1.1.2-alpha...1.1.3-alpha
[1.1.2-alpha]: https://github.com/ful1ie5/clickgen/compare/1.1.1-alpha...1.1.2-alpha
[1.1.1-alpha]: https://github.com/kaiziqbal/clickgen/compare/1.1.0-alpha...1.1.1-alpha
[1.1.0-alpha]: https://github.com/kaiziqbal/clickgen/releases/tag/1.1.0-alpha
