import os


def get_root_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
