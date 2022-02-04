import pathlib


root = pathlib.Path(__file__).parent.parent / "code_src"


def line_counter(path: pathlib.Path):
    line_count = 0
    file_count = 0
    for sub_path in path.iterdir():
        if sub_path.is_file():
            if sub_path.suffix == ".py":
                line_count += sub_path.read_text("UTF-8").count("\n")
                file_count += 1
        else:
            nb_lines, nb_files = line_counter(sub_path)
            line_count += nb_lines
            file_count += nb_files
    return line_count, file_count

print(line_counter(root))
print(dict.__len__({"1": 2}))
