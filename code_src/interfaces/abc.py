

class AbcInterface:
    """All the interfaces has this methods / attributes

    Une interface avec pause est une interface
     qui stoppe le jeu quand elle est ouverte
     -> menu, keys, ...

    != interface sans pause
    -> inventory, ...
    """
    paused: bool

    def tick(self):
        """Update the interface"""
        raise NotImplemented

    def draw(self):
        """Draw the interface on the screen"""
        raise NotImplemented

    def on_event(self, event):
        """Catch the events"""
        raise NotImplemented
