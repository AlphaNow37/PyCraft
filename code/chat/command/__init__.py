import pathlib


from .executor import execute

command_path = pathlib.Path(__file__).parent / "commands"
files = [path.name for path in command_path.iterdir() if not path.name == "__pycache__"]
__import__("commands", level=1, fromlist=files, globals=globals())
