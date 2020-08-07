class GetterClass(object):
    def __init__(self, *args):
        if args:
            self._repr = " | ".join(args)
        else:
            self._repr = ""

    def __getitem__(self, name):
        return getattr(self, name)

    def __repr__(self):
        return "< " + self._repr + " >"
