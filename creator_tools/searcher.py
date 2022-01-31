import pathlib


path = pathlib.Path(__file__).parent.parent / "code"


def search(string, path: pathlib.Path):
    for subpath in path.iterdir():
        if subpath.is_dir():
            yield from search(string, subpath)
        else:
            if subpath.suffix == ".py" and string in subpath.read_text("UTF-8"):
                yield subpath


print(*search("cote", path), sep="\n")
