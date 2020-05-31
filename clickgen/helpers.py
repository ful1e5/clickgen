from contextlib import contextmanager
import os
import shutil
import sys
import tempfile


def create_dir(path: str) -> None:
    """
        ⚡ Clickgen Helper Function ⚡
        
        Create a directory if not exists.
        'path' is an absolute or relative path to the directory to create.
    """

    isExists = os.path.exists(path)

    if (isExists == False):
        os.mkdir(path)


@contextmanager
def TemporaryDirectory():
    """
        ⚡ Clickgen Helper Function ⚡
        
        Work with Temporary Directory.
        Use this context with `with` syntax as following:
            
            with TemporaryDirectory() as temp_dir:
                ...
        
    """
    name = tempfile.mkdtemp()
    try:
        yield name
    finally:
        shutil.rmtree(name)


@contextmanager
def cd(path):
    """
        ⚡ Clickgen Helper Function ⚡
        
        Temporary change directory.
        Use this context with `with` syntax as following:

            with cd('/tmp'):
                ...
    """

    CWD = os.getcwd()

    os.chdir(path)
    try:
        yield
    except:
        print('Exception caught: %s' % sys.exc_info()[0])
    finally:
        os.chdir(CWD)


def symlink(target, link_name, overwrite=False):
    """
        ⚡ Clickgen Helper Function ⚡

        Create a symbolic link named 'link_name' pointing to 'target'.
        If link_name exists then FileExistsError is raised, unless 'overwrite=True'.
        When trying to overwrite a directory, IsADirectoryError is raised.
        
        ref => https://stackoverflow.com/a/55742015
    """

    if not overwrite:
        os.symlink(target, link_name)
        return

    link_dir = os.path.dirname(link_name)

    while True:
        temp_link_name = tempfile.mktemp(dir=link_dir)

        try:
            os.symlink(target, temp_link_name)
            break
        except FileExistsError:
            pass

    try:
        if os.path.isdir(link_name):
            raise IsADirectoryError(
                f"Cannot symlink over existing directory: '{link_name}'")
        os.replace(temp_link_name, link_name)
    except:
        if os.path.islink(temp_link_name):
            os.remove(temp_link_name)
        raise
