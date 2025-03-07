"""
Functions related to AP regions for Pokémon FireRed and LeafGreen (see ./data/regions for region definitions)
"""
from typing import TYPE_CHECKING, Dict, List, Tuple, Optional, Callable
from BaseClasses import Region, CollectionState, ItemClassification
from .data import data
from .items import PokemonFRLGItem
from .locations import PokemonFRLGLocation
from .options import GameVersion, LevelScaling

if TYPE_CHECKING:
    from . import PokemonFRLGWorld

INDIRECT_CONDITIONS: Dict[str, List[str]] = {
    "Seafoam Islands 1F": ["Seafoam Islands B3F Southwest Surfing Spot", "Seafoam Islands B3F Southwest Landing",
                           "Seafoam Islands B3F East Landing (South)", "Seafoam Islands B3F East Surfing Spot (South)",
                           "Seafoam Islands B3F South Water (Water Battle)"],
    "Seafoam Islands B3F Southwest": ["Seafoam Islands B4F Surfing Spot (West)",
                                      "Seafoam Islands B4F Near Articuno Landing"],
    "Victory Road 3F Southwest": ["Victory Road 2F Center Rock Barrier"],
    "Vermilion City": ["Navel Rock Arrival", "Birth Island Arrival"]
}

SEVII_REQUIRED_EVENTS = [
    "Champion's Room - Champion Rematch Reward"
]

STATIC_POKEMON_SPOILER_NAMES = {
    "STATIC_POKEMON_ELECTRODE_1": "Power Plant (Static)",
    "STATIC_POKEMON_ELECTRODE_2": "Power Plant (Static)",
    "LEGENDARY_POKEMON_ZAPDOS": "Power Plant (Static)",
    "CELADON_PRIZE_POKEMON_1": "Celadon Game Corner Prize Room",
    "CELADON_PRIZE_POKEMON_2": "Celadon Game Corner Prize Room",
    "CELADON_PRIZE_POKEMON_3": "Celadon Game Corner Prize Room",
    "CELADON_PRIZE_POKEMON_4": "Celadon Game Corner Prize Room",
    "CELADON_PRIZE_POKEMON_5": "Celadon Game Corner Prize Room",
    "GIFT_POKEMON_EEVEE": "Celadon Condominiums Roof Room",
    "STATIC_POKEMON_ROUTE12_SNORLAX": "Route 12 (Static)",
    "STATIC_POKEMON_ROUTE16_SNORLAX": "Route 16 (Static)",
    "GIFT_POKEMON_HITMONCHAN": "Saffron Dojo",
    "GIFT_POKEMON_HITMONLEE": "Saffron Dojo",
    "GIFT_POKEMON_LAPRAS": "Silph Co. 7F",
    "LEGENDARY_POKEMON_ARTICUNO": "Seafoam Islands B4F (Static)",
    "GIFT_POKEMON_OMANYTE": "Pokemon Lab Experiment Room (Helix)",
    "GIFT_POKEMON_KABUTO": "Pokemon Lab Experiment Room (Dome)",
    "GIFT_POKEMON_AERODACTYL": "Pokemon Lab Experiment Room (Amber)",
    "LEGENDARY_POKEMON_MOLTRES": "Mt. Ember Summit",
    "STATIC_POKEMON_HYPNO": "Berry Forest (Static)",
    "EGG_POKEMON_TOGEPI": "Water Labyrinth (Egg)",
    "LEGENDARY_POKEMON_MEWTWO": "Cerulean Cave B1F (Static)",
    "LEGENDARY_POKEMON_HO_OH": "Navel Rock Summit",
    "LEGENDARY_POKEMON_LUGIA": "Navel Rock Base",
    "LEGENDARY_POKEMON_DEOXYS": "Birth Island Exterior"
}

STARTING_TOWNS = {
    "SPAWN_PALLET_TOWN": "Pallet Town",
    "SPAWN_VIRIDIAN_CITY": "Viridian City South",
    "SPAWN_PEWTER_CITY": "Pewter City",
    "SPAWN_CERULEAN_CITY": "Cerulean City",
    "SPAWN_LAVENDER_TOWN": "Lavender Town",
    "SPAWN_VERMILION_CITY": "Vermilion City",
    "SPAWN_CELADON_CITY": "Celadon City",
    "SPAWN_FUCHSIA_CITY": "Fuchsia City",
    "SPAWN_CINNABAR_ISLAND": "Cinnabar Island",
    "SPAWN_INDIGO_PLATEAU": "Indigo Plateau",
    "SPAWN_SAFFRON_CITY": "Saffron City",
    "SPAWN_ROUTE4": "Route 4 West",
    "SPAWN_ROUTE10": "Route 10 North",
    "SPAWN_ONE_ISLAND": "One Island Town",
    "SPAWN_TWO_ISLAND": "Two Island Town",
    "SPAWN_THREE_ISLAND": "Three Island Town South",
    "SPAWN_FOUR_ISLAND": "Four Island Town",
    "SPAWN_FIVE_ISLAND": "Five Island Town",
    "SPAWN_SEVEN_ISLAND": "Seven Island Town",
    "SPAWN_SIX_ISLAND": "Six Island Town"
}

