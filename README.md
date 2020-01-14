# pyogame2
![picture](ogame.png)

OGame is a browser-based, money-management and space-war themed massively multiplayer online browser game with over 
two million accounts.

This lib is supposed to help write scripts and bots for your needs.
it supports ogame_version: `7.1.0`
version `7.1.0` `v7`

## install
<pre>
pip install pyogame2
</pre>
update
<pre>
pip uninstall pyogame2
pip install pyogame2
</pre>
dont want to wait for new updates download direct from the develop branch
<pre>
pip install git+https://github.com/PiecePaperCode/pyogame2.git@develop
</pre>

## Discord
[Join Discord](https://discord.gg/CeBDgnR)

## functions
### login
<pre>
from pyogame2 import OGame2
from pyogame2.constants import destination, coordinates, ships, mission, speed, buildings, status
 
empire = OGame2(UNI, USER, PASSWORD)
 
empire = OGame2(UNI, USER, PASSWORD, user_agent='NCSA_Mosaic/2.0 (Windows 3.1)') #optional
</pre>
 
### get attacked
<pre>
empire.get_attacked()                   returns bool 
</pre>

### get neutral
<pre>
empire.get_neutral()                    returns bool 
</pre>
 
### get planet id's
<pre>
empire.get_planet_ids()                 returns list 

empire.get_id_by_planet_name('name')    returns int

empire.get_planet_names()               returns list
</pre>

### get moon id's
<pre>
empire.get_moon_ids()                   returns list

**keep in mind to prefer planets id's moon id dont works on every get_function**
</pre>

### coordinates
<pre>
coordinates have the format [galaxy, system, position, destination]

destination is referred to planet moon or debris on that coordinate planet=1 debris=2 moon=3
for example [1,200,16,3] = galaxy=1, system=200, position=16, destination=3 for moon
with from pyogame2.constants import destination the process is much more readable.

when you dont give it an destination it will default to planet

                                        returns list
</pre>
```python
from pyogame2.constants import coordinates, destination
pos = coordinates(galaxy=1,
                  system=2,
                  position=12,
                  dest=destination.debris)

coordinates(1, 2, 12, destination.moon)
coordinates(1, 2, 12, destination.debris)
coordinates(1, 2, 12, destination.planet) or coordinates(1, 2, 12)
coordinates(1, 2) # for only use with get_galaxy
```
### get celestial coordinates
works with planet's and moon's
<pre>
empire.get_celestial_coordinates(id)    returns list
</pre>

### resources
<pre>
resources have the format [metal, crystal, deuterium]
darkmatter & energy are irrelevant, because you cant transport these.
It is used for transport and market functions

from pyogame2.constants import resources
res = resources(metal=1, crystal=2, deuterium=3)
[1, 2, 3]
</pre>

### get resources
<pre>
empire.get_resources(id)                returns class(object)

res = empire.get_resources(id)
res.resources
res.metal
res.crystal
res.deuterium
res.darkmatter
res.energy                              returns int
</pre>

### get supply
<pre>
empire.get_supply(id)                   returns class(object)

sup = empire.get_supply(id)

sup.metal_mine.level                    returns int
sup.metal_mine.is_possible              returns bool (possible to build)
sup.metal_mine.cost                     returns resources
sup.metal_mine.in_construction          returns bool

sup.crystal_mine
sup.deuterium_mine
sup.solar_plant
sup.fusion_plant 
sup.metal_storage
sup.crystal_storage
sup.deuterium_storage                   returns class(object)
</pre>

### get facilities
<pre>
empire.get_facilities(id)               returns class(object) 

fac = empire.get_facilities(id)
fac.robotics_factory
fac.shipyard
fac.research_laboratory
fac.alliance_depot
fac.missile_silo
fac.nanite_factory
fac.terraformer
fac.repair_dock
</pre>

### get moon facilities
<pre>
empire.get_moon_facilities(id)          returns class(object) 
</pre>

### get marketplace
<pre>
Use this function to get all offerings from the market.
resourses will be returned in the resourse's format
ships will be returned in the ship's format
</pre>
```python
for bid in empire.get_marketplace(id, page_nr):
    if bid.is_ships:
        print(bid.id, bid.offer, bid.price)
        print(ships.get_ship_name(bid.offer), ships.get_ship_amount(bid.offer))
    if bid.is_resources:
        print(bid.id, bid.offer, bid.price) 
    print(bid.is_possible)

>>>1234 (204, '508', 'shipyard') [0, '1500000', 0]
>>>light_fighter 508
>>>True
>>>1235 ['10000000', 0, 0] [0, '8000000', 0]
>>>False
```

### buy marketplace
<pre>
empire.buy_marketplace(bid.id, id)      returns bool
</pre>

### submit marketplace
<pre>
you can sell resources and ships. 
Note that you can sell one ship or one resources at at time.
run a for loop if you wanna stack offerings.
If the Market accepts your offer depends on your price and availability on your id_planet
</pre>
<pre>
empire.submit_marketplace(offer, 
                          price, 
                          id)           returns bool

empire.submit_marketplace(offer=resources(metal=100),
                          price=resources(crystal=50),
                          id=id


empire.submit_marketplace(offer=ships.large_transporter(10),
                          price=resources(crystal=96000),
                          id=id)
</pre>

### collect marketplace
<pre>
it will collect all your orders at once that are not collected yet buy & sell orders
</pre>
<pre>
empire.collect_marketplace()            returns bool
</pre>

### get traider
<pre>
empire.get_traider(id)                  returns Exception("function not implemented yet PLS contribute")
</pre>

### get research
<pre>
empire.get_research()                   returns class(object) 

res = empire.get_research()
res.energy
res.laser
res.ion
res.hyperspace
res.plasma
res.combustion_drive
res.impulse_drive
res.hyperspace_drive
res.espionage
res.computer
res.astrophysics
res.research_network
res.graviton
res.weapons
res.shielding
res.armor
</pre>

### get ships
<pre>
empire.get_ships(id)                    returns class(object) 

shi = empire.get_ships(id)
shi.light_fighter
shi.heavy_fighter
shi.cruiser
shi.battleship
shi.interceptor
shi.bomber
shi.destroyer
shi.deathstar
shi.reaper
shi.explorer
shi.small_transporter
shi.large_transporter
shi.colonyShip
shi.recycler
shi.espionage_probe
shi.solarSatellite
shi.crawler
</pre>

### get defences
<pre>
empire.get_defences(id)                 returns class(object) 

def = empire.get_defences(id)
def.rocket_launcher
def.laser_cannon_light
def.laser_cannon_heavy
def.gauss_cannon
def.ion_cannon
def.plasma_cannon
def.shield_dome_small
def.shield_dome_large
def.missile_interceptor
def.missile_interplanetary
</pre>

### get galaxy
<pre>
empire.get_galaxy(coordinates)          returns list of class(object)
</pre>
```python
for planet in empire.get_galaxy(coordinates(1, 23)):
    print(planet.list)                  #returns all infos as a list
    print(planet.planet_name, planet.coordinates, planet.player, planet.status, planet.moon)
    if planet.status == status.longinactive:
        #Farm Inactive
```        

### get ally
<pre>
empire.get_ally()                       returns string
</pre>

### get officers
<pre>
empire.get_officers()                   returns Exception("function not implemented yet PLS contribute")
</pre>

### get shop
<pre>
empire.get_shop()                       returns Exception("function not implemented yet PLS contribute")
</pre>

### get fleet
<pre>
empire.get_fleet()                      returns list of class(object)
</pre>

```python
for fleet in empire.get_fleet():
    if fleet.mission == mission.expedition:
        print(fleet.list)
        print(fleet.id, fleet.mission, fleet.returns, fleet.arrival, fleet.origin, fleet.destination)
```

### get phalanx
<pre>
empire.get_phalanx(id, coordinates)     returns list of class(object)
</pre>

```python
for fleet in empire.get_phalanx(moon_id, coordinates(2, 410, 7)):
    if fleet.mission == mission.expedition:
        print(fleet.list)
        print(fleet.id, fleet.mission, fleet.returns, fleet.arrival, fleet.origin, fleet.destination)
```

### send fleet
```python
from pyogame2.constants import coordinates, ships, mission, speed
empire.send_fleet(mission=mission.expedition,
                  id=id,
                  where=coordinates(1, 12, 16),
                  ships=[ships.small_transporter(1), ships.bomber(1)],
                  resources=[0, 0, 0],  # optional default no resources
                  speed=speed.max,      # optional default speed.max
                  holdingtime=2)        # optional default 0 will be needed by expeditions
```
<pre>                 
                                        returns bool
</pre>

### send message
<pre>
empire.send_message(player_id, msg)     returns None
</pre>


### build
Buildings
```python
from pyogame2.constants import buildings
empire.build(what=buildings.alliance_depot, 
             id=id)

buildings.metal_mine
buildings.crystal_mine
buildings.deuterium_mine
buildings.solar_plant
buildings.fusion_plant
buildings.solar_satellite(int)
buildings.crawler(int)
buildings.metal_storage
buildings.crystal_storage
buildings.deuterium_storage

buildings.robotics_factory
buildings.shipyard
buildings.research_laboratory
buildings.alliance_depot
buildings.missile_silo
buildings.nanite_factory
buildings.terraformer
buildings.repair_dock

empire.build(what=buildings.rocket_launcher(10), 
             id=id)

buildings.rocket_launcher(int)
buildings.laser_cannon_light(int)
buildings.laser_cannon_heavy(int)
buildings.gauss_cannon(int)
buildings.ion_cannon(int)
buildings.plasma_cannon(int)
buildings.shield_dome_small(int)
buildings.shield_dome_large(int)
buildings.missile_interceptor(int)
buildings.missile_interplanetary(int)

buildings.moon_base
buildings.sensor_phalanx
buildings.jump_gate
```
Ships
```python
from pyogame2.constants import ships
empire.build(what=ships.bomber(10), 
             id=id)

ships.light_fighter(int)
ships.heavy_fighter(int)
ships.cruiser(int)
ships.battleship(int)
ships.interceptor(int)
ships.bomber(int)
ships.destroyer(int)
ships.deathstar(int)
ships.reaper(int)
ships.explorer(int)
ships.small_transporter(int)
ships.large_transporter(int)
ships.colonyShip(int)
ships.recycler(int)
ships.espionage_probe(int)
```
<pre>                 
                                        returns None
</pre>

### research
```python
from pyogame2.constants import research
empire.research(what=research.energy, 
             id=id)

research.energy
research.laser
research.ion
research.hyperspace
research.plasma
research.combustion_drive
research.impulse_drive
research.hyperspace_drive
research.espionage
research.computer
research.astrophysics
research.research_network
research.graviton
research.weapons
research.shielding
research.armor
```
<pre>                 
                                        returns None
</pre>

### logout
<pre>                 
empire.logout()                         returns exit()
</pre>
