import os


class Helpers:
    def create_dir(path: str) -> None:
        isExists = os.path.exists(path)

        if (isExists == False):
            os.mkdir(path)
