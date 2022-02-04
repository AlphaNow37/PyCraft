import pathlib


def clear_dir(path: pathlib.Path):
    for subpath in path.iterdir():
        if subpath.is_dir():
            clear_dir(subpath)
            subpath.rmdir()
        else:
            subpath.unlink()
