class destination(object):
    """coordinate format [galaxy, system, position, type]
       type1=planet; type2=debris; type3=moon"""
    planet = 1
    debris = 2
    moon = 3


def coordinates(galaxy, system, position, dest=destination.planet):
    return [galaxy, system, position, dest]


class ships(object):
    def light_fighter(self):
        return 'am204', self

    def heavy_fighter(self):
        return 'am205', self

    def cruiser(self):
        return 'am206', self

    def battleship(self):
        return 'am207', self

    def interceptor(self):
        return 'am215', self

    def bomber(self):
        return 'am211', self

    def destroyer(self):
        return 'am213', self

    def deathstar(self):
        return 'am214', self

    def reaper(self):
        return 'am218', self

    def explorer(self):
        return 'am219', self

    def small_transporter(self):
        return 'am202', self

    def large_transporter(self):
        return 'am203', self

    def colonyShip(self):
        return 'am208', self

    def recycler(self):
        return 'am209', self

    def espionage_probe(self):
        return 'am210', self


class mission(object):
    attack = 1
    transport = 3
    park = 4
    park_ally = 5
    spy = 6
    colonize = 7
    recycle = 8
    destroy = 9
    expedition = 15

class speed(object):
    _10 = 1
    _20 = 2
    _30 = 3
    _40 = 4
    _50 = 5
    _60 = 6
    _70 = 7
    _80 = 8
    _90 = 9
    _100 = 10
    max = 10
    min = 1