# Data is formatted as (Map Group, Map Num, X-Coord, Y-Coord, Region Map ID, Region Map Index)
kanto_fly_destinations = {
    "Pallet Town": {
        "Pallet Town": [
            (3, 0, 6, 8, 1, 246),
            (3, 0, 15, 8, 1, 246),
            (3, 0, 16, 14, 1, 246)
        ]
    },
    "Viridian City": {
        "Viridian City South": [
            (3, 1, 25, 12, 1, 180),
            (3, 1, 25, 19, 1, 180),
            (3, 1, 36, 20, 1, 180),
            (3, 1, 26, 27, 1, 180)
        ],
        "Viridian City North": [
            (3, 1, 36, 11, 1, 180)
        ]
    },
    "Pewter City": {
        "Pewter City": [
            (3, 2, 17, 7, 1, 92),
            (3, 2, 33, 12, 1, 92),
            (3, 2, 15, 17, 1, 92),
            (3, 2, 28, 19, 1, 92),
            (3, 2, 17, 26, 1, 92),
            (3, 2, 9, 31, 1, 92)
        ],
        "Pewter City Near Museum": [
            (3, 2, 9, 25, 5, 92)
        ]
    },
    "Cerulean City": {
        "Cerulean City": [
            (3, 3, 10, 12, 1, 80),
            (3, 3, 17, 12, 1, 80),
            (3, 3, 30, 12, 1, 80),
            (3, 3, 15, 18, 1, 80),
            (3, 3, 22, 20, 1, 80),
            (3, 3, 13, 29, 1, 80),
            (3, 3, 23, 29, 1, 80),
            (3, 3, 29, 29, 1, 80)
        ],
        "Cerulean City Backyard": [
            (3, 3, 10, 8, 1, 80)
        ],
        "Cerulean City Outskirts": [
            (3, 3, 31, 8, 1, 80)
        ],
        "Cerulean City Near Cave": [
            (3, 3, 1, 13, 1, 80)
        ]
    },
    "Vermilion City": {
        "Vermilion City": [
            (3, 5, 9, 7, 1, 212),
            (3, 5, 15, 7, 1, 212),
            (3, 5, 12, 18, 1, 212),
            (3, 5, 19, 18, 1, 212),
            (3, 5, 29, 18, 1, 212),
            (3, 5, 28, 25, 1, 212)
        ],
        "Vermilion City Near Gym": [
            (3, 5, 14, 26, 1, 212)
        ],
        "Vermilion City Near Harbor": [
            (3, 5, 23, 34, 1, 212)
        ]
    },
    "Lavender Town": {
        "Lavender Town": [
            (3, 4, 6, 6, 1, 150),
            (3, 4, 18, 7, 1, 150),
            (3, 4, 10, 12, 1, 150),
            (3, 4, 20, 16, 1, 150),
            (3, 4, 5, 17, 1, 150),
            (3, 4, 10, 17, 1, 150)
        ]
    },
    "Celadon City": {
        "Celadon City": [
            (3, 6, 30, 4, 1, 143),
            (3, 6, 30, 12, 1, 143),
            (3, 6, 48, 12, 1, 143),
            (3, 6, 11, 15, 1, 143),
            (3, 6, 15, 15, 1, 143),
            (3, 6, 39, 21, 1, 143),
            (3, 6, 34, 22, 1, 143),
            (3, 6, 37, 30, 1, 143),
            (3, 6, 41, 30, 1, 143),
            (3, 6, 49, 30, 1, 143)
        ],
        "Celadon City Near Gym": [
            (3, 6, 11, 31, 1, 143)
        ]
    },
    "Fuchsia City": {
        "Fuchsia City": [
            (3, 7, 24, 6, 1, 276),
            (3, 7, 11, 16, 1, 276),
            (3, 7, 28, 17, 1, 276),
            (3, 7, 14, 32, 1, 276),
            (3, 7, 19, 32, 1, 276),
            (3, 7, 25, 32, 1, 276),
            (3, 7, 33, 32, 1, 276),
            (3, 7, 38, 32, 1, 276),
            (3, 7, 9, 33, 1, 276)
        ],
        "Fuchsia City Backyard": [
            (3, 7, 39, 28, 1, 276)
        ]
    },
    "Saffron City": {
        "Saffron City": [
            (3, 10, 34, 6, 1, 146),
            (3, 10, 40, 13, 1, 146),
            (3, 10, 46, 13, 1, 146),
            (3, 10, 22, 15, 1, 146),
            (3, 10, 27, 22, 1, 146),
            (3, 10, 40, 22, 1, 146),
            (3, 10, 47, 22, 1, 146),
            (3, 10, 8, 27, 1, 146),
            (3, 10, 58, 27, 1, 146),
            (3, 10, 33, 31, 1, 146),
            (3, 10, 24, 39, 1, 146),
            (3, 10, 43, 39, 1, 146),
            (3, 10, 34, 46, 1, 146)
        ]
    },
    "Cinnabar Island": {
        "Cinnabar Island": [
            (3, 8, 8, 4, 1, 312),
            (3, 8, 20, 5, 1, 312),
            (3, 8, 8, 10, 1, 312),
            (3, 8, 14, 12, 1, 312),
            (3, 8, 19, 12, 1, 312),
        ]
    },
    "Indigo Plateau": {
        "Indigo Plateau": [
            (3, 9, 11, 7, 1, 68)
        ]
    },
    "Route 2": {
        "Route 2 Southwest": [
            (3, 20, 5, 52, 1, 136)
        ],
        "Route 2 Northwest": [
            (3, 20, 5, 13, 1, 114)
        ],
        "Route 2 Northeast": [
            (3, 20, 17, 12, 1, 114),
            (3, 20, 17, 23, 1, 114)
        ],
        "Route 2 East": [
            (3, 20, 18, 41, 1, 136)
        ],
        "Route 2 Southeast": [
            (3, 20, 18, 47, 1, 136)
        ]
    },
    "Route 4": {
        "Route 4 West": [
            (3, 22, 12, 6, 1, 74),
            (3, 22, 19, 6, 1, 75)
        ],
        "Route 4 East": [
            (3, 22, 32, 6, 1, 75)
        ]
    },
    "Route 5": {
        "Route 5": [
            (3, 23, 23, 26, 1, 124),
            (3, 23, 24, 32, 1, 124)
        ],
        "Route 5 Near Tunnel": [
            (3, 23, 31, 32, 1, 124)
        ]
    },
    "Route 6": {
        "Route 6": [
            (3, 24, 12, 6, 1, 168)
        ],
        "Route 6 Near Tunnel": [
            (3, 24, 19, 14, 1, 168)
        ]
    },
    "Route 7": {
        "Route 7": [
            (3, 25, 15, 10, 1, 145)
        ],
        "Route 7 Near Tunnel": [
            (3, 25, 7, 15, 1, 144)
        ]
    },
    "Route 8": {
        "Route 8": [
            (3, 26, 7, 10, 1, 147)
        ],
        "Route 8 Near Tunnel": [
            (3, 26, 13, 5, 1, 147)
        ]
    },
    "Route 10": {
        "Route 10 North": [
            (3, 28, 8, 20, 1, 84),
            (3, 28, 13, 21, 1, 84)
        ],
        "Route 10 South": [
            (3, 28, 8, 58, 1, 128)
        ],
        "Route 10 Near Power Plant": [
            (3, 28, 7, 41, 1, 106)
        ],
        "Route 10 Near Power Plant Back": [
            (3, 28, 2, 37, 1, 106)
        ]
    },
    "Route 11": {
        "Route 11 West": [
            (3, 29, 6, 8, 1, 213),
            (3, 29, 58, 10, 1, 215)
        ],
        "Route 11 East": [
            (3, 29, 65, 10, 1, 215)
        ]
    },
    "Route 12": {
        "Route 12 North": [
            (3, 30, 14, 15, 1, 172)
        ],
        "Route 12 Center": [
            (3, 30, 14, 22, 1, 172)
        ],
        "Route 12 South": [
            (3, 30, 12, 87, 1, 238)
        ]
    },
    "Route 15": {
        "Route 15 South": [
            (3, 33, 16, 11, 1, 277)
        ],
        "Route 15 Southwest": [
            (3, 33, 9, 11, 1, 277)
        ]
    },
    "Route 16": {
        "Route 16 Northeast": [
            (3, 34, 27, 6, 1, 141)
        ],
        "Route 16 Northwest": [
            (3, 34, 10, 6, 1, 139),
            (3, 34, 20, 6, 1, 140)
        ],
        "Route 16 Center": [
            (3, 34, 27, 13, 1, 141)
        ]
    },
    "Route 18": {
        "Route 18 East": [
            (3, 36, 48, 9, 1, 275)
        ]
    },
    "Route 20": {
        "Route 20 Near North Cave": [
            (3, 38, 60, 9, 1, 316)
        ],
        "Route 20 Near South Cave": [
            (3, 38, 72, 15, 1, 317)
        ]
    },
    "Route 22": {
        "Route 22": [
            (3, 41, 8, 6, 1, 178)
        ]
    },
    "Route 23": {
        "Route 23 South": [
            (3, 42, 8, 153, 1, 156)
        ],
        "Route 23 Near Cave": [
            (3, 42, 5, 29, 1, 90)
        ],
        "Route 23 North": [
            (3, 42, 18, 29, 1, 90)
        ]
    },
    "Route 25": {
        "Route 25": [
            (3, 44, 51, 5, 1, 38)
        ]
    },
    "Navel Rock": {
        "Navel Rock Exterior": [
            (2, 0, 9, 9, 3, 186),
            (2, 0, 9, 16, 3, 186)
        ]
    },
    "Birth Island": {
        "Birth Island Exterior": [
            (2, 56, 15, 24, 4, 304)
        ]
    }
}

