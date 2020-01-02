import re
import requests
import constants as const


class OGame2(object):
    def __init__(self, universe, username, password, user_agent=None):
        self.universe = universe
        self.username = username
        self.password = password
        self.chat_token = None
        self.sendfleet_token = None
        self.build_token = None
        self.session = requests.Session()
        self.server_id = None
        self.server_number = None
        self.server_language = None
        if user_agent is None:
            user_agent = {
                'User-Agent':
                    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/79.0.3945.88 Mobile Safari/537.36'}
        self.session.headers.update(user_agent)

        OGame2.login(self)
        OGame2.get_init_chatroken(self)

    def login(self):
        form_data = {'kid': '',
                     'language': 'en',
                     'autologin': 'false',
                     'credentials[email]': self.username,
                     'credentials[password]': self.password}
        logged = self.session.post('https://lobby.ogame.gameforge.com/api/users', data=form_data)
        servers = self.session.get('https://lobby.ogame.gameforge.com/api/servers').json()
        for server in servers:
            if server['name'] == self.universe:
                self.server_number = server['number']
                break
        accounts = self.session.get('https://lobby.ogame.gameforge.com/api/users/me/accounts').json()
        for account in accounts:
            if account['server']['number'] == self.server_number:
                self.server_id = account['id']
                self.server_language = account['server']['language']
        login_link = self.session.get('https://lobby.ogame.gameforge.com/api/users/me/loginLink?'
                                      'id={}'
                                      '&server[language]={}'
                                      '&server[number]={}'
                                      '&clickedButton=account_list'.format(self.server_id,
                                                                           self.server_language,
                                                                           self.server_number)).json()
        self.session.content = self.session.get(login_link['url']).text

    def get_init_chatroken(self):
        marker_string = 'var ajaxChatToken = '
        for re_obj in re.finditer(marker_string, self.session.content):
            self.chat_token = self.session.content[re_obj.start() + len(marker_string): re_obj.end() + 35].split('"')[1]

    def get_init_sendfleetroken(self, content):
        marker_string = 'var fleetSendingToken = '
        for re_obj in re.finditer(marker_string, content):
            self.sendfleet_token = content[re_obj.start() + len(marker_string): re_obj.end() + 35].split('"')[1]

    def get_init_build_token(self, content, component):
        marker_string = 'component={}&modus=1&token='.format(component)
        for re_obj in re.finditer(marker_string, content):
            self.build_token = content[re_obj.start() + len(marker_string): re_obj.end() + 32]

    def get_attacked(self):
        attack = 'tooltip eventToggle soon'
        no_attack = 'tooltip noAttack'
        if attack in self.session.content:
            return True
        elif no_attack in self.session.content:
            return False

    def get_planet_ids(self):
        planet_ids = []
        marker_string = 'id="planet-'
        for planet_id in re.finditer(marker_string, self.session.content):
            id = self.session.content[planet_id.start() + 11:planet_id.end() + 8]
            planet_ids.append(int(id))
        return planet_ids

    def get_planet_names(self):
        planet_names = []
        marker_string = 'planet-name ">'
        for i, planet_name in enumerate(re.finditer(marker_string, self.session.content)):
            planet_name = self.session.content[planet_name.start() + 14:planet_name.end() + 20].split('<')[0]
            planet_names.append(planet_name)
        return planet_names

    def get_id_by_planet_name(self, name):
        planet_id = None
        marker_string = 'planet-name ">'
        for i, planet_name in enumerate(re.finditer(marker_string, self.session.content)):
            planet_name = self.session.content[planet_name.start() + 14:planet_name.end() + len(name)]
            if planet_name == name:
                planet_id = OGame2.get_planet_ids(self)[i]
                break
        return planet_id

    def get_moon_ids(self):
        moon_ids = []
        marker_string = 'data-jumpgateLevel'
        for planet_id in re.finditer(marker_string, self.session.content):
            id = self.session.content[planet_id.start() - 41:planet_id.end() - 51]
            moon_ids.append(int(id))
        return moon_ids

    def get_celestial_coordinates(self, id):
        galaxy = None
        system = None
        position = None
        destination = None
        marker_string = 'component=galaxy&amp;cp={}'.format(id)
        for coordinates in re.finditer(marker_string, self.session.content):
            raw_coordinates = self.session.content[coordinates.start() + 37:coordinates.end() + 50]
            coordinates = raw_coordinates.replace('&amp', '').split('&')[0].split(';')
            galaxy = int(coordinates[0].replace('galaxy=', ''))
            system = int(coordinates[1].replace('system=', ''))
            position = int(coordinates[2].replace('position=', ''))
        if id in OGame2.get_planet_ids(self):
            destination = const.destination.planet
        elif id in OGame2.get_moon_ids(self):
            destination = const.destination.moon
        return [galaxy, system, position, destination]

    def get_resources(self, id):
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                    'component=overview&cp={}'
                                    .format(self.server_number, self.server_language, id)).text
        marker_string = '<span id="{}" data-raw="'

        class resources(object):
            for re_obj in re.finditer(marker_string.format('resources_metal'), response):
                metal = response[re_obj.start() + 37: re_obj.end() + 20].split('"')[0].split('.')[0]
            for re_obj in re.finditer(marker_string.format('resources_crystal'), response):
                crystal = response[re_obj.start() + 39: re_obj.end() + 20].split('"')[0].split('.')[0]
            for re_obj in re.finditer(marker_string.format('resources_deuterium'), response):
                deuterium = response[re_obj.start() + 41: re_obj.end() + 20].split('"')[0].split('.')[0]
            for re_obj in re.finditer(marker_string.format('resources_darkmatter'), response):
                darkmatter = response[re_obj.start() + 42: re_obj.end() + 20].split('"')[0].split('.')[0]
            for re_obj in re.finditer(marker_string.format('resources_energy'), response):
                energy = response[re_obj.start() + 38: re_obj.end() + 20].split('"')[0].split('.')[0]
            resources = [metal, crystal, deuterium]

        return resources

    def get_supply(self, id):
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                    'component=supplies&cp={}'
                                    .format(self.server_number, self.server_language, id)).text
        marker_string = '''class="level"
                  data-value="'''

        class supply_buildings(object):
            supply_buildings = []
            for re_obj in re.finditer(marker_string.format(marker_string), response):
                supply_buildings.append(int(response[re_obj.start() + len(marker_string):
                                                     re_obj.end() + 3].split('"')[0]))
            metal_mine = supply_buildings[0]
            crystal_mine = supply_buildings[1]
            deuterium_mine = supply_buildings[2]
            solar_plant = supply_buildings[3]
            fusion_plant = supply_buildings[4]
            metal_storage = supply_buildings[5]
            crystal_storage = supply_buildings[6]
            deuterium_storage = supply_buildings[7]

        return supply_buildings

    def get_facilities(self, id):
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                    'component=facilities&cp={}'
                                    .format(self.server_number, self.server_language, id)).text
        marker_string = '''class="level"
                  data-value="'''

        class facilities_buildings(object):
            facilities_buildings = []
            for re_obj in re.finditer(marker_string.format(marker_string), response):
                facilities_buildings.append(int(response[re_obj.start() + len(marker_string):
                                                         re_obj.end() + 3].split('"')[0]))
            robotics_factory = facilities_buildings[0]
            shipyard = facilities_buildings[1]
            research_laboratory = facilities_buildings[2]
            alliance_depot = facilities_buildings[3]
            missile_silo = facilities_buildings[4]
            nanite_factory = facilities_buildings[5]
            terraformer = facilities_buildings[6]
            repair_dock = facilities_buildings[7]

        return facilities_buildings

    def get_moon_facilities(self, id):
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                    'component=facilities&cp={}'
                                    .format(self.server_number, self.server_language, id)).text
        marker_string = '''class="level"
                  data-value="'''

        class moon_facilities_buildings(object):
            facilities_buildings = []
            for re_obj in re.finditer(marker_string.format(marker_string), response):
                facilities_buildings.append(int(response[re_obj.start() + len(marker_string):
                                                         re_obj.end() + 3].split('"')[0]))
            robotics_factory = facilities_buildings[0]
            shipyard = facilities_buildings[1]
            moon_base = facilities_buildings[2]
            sensor_phalanx = facilities_buildings[3]
            jump_gate = facilities_buildings[4]

        return moon_facilities_buildings

    def get_marketplace(self, id, page):
        biddings = []
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&' \
                                    'component=marketplace&tab=buying&action=fetchBuyingItems&ajax=1&'
                                    'pagination%5Bpage%5D={}&cp={}' \
                                    .format(self.server_number, self.server_language, page, id)).json()

        def get_item_type(item):
            type = None
            if 'sprite ship small ' in item:
                type = 'ship', int(item[29:32])
            elif 'metal' in item:
                type = 'resources', 'metal'
            elif 'crystal' in item:
                type = 'resources', 'crystal'
            elif 'deuterium' in item:
                type = 'resources', 'deuterium'
            return type

        items = response['content']['marketplace/marketplace_items_buying'].split('<div class="row item og-hline">')
        del items[0]
        for item in items:
            id_int = item.find('<a data-itemid=')
            ships_resources_marker_string = 'class="sprite '
            class_sprite = []
            for re_obj in re.finditer(ships_resources_marker_string, item):
                class_sprite.append(item[re_obj.start(): re_obj.end() + 40])
            to_buy_item_type = get_item_type(class_sprite[0])
            to_pay_item_type = get_item_type(class_sprite[1])

            quantity_marker_string = 'text quantity'
            text_quantity = []
            for re_obj in re.finditer(quantity_marker_string, item):
                text_quantity.append(item[re_obj.start(): re_obj.end() + 40])
            to_buy_item_amount = text_quantity[0].split('>')[1].split('<')[0].replace('.', '')
            to_pay_item_amount = text_quantity[1].split('>')[1].split('<')[0].replace('.', '')

            class bid:
                id = item[id_int + 16: id_int + 25].split('"')[0]
                offer = None
                price = None
                is_ships = False
                is_resources = False
                is_possible = False
                if to_buy_item_type[0] == 'ship':
                    is_ships = True
                    offer = to_buy_item_type[1], to_buy_item_amount, 'shipyard'
                else:
                    is_resources = True
                    if 'metal' in to_buy_item_type[1]:
                        offer = const.resources(metal=to_buy_item_amount)
                    elif 'crystal' in to_buy_item_type[1]:
                        offer = const.resources(cristal=to_buy_item_amount)
                    elif 'deuterium' in to_buy_item_type[1]:
                        offer = const.resources(deuterium=to_buy_item_amount)

                if 'metal' in to_pay_item_type[1]:
                    price = const.resources(metal=to_pay_item_amount)
                elif 'crystal' in to_pay_item_type[1]:
                    price = const.resources(cristal=to_pay_item_amount)
                elif 'deuterium' in to_pay_item_type[1]:
                    price = const.resources(deuterium=to_pay_item_amount)

                if 'enabled' in class_sprite[2]:
                    is_possible = True

            biddings.append(bid)
        return biddings

    def buy_marketplace(self, market_id, id):
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&' \
                                    'component=marketplace&tab=buying&action=fetchBuyingItems&ajax=1&'
                                    'pagination%5Bpage%5D={}&cp={}' \
                                    .format(self.server_number, self.server_language, 1, id)).json()

        form_data = {'marketItemId': market_id}
        response = self.session.post('https://s161-de.ogame.gameforge.com/game/index.php?page=ingame&'
                                     'component=marketplace&tab=buying&action=acceptRequest&asJson=1',
                                     data=form_data).json()
        if response['status'] == 'success':
            return True
        else:
            return False

    def submit_marketplace(self, offer, price, id):
        ItemId = None
        quantity = None
        priceType = None
        price_form = None
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                    'component=marketplace&tab=create_offer&cp={}'
                                    .format(self.server_number, self.server_language, id))

        if const.ships.is_ship(offer):
            itemType = 1
            ItemId = const.ships.get_ship_id(offer)
            quantity = const.ships.get_ship_amount(offer)
        else:
            itemType = 2
            for i, res in enumerate(offer):
                if res != 0:
                    ItemId = i + 1
                    quantity = res
                    break
        # ill fix this later in DRY
        for i, res in enumerate(price):
            if res != 0:
                priceType = i + 1
                price_form = res
                break

        form_data = {'marketItemType': 2,
                     'itemType': itemType,
                     'itemId': ItemId,
                     'quantity': quantity,
                     'priceType': priceType,
                     'price': price_form}
        response = self.session.post('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                     'component=marketplace&tab=create_offer&action=submitOffer&asJson=1'
                                     .format(self.server_number, self.server_language), data=form_data).json()
        if response['status'] == 'success':
            return True
        else:
            return False

    def collect_marketplace(self):
        to_collect_market_ids = []
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                    'component=marketplace&tab=history_buying&action=fetchHistoryBuyingItems&ajax=1&'
                                    'pagination%5Bpage%5D=1'
                                    .format(self.server_number, self.server_language, OGame2.get_planet_ids(self)[0])) \
                                    .json()
        items = response['content']['marketplace/marketplace_items_history'].split('data-transactionid=')
        del items[0]
        for item in items:
            if 'buttons small enabled collectItem' in item:
                to_collect_market_ids.append(int(item[1:10].split('"')[0]))

        response['status'] = False
        for id in to_collect_market_ids:
            form_data = {'marketTransactionId': id}
            response = self.session.post('https://s{}-{}.ogame.gameforge.com/game/index.php?page=componentOnly&'
                                         'component=marketplace&action=collectItem&asJson=1'
                                         .format(self.server_number, self.server_language), data=form_data).json()

        if response['status'] == 'success':
            return True
        else:
            return False

    def get_traider(self, id):
        raise Exception("function not implemented yet PLS contribute")

    def get_research(self):
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                    'component=research&cp={}'
                                    .format(self.server_number, self.server_language,
                                            OGame2.get_planet_ids(self)[0])).text
        marker_string = '''class="level"
                  data-value="'''

        class research_level(object):
            research_level = []
            for re_obj in re.finditer(marker_string.format(marker_string), response):
                research_level.append(int(response[re_obj.start() + len(marker_string):
                                                   re_obj.end() + 3].split('"')[0]))
            energy = research_level[0]
            laser = research_level[1]
            ion = research_level[2]
            hyperspace = research_level[3]
            plasma = research_level[4]
            combustion_drive = research_level[5]
            impulse_drive = research_level[6]
            hyperspace_drive = research_level[7]
            espionage = research_level[8]
            computer = research_level[9]
            astrophysics = research_level[10]
            research_network = research_level[11]
            graviton = research_level[12]
            weapons = research_level[13]
            shielding = research_level[14]
            armor = research_level[15]

        return research_level

    def get_ships(self, id):
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                    'component=shipyard&cp={}'
                                    .format(self.server_number, self.server_language, id)).text
        marker_string = '''class="amount"
                  data-value="'''

        class ships_amount(object):
            ships_amount = []
            for re_obj in re.finditer(marker_string.format(marker_string), response):
                ships_amount.append(int(response[re_obj.start() + len(marker_string):
                                                 re_obj.end() + 10].split('"')[0]))
            light_fighter = ships_amount[0]
            heavy_fighter = ships_amount[1]
            cruiser = ships_amount[2]
            battleship = ships_amount[3]
            interceptor = ships_amount[4]
            bomber = ships_amount[5]
            destroyer = ships_amount[6]
            deathstar = ships_amount[7]
            reaper = ships_amount[8]
            explorer = ships_amount[9]
            small_transporter = ships_amount[10]
            large_transporter = ships_amount[11]
            colonyShip = ships_amount[12]
            recycler = ships_amount[13]
            espionage_probe = ships_amount[14]
            solarSatellite = ships_amount[15]
            crawler = ships_amount[16]

        return ships_amount

    def get_defences(self, id):
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                    'component=defenses&cp={}'
                                    .format(self.server_number, self.server_language, id)).text
        marker_string = '''class="amount"
                  data-value="'''

        class defences_amount(object):
            defences_amount = []
            for re_obj in re.finditer(marker_string.format(marker_string), response):
                defences_amount.append(int(response[re_obj.start() + len(marker_string):
                                                    re_obj.end() + 10].split('"')[0]))
            rocket_launcher = defences_amount[0]
            laser_cannon_light = defences_amount[1]
            laser_cannon_heavy = defences_amount[2]
            gauss_cannon = defences_amount[3]
            ion_cannon = defences_amount[4]
            plasma_cannon = defences_amount[5]
            shield_dome_small = defences_amount[6]
            shield_dome_large = defences_amount[7]
            missile_interceptor = defences_amount[8]
            missile_interplanetary = defences_amount[9]

        return defences_amount

    def get_galaxy(self, coordinates):
        planet_info = []
        galaxy = coordinates[0]
        system = coordinates[1]
        form_data = {'galaxy': galaxy, 'system': system}
        response = self.session.post('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                     'component=galaxyContent&ajax=1'
                                     .format(self.server_number, self.server_language), data=form_data).text
        marker_string = '<td rel=\\"planet{}\\"'
        positions = []
        for position in range(1, 16):
            if response.find(marker_string.format(str(position))) != -1:
                positions.append(position)

        marker_string = '<h1>Planet:'
        planet_name = []
        for re_obj in re.finditer(marker_string, response):
            planet_name.append(response[re_obj.start() + 39: re_obj.end() + 50].split('<')[0])

        marker_string = '"status_abbr_'
        planet_player = []
        for re_obj in re.finditer(marker_string, response):
            raw_player = response[re_obj.start() + 0: re_obj.end() + 40]
            if '<' in raw_player:
                planet_player.append(raw_player.split('>')[1].split('<')[0])

        for pos, player, planet in zip(positions, planet_player, planet_name):
            planet_info.append([player,
                                [galaxy, system, pos, const.destination.planet],
                                planet])
        return planet_info

    def get_ally(self):
        ally_name = None
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=alliance'
                                    .format(self.server_number, self.server_language)).text
        marker_string = '<meta name="ogame-alliance-name" content="'
        for re_obj in re.finditer(marker_string, response):
            ally_name = response[re_obj.start() + len(marker_string): re_obj.end() + 10].split('"')[0]
        return ally_name

    def get_officers(self):
        raise Exception("function not implemented yet PLS contribute")

    def get_shop(self):
        raise Exception("function not implemented yet PLS contribute")

    def send_message(self, player_id, msg):
        form_data = {'playerId': player_id,
                     'text': msg,
                     'mode': 1,
                     'ajax': 1,
                     'token': self.chat_token}
        response = self.session.post('https://s{}-{}.ogame.gameforge.com/game/index.php?'
                                     'page=ajaxChat'.format(self.server_number, self.server_language),
                                     data=form_data).json()
        self.chat_token = response['newToken']

    def send_fleet(self, mission, id, where, ships, resources=[0, 0, 0], speed=10, holdingtime=0):
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                    'component=fleetdispatch&cp={}'
                                    .format(self.server_number, self.server_language, id)).text
        OGame2.get_init_sendfleetroken(self, response)

        form_data = {'token': self.sendfleet_token}

        for ship in ships:
            ship_type = 'am{}'.format(ship[0])
            form_data.update({ship_type: ship[1]})

        form_data.update({'galaxy': where[0],
                          'system': where[1],
                          'position': where[2],
                          'type': where[3],
                          'metal': resources[0],
                          'crystal': resources[1],
                          'deuterium': resources[2],
                          'prioMetal': 1,
                          'prioCrystal': 2,
                          'prioDeuterium': 3,
                          'mission': mission,
                          'speed': speed,
                          'retreatAfterDefenderRetreat': 0,
                          'union': 0,
                          'holdingtime': holdingtime})

        response = self.session.post('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                     'component=fleetdispatch&action=sendFleet&ajax=1&asJson=1'
                                     .format(self.server_number, self.server_language), data=form_data).json()
        return response['success']

    def build(self, what, id):
        type = what[0]
        amount = what[1]
        component = what[2]
        response = self.session.get('https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&'
                                    'component={}&cp={}'
                                    .format(self.server_number, self.server_language, component, id)).text
        OGame2.get_init_build_token(self, response, component)

        build_url = 'https://s{}-{}.ogame.gameforge.com/game/index.php?page=ingame&' \
                    'component={}&modus=1&token={}&type={}&menge={}' \
            .format(self.server_number, self.server_language, component, self.build_token, type, amount)
        response = self.session.get(build_url)

    def research(self, research, id):
        OGame2.build(self, research, id)
