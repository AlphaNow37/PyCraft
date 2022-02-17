import pathlib

root_path = pathlib.Path(__file__).parent.parent / "code_src"


def search(string, path: pathlib.Path):
    for subpath in path.iterdir():
        if subpath.is_dir():
            yield from search(string, subpath)
        else:
            if subpath.suffix == ".py":
                text = subpath.read_text("UTF-8")
                if string in text:
                    lines = [i for i, line in enumerate(text.split("\n")) if string in line]
                    yield subpath, lines


def get_visualisation_search(string):
    results = list(search(string, root_path))
    paths = [str(a[0]).removeprefix(str(root_path)+"\\") for a in results]
    max_lenght: int = len(max(paths, key=len))
    for path, lines in search(string, root_path):
        path_str = str(path).removeprefix(str(root_path)+"\\")
        print(f"{path_str}{' '*(max_lenght-len(path_str))} at lines {' '.join(map(str, lines))}")

get_visualisation_search("\nimport ")
print()
get_visualisation_search("\nimport pygame")
