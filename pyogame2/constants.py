class destination(object):
    """coordinate format [galaxy, system, position, type]
       type1=planet; type2=debris; type3=moon"""
    planet = 1
    debris = 2
    moon = 3


def coordinates(galaxy, system, position, dest=destination.planet):
    return [galaxy, system, position, dest]


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


class buildings(object):
    metal_mine = 1, 1, 'supplies'
    crystal_mine = 2, 1, 'supplies'
    deuterium_mine = 3, 1, 'supplies'
    solar_plant = 4, 1, 'supplies'
    fusion_plant = 12, 1, 'supplies'
    def solar_satellite(self=1): return 212, self, 'supplies'
    def crawler(self=1): return 217, self, 'supplies'
    metal_storage = 22, 1, 'supplies'
    crystal_storage = 23, 1, 'supplies'
    deuterium_storage = 24, 1, 'supplies'

    robotics_factory = 14, 1, 'facilities'
    shipyard = 21, 1, 'facilities'
    research_laboratory = 31, 1, 'facilities'
    alliance_depot = 34, 1, 'facilities'
    missile_silo = 44, 1, 'facilities'
    nanite_factory = 15, 1, 'facilities'
    terraformer = 33, 1, 'facilities'
    repair_dock = 36, 1, 'facilities'

    def rocket_launcher(self=1): return 401, self, 'defenses'
    def laser_cannon_light(self=1): return 402, self, 'defenses'
    def laser_cannon_heavy(self=1): return 403, self, 'defenses'
    def gauss_cannon(self=1): return 404, self, 'defenses'
    def ion_cannon(self=1): return 405, self, 'defenses'
    def plasma_cannon(self=1): return 406, self, 'defenses'
    def shield_dome_small(self=1): return 407, self, 'defenses'
    def shield_dome_large(self=1): return 408, self, 'defenses'
    def missile_interceptor(self=1): return 502, self, 'defenses'
    def missile_interplanetary(self=1): return 503, self, 'defenses'

    moon_base = 41, 1, 'facilities'
    sensor_phalanx = 42, 1, 'facilities'
    jump_gate = 43, 1, 'facilities'


class research(object):
    energy = 113, 1, 'research'
    laser = 120, 1, 'research'
    ion = 121, 1, 'research'
    hyperspace = 114, 1, 'research'
    plasma = 122, 1, 'research'
    combustion_drive = 115, 1, 'research'
    impulse_drive = 117, 1, 'research'
    hyperspace_drive = 118, 1, 'research'
    espionage = 106, 1, 'research'
    computer = 108, 1, 'research'
    astrophysics = 124, 1, 'research'
    research_network = 123, 1, 'research'
    graviton = 199, 1, 'research'
    weapons = 109, 1, 'research'
    shielding = 110, 1, 'research'
    armor = 111, 1, 'research'


class ships(object):
    def light_fighter(self): return 204, self, 'shipyard'
    def heavy_fighter(self): return 205, self, 'shipyard'
    def cruiser(self): return 206, self, 'shipyard'
    def battleship(self): return 207, self, 'shipyard'
    def interceptor(self): return 215, self, 'shipyard'
    def bomber(self): return 211, self, 'shipyard'
    def destroyer(self): return 213, self, 'shipyard'
    def deathstar(self): return 214, self, 'shipyard'
    def reaper(self): return 218, self, 'shipyard'
    def explorer(self): return 219, self, 'shipyard'
    def small_transporter(self): return 202, self, 'shipyard'
    def large_transporter(self): return 203, self, 'shipyard'
    def colonyShip(self): return 208, self, 'shipyard'
    def recycler(self): return 209, self, 'shipyard'
    def espionage_probe(self): return 210, self, 'shipyard'

    def get_ship_name(ships):
        if ships[0] == 204: return 'light_fighter'
        if ships[0] == 205: return 'heavy_fighter'
        if ships[0] == 206: return 'cruiser'
        if ships[0] == 207: return 'battleship'
        if ships[0] == 215: return 'interceptor'
        if ships[0] == 211: return 'bomber'
        if ships[0] == 213: return 'destroyer'
        if ships[0] == 214: return 'deathstar'
        if ships[0] == 218: return 'reaper'
        if ships[0] == 219: return 'explorer'
        if ships[0] == 202: return 'small_transporter'
        if ships[0] == 203: return 'large_transporter'
        if ships[0] == 208: return 'colonyShip'
        if ships[0] == 209: return 'recycler'
        if ships[0] == 210: return 'espionage_probe'

    def get_ship_amount(ships):
        return ships[1]

def resources(metal=0, cristal=0, deuterium=0):
    return [metal, cristal, deuterium]
