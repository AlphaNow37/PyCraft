
_no_attr = object()

class TempSetattr:
    """
    setattr a temporary value to an object
    obj = ...  # obj.attr -> value_a
    with TempSetattr(obj, "attr", value_b):
        ...  # obj.attr -> value_b
    ...  # obj.attr -> value_a

    """
    def __init__(self, obj, name, temp_value):
        self.obj = obj
        self.name = name
        self.temp_value = temp_value

    def __enter__(self):
        self.before_value = getattr(self.obj, self.name, _no_attr)
        setattr(self.obj, self.name, self.temp_value)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.before_value is _no_attr:
            delattr(self.obj, self.name)
        else:
            setattr(self.obj, self.name, self.before_value)


if __name__ == '__main__':
    a = type("_", (), {})()
    a.test = 11
    with TempSetattr(a, "test", 5):
        print(a.test)
    print(a.test)
