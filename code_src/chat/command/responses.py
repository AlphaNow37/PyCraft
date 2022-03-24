
class Error(Exception):
    textcolor = "red"


class CommandError(Error):
    pass


class ParamsError(Error):
    pass


class Send(Exception):
    def __init__(self, error, name="Send", textcolor="white"):
        self.args = (error, )
        self.name = name
        self.textcolor = textcolor