sevii_fly_destinations = {
    "One Island Town": {
        "One Island Town": [
            (3, 12, 14, 6, 2, 177),
            (3, 12, 19, 10, 2, 177),
            (3, 12, 8, 12, 2, 177),
            (3, 12, 12, 18, 2, 177)
        ]
    },
    "Kindle Road": {
        "Kindle Road Center": [
            (3, 45, 15, 59, 2, 112)
        ],
        "Kindle Road North": [
            (3, 45, 11, 6, 2, 68)
        ]
    },
    "Two Island Town": {
        "Two Island Town": [
            (3, 13, 10, 8, 2, 207),
            (3, 13, 21, 8, 2, 207),
            (3, 13, 33, 10, 2, 207),
            (3, 13, 39, 10, 2, 207)
        ]
    },
    "Cape Brink": {
        "Cape Brink": [
            (3, 47, 12, 17, 2, 163)
        ]
    },
    "Three Isle Port": {
        "Three Isle Port West": [
            (3, 49, 16, 5, 2, 304),
            (3, 49, 12, 13, 2, 304)
        ],
        "Three Isle Port East": [
            (3, 49, 38, 6, 2, 305)
        ]
    },
    "Three Island Town": {
        "Three Island Town South": [
            (3, 14, 14, 28, 2, 282),
            (3, 14, 3, 32, 2, 282)
        ],
        "Three Island Town North": [
            (3, 14, 4, 7, 2, 282),
            (3, 14, 12, 7, 2, 282),
            (3, 14, 12, 13, 2, 282),
            (3, 14, 18, 13, 2, 282),
            (3, 14, 13, 20, 2, 282)
        ]
    },
    "Bond Bridge": {
        "Bond Bridge": [
            (3, 48, 12, 7, 2, 278)
        ]
    },
    "Four Island Town": {
        "Four Island Town": [
            (3, 15, 12, 14, 3, 91),
            (3, 15, 25, 15, 3, 91),
            (3, 15, 18, 21, 3, 91),
            (3, 15, 33, 24, 3, 91),
            (3, 15, 22, 27, 3, 91),
            (3, 15, 25, 27, 3, 91),
            (3, 15, 10, 28, 3, 91)
        ],
        "Four Island Town Near Cave": [
            (3, 15, 38, 13, 3, 91)
        ]
    },
    "Five Island Town": {
        "Five Island Town": [
            (3, 16, 12, 7, 3, 258),
            (3, 16, 18, 7, 3, 258),
            (3, 16, 22, 10, 3, 258),
            (3, 16, 12, 14, 3, 258)
        ]
    },
    "Five Isle Meadow": {
        "Five Isle Meadow": [
            (3, 56, 12, 22, 3, 281)
        ]
    },
    "Resort Gorgeous": {
        "Resort Gorgeous Near Resort": [
            (3, 54, 39, 9, 3, 215)
        ],
        "Resort Gorgeous Near Cave": [
            (3, 54, 64, 14, 3, 216)
        ]
    },
    "Six Island Town": {
        "Six Island Town": [
            (3, 18, 11, 12, 4, 127),
            (3, 18, 20, 12, 4, 127),
            (3, 18, 16, 18, 4, 127)
        ]
    },
    "Water Path": {
        "Water Path North": [
            (3, 60, 5, 14, 4, 84),
            (3, 60, 11, 20, 4, 84)
        ]
    },
    "Ruin Valley": {
        "Ruin Valley": [
            (3, 61, 24, 25, 4, 192)
        ]
    },
    "Green Path": {
        "Green Path East": [
            (3, 59, 63, 11, 4, 83)
        ],
        "Green Path West": [
            (3, 59, 45, 11, 4, 82)
        ]
    },
    "Outcast Island": {
        "Outcast Island": [
            (3, 58, 7, 22, 4, 15)
        ]
    },
    "Seven Island Town": {
        "Seven Island Town": [
            (3, 17, 12, 4, 4, 181),
            (3, 17, 5, 10, 4, 181),
            (3, 17, 11, 10, 4, 181),
            (3, 17, 16, 13, 4, 181)
        ]
    },
    "Sevault Canyon": {
        "Sevault Canyon": [
            (3, 64, 7, 18, 4, 204),
            (3, 64, 14, 62, 4, 248)
        ]
    },
    "Tanoby Ruins": {
        "Tanoby Ruins Viapois Island": [
            (3, 65, 11, 7, 4, 267)
        ],
        "Tanoby Ruins Rixy Island": [
            (3, 65, 12, 16, 4, 267)
        ],
        "Tanoby Ruins Scufib Island": [
            (3, 65, 32, 10, 4, 268)
        ],
        "Tanoby Ruins Dilford Island": [
            (3, 65, 44, 12, 4, 269)
        ],
        "Tanoby Ruins Weepth Island": [
            (3, 65, 88, 9, 4, 271)
        ],
        "Tanoby Ruins Liptoo Island": [
            (3, 65, 103, 11, 4, 272)
        ],
        "Tanoby Ruins Monean Island": [
            (3, 65, 120, 11, 4, 273)
        ]
    },
    "Trainer Tower Exterior": {
        "Trainer Tower Exterior North": [
            (3, 62, 58, 8, 4, 137)
        ]
    }
}

