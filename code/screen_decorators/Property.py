import operator
from functools import partialmethod, partial


def _default(*_, **__):
    raise NotImplementedError()


class Property:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.reset = partial(self.reset, self)
        self.reset()

    value: object
    reset = _default

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def not_bool(self):
        self.value = not self.value

    def _op(self, op, other):
        return op(self.value, other)

    for op_name in ["add", "sub", "mul", "truediv", "eq", "mod", "gt", "lt", "ge", "le"]:
        op_name = f"__{op_name}__"
        locals()[op_name] = partialmethod(_op, getattr(operator, op_name))

    def __rsub__(self, other):
        return other - self.value

    def _iop(self, op, other):
        self.value = op(self.value, other)
        return self

    for op_name in ["add", "sub", "mul", "truediv", "mod"]:
        op_name = f"__i{op_name}__"
        locals()[op_name] = partialmethod(_iop, getattr(operator, op_name))

    def _cast(self, caster, *args, **kwargs):
        return caster(self.value, *args, **kwargs)

    for caster in (int, str, bool, float, round):
        locals()[f"__{caster.__name__}__"] = partialmethod(_cast, caster)

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value!r})"
