
class Error(Exception):
    pass


class CommandError(Error):
    pass


class ParamsError(Error):
    pass


class Send(Exception):
    def __init__(self, error, name="Send"):
        self.args = (error, )
        self.name = name
