# pyogame2
![picture](ogame.png)

 OGame is a browser-based, money-management and space-war themed massively multiplayer online browser game with over 
 two million accounts.
 
 This lib is supposed to help write scripts and bots for your needs.
 it supports ogame_version: `7.1.0`
 
 ## functions
 ### login
 <pre>
 from __init__ import OGame2
 
 empire = OGame2(UNI, USER, PASSWORD)
 
 empire = OGame2(UNI, USER, PASSWORD, user_agent='NCSA_Mosaic/2.0 (Windows 3.1)') #optional
 </pre>
 
### get planet id's
<pre>
empire.get_planet_ids()                 returns list 

empire.get_id_by_planet_name('name')    returns int

empire.get_planet_names()               returns list
</pre>

### coordinates
<pre>
coordinates have the format [galaxy, system, position, destination]

destination is referred to planet moon or debris on that coordinate planet=1 debris=2 moon=3
for example [1,200,16,3] = galaxy=1, system=200, position=16, destination=3 for moon
with from constants import destination the process is much more readable.

when you dont give it an destination it will default to planet

                                        returns list
</pre>
```python
from constants import coordinates, destination
pos = coordinates(galaxy=1,
                  system=2,
                  position=12,
                  dest=destination.debris)

coordinates(1, 2, 12, destination.moon)
coordinates(1, 2, 12, destination.debris)
coordinates(1, 2, 12, destination.planet) or coordinates(1, 2, 12)
```


### get resources
<pre>
empire.get_resources(id)                returns class(object)

res = empire.get_resources(id)
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
sup.metal_mine
sup.crystal_mine
sup.deuterium_mine
sup.solar_plant
sup.fusion_plant 
sup.metal_storage
sup.crystal_storage
sup.deuterium_storage                   returns int
</pre>

### get facilities
<pre>
empire.get_facilities(id)               returns class(object) 
</pre>

### get marketplace
<pre>
empire.get_marketplace(id)              returns Exception("function not implemented yet PLS contribute")
</pre>

### get traider
<pre>
empire.get_traider(id)                  returns Exception("function not implemented yet PLS contribute")
</pre>

### get research
<pre>
empire.get_research()                   returns class(object) 
</pre>

### get ships
<pre>
empire.get_ships(id)                    returns class(object) 
</pre>

### get defences
<pre>
empire.get_defences(id)                 returns class(object) 
</pre>

### get galaxy
<pre>
empire.get_galaxy(coordinates)          returns list in list

galaxy = empire.get_galaxy(coordinates)
galaxy = [[player1, coordinates, planet_name], [player2, coordinates, planet_name]]
</pre>

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

### send message
<pre>
empire.send_message(player_id, msg)     returns None
</pre>

### send fleet
```python
from constants import coordinates, ships, mission, speed
empire.send_fleet(mission=mission.transport,
                  id=id,
                  where=coordinates(1, 12, 16),
                  ships=[ships.small_transporter(1), ships.bomber(1)],
                  resources=[0, 0, 0],  # optional default no resources
                  speed=speed.max)      # optional default speed.max
```
<pre>                 
                                        returns None
</pre>