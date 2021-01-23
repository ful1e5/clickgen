# `clickgen.util` Module

This module provides utility functions and classes, Which makes developer life easier.

<!-- Typing Constant -->

## `clickgen.util.LikePath`

Provide location `typing`.

<!-- Context Managers  -->

## `clickgen.util.chdir`

Temporary change `working` directory.

!!! Note
    Use inside `with` syntax.

### Args

directory ([`LikePath`](#likepath)): path to directory.

### Returns

`None`.

### Example

```python
>>> with clickgen.util.chdir("new"):
>>>   print(os.cwd())
>>> print(os.cwd())

/tmp/new/
/tmp/
```

<!-- Functions -->

## `clickgen.util.remove_util`

Remove this file, directory or symlink. If Path exits on filesystem.

!!! Warning
    Some times `remove_util` leaves directory fingerprints (An empty directory).

### Args

p ([`LikePath`](#likepath)): path to directory.

### Returns

`None`.

### Examples

```python
>>> remove_util("/tmp/new")
>>> remove_util(Path("/tmp/new"))
```

<!-- Classes -->

## `clickgen.util.PNGProvider`

Provide organized `.png` files.

### Attributes

bitmaps_dir (`pathlib.Path`): Hold `.png` files directory passed in `__init__`.

### `PNGProvider.__init__()`

#### Args

bitmaps_dir ([`LikePath`](#likepath)): path to directory where `.png` files are stored.

#### Returns

`None`.

#### Raises

- `FileNotFoundError`: If zero `.png` file found provided directory.

### `PNGProvider.get()`

Get `.png` file/s from key.
This method return file location in `pathlib.Path` instance.

Also, this method is not supported directory sync, Which means creating a new file or deleting a file not affect this method.

The only way to sync the directory is, By creating a new instance of the `PNGProvider` class.

#### Args

key (str): `.png` filename without extension.

#### Returns

- `pathlib.Path`: Only one .png file found in provided directory.

- `List[pathlib.Path]`: Multiple `.png` files are found in provided directory.
