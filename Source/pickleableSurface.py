import pygame as pg

pgSurf = pg.surface.Surface

class PickleableSurface(pgSurf):
    def __init__(self, *arg,**kwarg):
        size = arg[0]

        # size given is not an iterable,  but the object of pgSurf itself
        if (isinstance(size, pgSurf)):
            pgSurf.__init__(self, size=size.get_size(), flags=size.get_flags())
            self.surface = self
            self.name='test'
            self.blit(size, (0, 0))

        else:
            pgSurf.__init__(self, *arg, **kwarg)
            self.surface = self
            self.name = 'test'

    def __getstate__(self):
        state = self.__dict__.copy()
        surface = state["surface"]

        _1 = pg.image.tostring(surface.copy(), "RGBA")
        _2 = surface.get_size()
        _3 = surface.get_flags()
        state["surface_string"] = (_1, _2, _3)
        return state

    def __setstate__(self, state):
        surface_string, size, flags = state["surface_string"]

        pgSurf.__init__(self, size=size, flags=flags)

        s=pg.image.fromstring(surface_string, size, "RGBA")
        state["surface"] =s;
        self.blit(s,(0,0));self.surface=self;
        self.__dict__.update(state)