fly_destination_entrance_map = {
      "Pallet Town Fly Destination": "SPAWN_PALLET_TOWN",
      "Viridian City Fly Destination": "SPAWN_VIRIDIAN_CITY",
      "Pewter City Fly Destination": "SPAWN_PEWTER_CITY",
      "Route 4 Fly Destination": "SPAWN_ROUTE4",
      "Cerulean City Fly Destination": "SPAWN_CERULEAN_CITY",
      "Vermilion City Fly Destination": "SPAWN_VERMILION_CITY",
      "Route 10 Fly Destination": "SPAWN_ROUTE10",
      "Lavender Town Fly Destination": "SPAWN_LAVENDER_TOWN",
      "Celadon City Fly Destination": "SPAWN_CELADON_CITY",
      "Fuchsia City Fly Destination": "SPAWN_FUCHSIA_CITY",
      "Saffron City Fly Destination": "SPAWN_SAFFRON_CITY",
      "Cinnabar Island Fly Destination": "SPAWN_CINNABAR_ISLAND",
      "Indigo Plateau Fly Destination": 'SPAWN_INDIGO_PLATEAU',
      "One Island Fly Destination": "SPAWN_ONE_ISLAND",
      "Two Island Fly Destination": "SPAWN_TWO_ISLAND",
      "Three Island Fly Destination": "SPAWN_THREE_ISLAND",
      "Four Island Fly Destination": "SPAWN_FOUR_ISLAND",
      "Five Island Fly Destination": "SPAWN_FIVE_ISLAND",
      "Six Island Fly Destination": "SPAWN_SIX_ISLAND",
      "Seven Island Fly Destination": "SPAWN_SEVEN_ISLAND"
}


