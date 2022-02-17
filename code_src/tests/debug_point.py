from . import Test


class DebugPoint(Test):
    def point(self):
        globals().update(self.__dict__)
        ...  # set a point here
        ...
