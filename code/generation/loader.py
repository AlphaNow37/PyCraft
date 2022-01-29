from . import Generator
import json
from functools import partial

def load_from_data(data_str: str) -> Generator:
    gen = Generator()
    data = json.loads(data_str)
    data = load_data(data, gen)
    gen.__dict__ = data
    print(data)
    return gen

def load_data(data, gen):
    match data:
        case {"type": "//partial//", "func": func_name, "args": args, "kwargs": kwargs}:
            return partial(load_data(func_name, gen), *args, **kwargs)
        case str(f_name) if f_name.startswith("[f]"):
            f_name: str
            f_name = f_name.removeprefix("[f]")
            func = statics_funcs.get(f_name)
            return func or getattr(gen, f_name)
        case [*_]:
            return [load_data(content, gen)for content in data]
        case {}:
            return {load_data(key, gen): load_data(value, gen) for (key, value) in data.items()}
        case _:
            return data


def get_data_from_gen(gen: Generator) -> str:
    gen_dict = gen.__dict__
    string = json.dumps(gen_dict, default=serialise_funcs)
    return string


def serialise_funcs(obj):
    if isinstance(obj, partial):
        return {
            "type": "//partial//",
            "func": serialise_funcs(obj.func),
            "args": obj.args,
            "kwargs": obj.keywords,
        }
    elif callable(obj):
        name = obj.__name__
        return "[f]"+name
    else:
        raise ValueError(obj)
statics_funcs = {
}