class PokemonFRLGRegion(Region):
    distance: Optional[int]

    def __init__(self, name, player, multiworld):
        super().__init__(name, player, multiworld)
        self.distance = None


def create_regions(world: "PokemonFRLGWorld") -> Dict[str, Region]:
    """
    Iterates through regions created from JSON to create regions and adds them to the multiworld.
    Also creates and places events and connects regions via warps and the exits defined in the JSON.
    """

    # Used in connect_to_map_encounters. Splits encounter categories into "subcategories" and gives them names
    # and rules so the rods can only access their specific slots.
    encounter_categories: Dict[str, List[Tuple[Optional[str], range, Optional[Callable[[CollectionState], bool]]]]] = {
        "Land": [(None, range(0, 12), None)],
        "Water": [(None, range(0, 5), None)],
        "Fishing": [
            ("Old Rod", range(0, 2), lambda state: state.has("Old Rod", world.player)),
            ("Good Rod", range(2, 5), lambda state: state.has("Good Rod", world.player)),
            ("Super Rod", range(5, 10), lambda state: state.has("Super Rod", world.player)),
        ],
    }

    game_version = world.options.game_version.current_key
    kanto_only = world.options.kanto_only

    def connect_to_map_encounters(regions: Dict[str, Region], region: Region, map_name: str, encounter_region_name: str,
                                  include_slots: Tuple[bool, bool, bool]):
        """
        Connects the provided region to the corresponding wild encounters for the given parent map.

        Each in-game map may have a non-physical Region for encountering wild Pokémon in each of the three categories
        land, water, and fishing. Region data defines whether a given region includes places where those encounters can
        be accessed (i.e. whether the region has tall grass, a river bank, is on water, etc.).

        These regions are created lazily and dynamically so as not to bother with unused maps.
        """

        if True in include_slots and encounter_region_name is None:
            raise AssertionError(f"{region.name} has encounters but does not have an encounter region name")

        for i, encounter_category in enumerate(encounter_categories.items()):
            if include_slots[i]:
                region_name = f"{encounter_region_name} {encounter_category[0]} Encounters"

                # If the region hasn't been created yet, create it now
                try:
                    encounter_region = regions[region_name]
                except KeyError:
                    encounter_region = PokemonFRLGRegion(region_name, world.player, world.multiworld)
                    encounter_slots = getattr(world.modified_maps[map_name],
                                              f"{encounter_category[0].lower()}_encounters").slots[game_version]

                    # Subcategory is for splitting fishing rods; land and water only have one subcategory
                    for subcategory in encounter_category[1]:
                        # Want to create locations per species, not per slot
                        # encounter_categories includes info on which slots belong to which subcategory
                        unique_species = []
                        for j, species_data in enumerate(encounter_slots):
                            species_id = species_data.species_id
                            if j in subcategory[1] and species_id not in unique_species:
                                unique_species.append(species_id)

                        # Create a location for the species
                        for j, species_id in enumerate(unique_species):
                            subcategory_name = subcategory[0] if subcategory[0] is not None else encounter_category[0]

                            encounter_location = PokemonFRLGLocation(
                                world.player,
                                f"{encounter_region_name} - {subcategory_name} Encounter {j + 1}",
                                None,
                                encounter_region,
                                None,
                                None,
                                frozenset(["Pokemon", "Wild"]),
                                spoiler_name=f"{encounter_region_name} ({subcategory_name})",
                            )
                            encounter_location.show_in_spoiler = False

                            # Add access rules
                            if subcategory[2] is not None:
                                encounter_location.access_rule = subcategory[2]

                            # Fill the location with an event for catching that species
                            encounter_location.place_locked_item(PokemonFRLGItem(
                                data.species[species_id].name,
                                ItemClassification.progression_skip_balancing,
                                None,
                                world.player
                            ))
                            world.repeatable_pokemon.add(data.species[species_id].name)
                            encounter_region.locations.append(encounter_location)

                    # Add the new encounter region to the multiworld
                    regions[region_name] = encounter_region

                # Encounter region exists, just connect to it
                region.connect(encounter_region, f"{region.name} ({encounter_category[0]} Battle)")

    regions: Dict[str, Region] = {}
    connections: List[Tuple[str, str, str]] = []
    for region_data in data.regions.values():
        if kanto_only and not region_data.kanto:
            continue

        region_name = region_data.name
        new_region = PokemonFRLGRegion(region_name, world.player, world.multiworld)

        for event_id in region_data.events:
            event_data = world.modified_events[event_id]

            if world.options.kanto_only and event_data.name in SEVII_REQUIRED_EVENTS:
                continue

            if type(event_data.name) is list:
                if world.options.game_version == GameVersion.option_firered:
                    name = event_data.name[0]
                else:
                    name = event_data.name[1]
            else:
                name = event_data.name

            if type(event_data.item) is list:
                if world.options.game_version == GameVersion.option_firered:
                    item = event_data.item[0]
                else:
                    item = event_data.item[1]
            else:
                item = event_data.item

            event = PokemonFRLGLocation(world.player,
                                        name,
                                        None,
                                        new_region,
                                        None,
                                        None,
                                        event_data.tags,
                                        spoiler_name=STATIC_POKEMON_SPOILER_NAMES[event_id]
                                        if event_id in STATIC_POKEMON_SPOILER_NAMES else None)
            event.place_locked_item(PokemonFRLGItem(item,
                                                    ItemClassification.progression,
                                                    None,
                                                    world.player))
            event.show_in_spoiler = False
            new_region.locations.append(event)

            if "Trade" in name:
                world.trade_pokemon.append([region_name, name])

        for region_id, exit_name in region_data.exits.items():
            if kanto_only and not data.regions[region_id].kanto:
                continue
            region_exit = data.regions[region_id].name
            if not kanto_only and region_exit == "Vermilion City" and exit_name == "Follow Bill":
                continue
            connections.append((exit_name, region_name, region_exit))

        for warp in region_data.warps:
            source_warp = data.warps[warp]
            if source_warp.name == "":
                continue
            dest_warp = data.warps[data.warp_map[warp]]
            if dest_warp.parent_region_id is None:
                continue
            if kanto_only and not data.regions[dest_warp.parent_region_id].kanto:
                continue
            dest_region_name = data.regions[dest_warp.parent_region_id].name
            connections.append((source_warp.name, region_name, dest_region_name))

        regions[region_name] = new_region

        parent_map_name = region_data.parent_map.name if region_data.parent_map is not None else None
        connect_to_map_encounters(regions, new_region, parent_map_name, region_data.encounter_region,
                                  (region_data.has_land, region_data.has_water, region_data.has_fishing))

    for name, source, dest in connections:
        name = modify_entrance_name(world, name)
        regions[source].connect(regions[dest], name)

    if world.options.level_scaling != LevelScaling.option_off:
        trainer_name_level_list: List[Tuple[str, int]] = []
        encounter_name_level_list: List[Tuple[str, int]] = []

        game_version = world.options.game_version.current_key

        for scaling_data in world.scaling_data:
            if scaling_data.region not in regions:
                region = PokemonFRLGRegion(scaling_data.region, world.player, world.multiworld)
                regions[scaling_data.region] = region

                for connection in scaling_data.connections:
                    name = f"{regions[connection].name} -> {region.name}"
                    regions[connection].connect(region, name)
            else:
                region = regions[scaling_data.region]

            if "Trainer" in scaling_data.tags:
                scaling_event = PokemonFRLGLocation(
                    world.player,
                    scaling_data.name,
                    None,
                    region,
                    None,
                    None,
                    scaling_data.tags,
                    scaling_data.data_ids
                )
                scaling_event.place_locked_item(PokemonFRLGItem("Trainer Party",
                                                                ItemClassification.filler,
                                                                None,
                                                                world.player))
                scaling_event.show_in_spoiler = False
                region.locations.append(scaling_event)
            elif "Static" in scaling_data.tags:
                scaling_event = PokemonFRLGLocation(
                    world.player,
                    scaling_data.name,
                    None,
                    region,
                    None,
                    None,
                    scaling_data.tags,
                    scaling_data.data_ids
                )
                scaling_event.place_locked_item(PokemonFRLGItem("Static Encounter",
                                                                ItemClassification.filler,
                                                                None,
                                                                world.player))
                scaling_event.show_in_spoiler = False
                region.locations.append(scaling_event)
            elif "Wild" in scaling_data.tags:
                index = 1
                events: Dict[str, Tuple[str, List[str], Optional[Callable[[CollectionState], bool]]]] = {}
                encounter_category_data = encounter_categories[scaling_data.type]
                for data_id in scaling_data.data_ids:
                    map_data = data.maps[data_id]
                    encounters = (map_data.land_encounters if scaling_data.type == "Land" else
                                  map_data.water_encounters if scaling_data.type == "Water" else
                                  map_data.fishing_encounters)
                    for subcategory in encounter_category_data:
                        for i in subcategory[1]:
                            subcategory_name = subcategory[0] if subcategory[0] is not None else scaling_data.type
                            species_name = f"{subcategory_name} {encounters.slots[game_version][i].species_id}"
                            if species_name not in events:
                                encounter_data = (f"{scaling_data.name} {index}", [f"{data_id} {i}"], subcategory[2])
                                events[species_name] = encounter_data
                                index = index + 1
                            else:
                                events[species_name][1].append(f"{data_id} {i}")

                for event in events.values():
                    scaling_event = PokemonFRLGLocation(
                        world.player,
                        event[0],
                        None,
                        region,
                        None,
                        None,
                        scaling_data.tags | {scaling_data.type},
                        event[1]
                    )

                    scaling_event.place_locked_item(PokemonFRLGItem("Wild Encounter",
                                                                    ItemClassification.filler,
                                                                    None,
                                                                    world.player))
                    scaling_event.show_in_spoiler = False
                    if event[2] is not None:
                        scaling_event.access_rule = event[2]
                    region.locations.append(scaling_event)

        for region in regions.values():
            for location in region.locations:
                if "Scaling" in location.tags:
                    if "Trainer" in location.tags:
                        min_level = 100

                        for data_id in location.data_ids:
                            trainer_data = data.trainers[data_id]
                            for pokemon in trainer_data.party.pokemon:
                                min_level = min(min_level, pokemon.level)

                        trainer_name_level_list.append((location.name, min_level))
                        world.trainer_name_level_dict[location.name] = min_level
                    elif "Static" in location.tags:
                        for data_id in location.data_ids:
                            pokemon_data = None

                            if data_id in data.misc_pokemon:
                                pokemon_data = data.misc_pokemon[data_id]
                            elif data_id in data.legendary_pokemon:
                                pokemon_data = data.legendary_pokemon[data_id]

                            encounter_name_level_list.append((location.name, pokemon_data.level[game_version]))
                            world.encounter_name_level_dict[location.name] = pokemon_data.level[game_version]
                    elif "Wild" in location.tags:
                        max_level = 1

                        for data_id in location.data_ids:
                            data_ids = data_id.split()
                            map_data = data.maps[data_ids[0]]
                            encounters = (map_data.land_encounters if "Land" in location.tags else
                                          map_data.water_encounters if "Water" in location.tags else
                                          map_data.fishing_encounters)

                            encounter_max_level = encounters.slots[game_version][int(data_ids[1])].max_level
                            max_level = max(max_level, encounter_max_level)

                        encounter_name_level_list.append((location.name, max_level)),
                        world.encounter_name_level_dict[location.name] = max_level

        trainer_name_level_list.sort(key=lambda i: i[1])
        world.trainer_name_list = [i[0] for i in trainer_name_level_list]
        world.trainer_level_list = [i[1] for i in trainer_name_level_list]
        encounter_name_level_list.sort(key=lambda i: i[1])
        world.encounter_name_list = [i[0] for i in encounter_name_level_list]
        world.encounter_level_list = [i[1] for i in encounter_name_level_list]

    if world.options.random_starting_town:
        forbidden_starting_towns = ["SPAWN_INDIGO_PLATEAU", "SPAWN_ROUTE10"]
        if world.options.kanto_only:
            forbidden_starting_towns.extend(["SPAWN_ONE_ISLAND", "SPAWN_TWO_ISLAND", "SPAWN_THREE_ISLAND",
                                             "SPAWN_FOUR_ISLAND", "SPAWN_FIVE_ISLAND", "SPAWN_SIX_ISLAND",
                                             "SPAWN_SEVEN_ISLAND"])
        allowed_starting_towns = [town for town in STARTING_TOWNS.keys() if town not in forbidden_starting_towns]
        world.starting_town = world.random.choice(allowed_starting_towns)

    if world.options.randomize_fly_destinations:
        fly_destinations = kanto_fly_destinations.copy()
        if not world.options.kanto_only:
            fly_destinations.update(sevii_fly_destinations)
        maps_already_chosen = set()
        for exit in regions["Sky"].exits:
            regions[exit.connected_region.name].entrances.remove(exit)
            exit.connected_region = None
            allowed_maps = [k for k in fly_destinations.keys() if k not in maps_already_chosen]
            map = world.random.choice(allowed_maps)
            allowed_regions = list(fly_destinations[map].keys())
            region = world.random.choice(allowed_regions)
            allowed_warps = fly_destinations[map][region]
            warp = world.random.choice(allowed_warps)
            maps_already_chosen.add(map)
            exit.connected_region = regions[region]
            regions[region].entrances.append(exit)
            world.fly_destination_data[fly_destination_entrance_map[exit.name]] = warp

    regions["Menu"] = PokemonFRLGRegion("Menu", world.player, world.multiworld)
    regions["Menu"].connect(regions[STARTING_TOWNS[world.starting_town]], "Start Game")
    regions["Menu"].connect(regions["Player's PC"], "Use PC")
    regions["Menu"].connect(regions["Pokedex"], "Pokedex")
    regions["Menu"].connect(regions["Evolutions"], "Evolve")
    regions["Menu"].connect(regions["Sky"], "Flying")

    return regions


