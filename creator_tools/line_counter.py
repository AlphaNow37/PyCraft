import pathlib
from collections import defaultdict


root = pathlib.Path(__file__).parent.parent / "code_src"


def fusion_dct(dct1, dct2):
    return {
        key: dct1.get(key, 0) + dct2.get(key, 0)
        for key in (set(dct1) | set(dct2))
    }


def line_counter(path: pathlib.Path):
    dct = defaultdict(lambda: 0)
    for sub_path in path.iterdir():
        if sub_path.is_file():
            if sub_path.suffix == ".py":
                dct["lines"] += sub_path.read_text("UTF-8").count("\n")
                dct["files"] += 1
        else:
            dct2 = line_counter(sub_path)
            dct = fusion_dct(dct, dct2)
    return dct

print(line_counter(root))
