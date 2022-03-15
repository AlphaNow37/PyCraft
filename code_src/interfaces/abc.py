from .. import Game


class AbcInterface:
    """All the interfaces has this methods / attributes

    Une interface avec pause est une interface
     qui stoppe le jeu quand elle est ouverte
     -> menu, keys, ...

    != interface sans pause
    -> inventory, ...
    """
    paused: bool

    def __init__(self, game: Game):
        self.game: Game = game

    def tick(self):
        """Update the interface"""
        raise NotImplementedError

    def draw(self):
        """Draw the interface on the screen"""
        raise NotImplementedError

    def on_event(self, event):
        """Catch the events"""
        raise NotImplementedError

    def close(self):
        """When the interface close"""
        self.game.interface = None