def create_indirect_conditions(world: "PokemonFRLGWorld"):
    for region, entrances in INDIRECT_CONDITIONS.items():
        for entrance in entrances:
            world.multiworld.register_indirect_condition(world.get_region(region), world.get_entrance(entrance))


def modify_entrance_name(world: "PokemonFRLGWorld", name: str) -> str:
    route_2_modification = {
        "Route 2 Northwest Cuttable Tree": "Route 2 Northwest Smashable Rock",
        "Route 2 Northeast Cuttable Tree (North)": "Route 2 Northeast Smashable Rock",
        "Route 2 Northeast Cuttable Tree (South)": "Route 2 Northeast Cuttable Tree"
    }
    block_tunnels = {
        "Route 5 Unobstructed Path": "Route 5 Smashable Rocks",
        "Route 5 Near Tunnel Unobstructed Path": "Route 5 Near Tunnel Smashable Rocks",
        "Route 6 Unobstructed Path": "Route 6 Smashable Rocks",
        "Route 6 Near Tunnel Unobstructed Path": "Route 6 Near Tunnel Smashable Rocks",
        "Route 7 Unobstructed Path": "Route 7 Smashable Rocks",
        "Route 7 Near Tunnel Unobstructed Path": "Route 7 Near Tunnel Smashable Rocks",
        "Route 8 Unobstructed Path": "Route 8 Smashable Rocks",
        "Route 8 Near Tunnel Unobstructed Path": "Route 8 Near Tunnel Smashable Rocks"
    }
    block_pokemon_tower = {
        "Pokemon Tower 1F Unobstructed Path": "Pokemon Tower 1F Reveal Ghost",
        "Pokemon Tower 1F Near Stairs Unobstructed Path": "Pokemon Tower 1F Near Stairs Pass Ghost"
    }
    rotue_23_trees = {
        "Route 23 Near Water Unobstructed Path": "Route 23 Near Water Cuttable Trees",
        "Route 23 Center Unobstructed Path": "Route 23 Center Cuttable Trees"
    }
    route_23_modification = {
        "Route 23 South Water Unobstructed Path": "Route 23 Waterfall Ascend",
        "Route 23 North Water Unobstructed Path": "Route 23 Waterfall Drop"
    }

    if "Modify Route 2" in world.options.modify_world_state.value and name in route_2_modification.keys():
        return route_2_modification[name]
    if "Block Tunnels" in world.options.modify_world_state.value and name in block_tunnels.keys():
        return block_tunnels[name]
    if "Block Tower" in world.options.modify_world_state.value and name in block_pokemon_tower.keys():
        return block_pokemon_tower[name]
    if "Route 23 Trees" in world.options.modify_world_state.value and name in rotue_23_trees.keys():
        return rotue_23_trees[name]
    if "Modify Route 23" in world.options.modify_world_state.value and name in route_23_modification.keys():
        return route_23_modification[name]
    return name
