import os


def get_root_path() -> str:
    return os.path.dirname(os.path.abspath(__file__))
