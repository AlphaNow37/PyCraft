import re
from . import token
from ...generation import generation_blocks
from json import loads as json_loads, JSONDecodeError


regex_arguments = re.compile(r"""((?P<enter>["']).*(?P=enter))|([^ ]+)""")
regex_number = re.compile(r"-?[\d]*\.?[\d]")
regex_block = re.compile(r"(minecraft:|pycraft:)?(?P<name>[a-zA-Z_]+)")
regex_pos = re.compile(r"~[+-]?[0-9]*")
regex_rel_dir = re.compile(r"\^[+-]?[0-9]*")
regex_json = re.compile(r"(?P<arg>.+)(?P<json>{.*})")
bools = {
    "no": False,
    "false": False,
    "yes": True,
    "true": True,
}
nones = ["/", "-", "..."]

def lex_parse(input_str: str):
    args = []
    for a, _, b in regex_arguments.findall(input_str):
        if a:
            base_arg = a
            a: str = a.strip("\'\"")
            args.append(token.SpecialString(a, base_arg))
            continue

        arg: str = b
        json = None
        if res := regex_json.fullmatch(arg):
            dct_args = res.groupdict()
            json_str = dct_args["json"]
            try:
                json = json_loads(json_str)
            except JSONDecodeError:
                pass
            else:
                arg = dct_args["arg"]
        if regex_number.fullmatch(arg):
            args.append(token.Number(float(arg), arg))
            continue
        elif regex_number.fullmatch(arg.removesuffix("%")):
            args.append(token.Percent(float(arg.removesuffix("%")), arg))
            continue
        elif arg.lower() in bools:
            args.append(token.BoolValue(bools[arg], arg))
            continue
        elif arg in nones:
            args.append(token.none)
            continue
        elif res := regex_block.fullmatch(arg):
            name = res.groupdict()["name"]
            if block := generation_blocks.BLOCKS.get(name.upper()):
                args.append(token.Block(block, arg, json))
                continue
        elif regex_pos.fullmatch(arg):
            if arg == "~":
                nb = 0
            else:
                nb = float(arg.strip("~+"))
            args.append(token.RelativePosition(nb, arg))
            continue
        elif regex_rel_dir.fullmatch(arg):
            if arg == "^":
                nb = 0
            else:
                nb = float(arg.strip("^+"))
            args.append(token.RelDirectionPosition(nb, arg))
            continue

        args.append(token.String(arg.lower(), arg))
    return args
