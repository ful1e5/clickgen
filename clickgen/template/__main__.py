import os
import shutil

basedir = os.path.abspath(os.path.dirname(__file__))
cursor_file_path = os.path.join(basedir, 'cursor.theme')
index_file_path = os.path.join(basedir, 'index.theme')


def create_dir(path: str) -> None:
    isExists = os.path.exists(path)

    if (isExists == False):
        os.mkdir(path)


def create_x11_template(dir: str, name: str, comment: str = '') -> None:

    abs_dir = os.path.abspath(dir)
    cursor_file_out_path = os.path.join(abs_dir, 'cursor.theme')
    index_file_out_path = os.path.join(abs_dir, 'index.theme')

    create_dir(dir)

    with open(cursor_file_path, 'r') as cursor_file:
        with open(cursor_file_out_path, 'w') as cursor_file_out:
            lines = cursor_file.readlines()

            for line in lines:
                cursor_file_out.write(line.replace('<Name>', name))

    with open(index_file_path, 'r') as index_file:
        with open(index_file_out_path, 'w') as index_file_out:
            lines = index_file.readlines()

            for line in lines:
                temp_line = line.replace('<Name>', name)
                temp_line = temp_line.replace('<Comment>',
                                              '%s cursor theme' % name)

                if (comment != ''):
                    temp_line = line.replace('<Comment>', comment)
                index_file_out.write(temp_line)
