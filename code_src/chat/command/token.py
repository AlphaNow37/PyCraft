from .responses import CommandError


class OneValueToken:
    name = None
    no_json = True

    def __init__(self, value, base_value: str, json=None):
        if json and self.no_json:
            raise CommandError(f"token {base_value} has not attached data")
        self.json = json or {}
        self.base_value = base_value
        self.value = value
        assert self.assert_good(value)

    def __repr__(self):
        return f"T.{self.name}('{self.value}')"

    def __str__(self):
        return self.base_value

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __bool__(self):
        return bool(self)

    def assert_good(self, value):
        return True

    __match_args__ = ("value", )


class String(OneValueToken):
    name = "Str"

    def assert_good(self, value):
        return isinstance(value, str)


class SpecialString(String):
    name = "SS"


class Number(OneValueToken):
    name = "Nb"

    def assert_good(self, value):
        return isinstance(value, int | float)

class Percent(Number):
    name = "P%"


class BoolValue(OneValueToken):
    name = "Bo"

    def assert_good(self, value):
        return isinstance(value, bool)

class Block(OneValueToken):
    name = "Bl"
    no_json = False

    def __init__(self, value, base_value: str, json):
        value = list(value)
        super().__init__(value, base_value, json)
        if json:
            self.value[1] |= json

class RelativePosition(OneValueToken):
    name = "Pos"

    def assert_good(self, value):
        return isinstance(value, int | float)

class RelDirectionPosition(OneValueToken):
    name = "Dir"

    def assert_good(self, value):
        return isinstance(value, int | float)


none = object()
