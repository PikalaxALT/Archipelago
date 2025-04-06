"""
Archipelago World definition for Pokémon FireRed/LeafGreen
"""
import base64
import copy
import logging
import os.path
import pkgutil
import settings
import threading

from collections import defaultdict
from typing import Any, ClassVar, Dict, List, Set, TextIO

from BaseClasses import CollectionState, ItemClassification, LocationProgressType, MultiWorld, Tutorial
from Fill import fill_restrictive, FillError
from worlds.AutoWorld import WebWorld, World
from entrance_rando import ERPlacementState
from .client import PokemonFRLGClient
from .data import (data as frlg_data, ability_name_map, ALL_SPECIES, LEGENDARY_POKEMON, NAME_TO_SPECIES_ID,
                   LocationCategory, EventData, EvolutionMethodEnum, FlyData, MapData, MiscPokemonData, MoveData,
                   move_name_map, SpeciesData, StarterData, TrainerData, TradePokemonData)
from .entrances import shuffle_entrances
from .groups import item_groups, location_groups
from .items import PokemonFRLGItem, create_item_name_to_id_map, get_random_item, get_item_classification
from .level_scaling import level_scaling
from .locations import (PokemonFRLGLocation, create_location_name_to_id_map, create_locations_from_categories,
                        set_free_fly)
from .logic import (can_evolve, can_cut, can_flash, can_fly, can_rock_smash, can_strength, can_surf, can_waterfall,
                    has_badge_requirement, has_pokemon, set_allowed_evo_methods)
from .options import (PokemonFRLGOptions, CeruleanCaveRequirement, Dexsanity, DungeonEntranceShuffle, FlashRequired,
                      FreeFlyLocation, GameVersion, Goal, RandomizeLegendaryPokemon, RandomizeMiscPokemon,
                      RandomizeWildPokemon, SeviiIslandPasses, ShuffleFlyUnlocks, ShuffleHiddenItems, ShuffleBadges,
                      ShuffleRunningShoes, SilphCoCardKey, TownMapFlyLocation, Trainersanity, ViridianCityRoadblock)
from .pokemon import (add_hm_compatability, randomize_abilities, randomize_damage_categories, randomize_legendaries,
                      randomize_misc_pokemon, randomize_moves, randomize_move_types, randomize_requested_trade_pokemon,
                      randomize_starters, randomize_tm_hm_compatibility, randomize_tm_moves, randomize_trainer_parties,
                      randomize_types, randomize_wild_encounters)
from .regions import starting_town_map, create_indirect_conditions, create_regions
from .rules import set_evolution_rules, set_rules
from .rom import get_tokens, PokemonFireRedProcedurePatch, PokemonLeafGreenProcedurePatch
from .sanity_check import validate_regions
from .util import int_to_bool_array, HM_TO_COMPATIBILITY_ID


class PokemonFRLGWebWorld(WebWorld):
    """
    Webhost info for Pokémon FireRed and LeafGreen
    """
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokémon FireRed and LeafGreen with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Vyneras"]
    )

    tutorials = [setup_en]


class PokemonFRLGSettings(settings.Group):
    class PokemonFireRedRomFile(settings.UserFilePath):
        """File name of your English Pokémon FireRed ROM"""
        description = "Pokemon FireRed ROM File"
        copy_to = "Pokemon - FireRed Version (USA, Europe).gba"
        md5s = PokemonFireRedProcedurePatch.hash

    class PokemonLeafGreenRomFile(settings.UserFilePath):
        """File name of your English Pokémon LeafGreen ROM"""
        description = "Pokemon LeafGreen ROM File"
        copy_to = "Pokemon - LeafGreen Version (USA, Europe).gba"
        md5s = PokemonLeafGreenProcedurePatch.hash

    firered_rom_file: PokemonFireRedRomFile = PokemonFireRedRomFile(PokemonFireRedRomFile.copy_to)
    leafgreen_rom_file: PokemonLeafGreenRomFile = PokemonLeafGreenRomFile(PokemonLeafGreenRomFile.copy_to)


class PokemonFRLGWorld(World):
    """
    Pokémon FireRed and LeafGreen are remakes of the very first Pokémon games.
    Experience the Kanto region with several updated features from Gen III.
    Catch, train, and battle Pokémon, face off against the evil organization Team Rocket, challenge Gyms in order to
    earn Badges, help resolve the many crises on the Sevii Islands, and become the Pokémon Champion!
    """
    game = "Pokemon FireRed and LeafGreen"
    web = PokemonFRLGWebWorld()
    topology_present = True

    settings_key = "pokemon_frlg_settings"
    settings: ClassVar[PokemonFRLGSettings]

    options_dataclass = PokemonFRLGOptions
    options: PokemonFRLGOptions

    item_name_to_id = create_item_name_to_id_map()
    location_name_to_id = create_location_name_to_id_map()
    item_name_groups = item_groups
    location_name_groups = location_groups

    required_client_version = (0, 6, 0)
    origin_region_name = "Title Screen"

    starting_town: str
    free_fly_location_id: int
    town_map_fly_location_id: int
    resort_gorgeous_mon: int
    modified_species: Dict[int, SpeciesData]
    modified_maps: Dict[str, MapData]
    modified_starters: Dict[str, StarterData]
    modified_events: Dict[str, EventData]
    modified_legendary_pokemon: Dict[str, MiscPokemonData]
    modified_misc_pokemon: Dict[str, MiscPokemonData]
    modified_trade_pokemon: Dict[str, TradePokemonData]
    modified_trainers: Dict[str, TrainerData]
    modified_tmhm_moves: List[int]
    modified_moves: Dict[str, MoveData]
    modified_type_damage_categories: List[int]
    hm_compatibility: Dict[str, Set[str]]
    repeatable_pokemon: List[str]
    per_species_tmhm_moves: Dict[int, List[int]]
    blacklisted_wild_pokemon: Set[int]
    blacklisted_starters: Set[int]
    blacklisted_trainer_pokemon: Set[int]
    blacklisted_abilities: Set[int]
    blacklisted_moves: Set[int]
    trainer_name_level_dict: Dict[str, int]
    trainer_name_list: List[str]
    trainer_level_list: List[int]
    encounter_name_level_dict: Dict[str, int]
    encounter_name_list: List[str]
    encounter_level_list: List[int]
    itempool: List[PokemonFRLGItem]
    pre_fill_items: List[PokemonFRLGItem]
    fly_destination_data: Dict[str, FlyData]
    er_placement_state: ERPlacementState | None
    er_spoiler_names: List[str]
    allowed_evo_methods: List[EvolutionMethodEnum]
    moves_by_type: Dict[int, Set[int]]
    required_trade_pokemon: Dict[str, str]
    randomizing_entrances: bool
    shop_locations_by_spheres: List[Set[PokemonFRLGLocation]]
    auth: bytes

    def __init__(self, multiworld, player):
        super(PokemonFRLGWorld, self).__init__(multiworld, player)
        self.starting_town = "SPAWN_PALLET_TOWN"
        self.free_fly_location_id = 0
        self.town_map_fly_location_id = 0
        self.resort_gorgeous_mon = frlg_data.constants["SPECIES_PIKACHU"]
        self.modified_species = copy.deepcopy(frlg_data.species)
        self.modified_maps = copy.deepcopy(frlg_data.maps)
        self.modified_starters = copy.deepcopy(frlg_data.starters)
        self.modified_events = copy.deepcopy(frlg_data.events)
        self.modified_legendary_pokemon = copy.deepcopy(frlg_data.legendary_pokemon)
        self.modified_misc_pokemon = copy.deepcopy(frlg_data.misc_pokemon)
        self.modified_trade_pokemon = copy.deepcopy(frlg_data.trade_pokemon)
        self.modified_trainers = copy.deepcopy(frlg_data.trainers)
        self.modified_tmhm_moves = copy.deepcopy(frlg_data.tmhm_moves)
        self.modified_moves = copy.deepcopy(frlg_data.moves)
        self.modified_type_damage_categories = copy.deepcopy(frlg_data.type_damage_categories)
        self.hm_compatibility = {}
        self.repeatable_pokemon = []
        self.per_species_tmhm_moves = {}
        self.trainer_name_level_dict = {}
        self.trainer_name_list = []
        self.trainer_level_list = []
        self.encounter_name_level_dict = {}
        self.encounter_name_list = []
        self.encounter_level_list = []
        self.itempool = []
        self.pre_fill_items = []
        self.fly_destination_data = {}
        self.er_placement_state = None
        self.er_spoiler_names = []
        self.allowed_evo_methods = []
        self.moves_by_type = {}
        self.required_trade_pokemon = {}
        self.randomizing_entrances = False
        self.shop_locations_by_spheres = []
        self.finished_level_scaling = threading.Event()

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        assert validate_regions()

    def get_filler_item_name(self) -> str:
        return get_random_item(self, ItemClassification.filler)

    def generate_early(self) -> None:
        self.blacklisted_wild_pokemon = {
            species.species_id for species in self.modified_species.values()
            if species.name in self.options.wild_pokemon_blacklist.value
        }
        if "Legendaries" in self.options.wild_pokemon_blacklist.value:
            self.blacklisted_wild_pokemon |= LEGENDARY_POKEMON

        self.blacklisted_starters = {
            species.species_id for species in self.modified_species.values()
            if species.name in self.options.starter_blacklist.value
        }
        if "Legendaries" in self.options.starter_blacklist.value:
            self.blacklisted_starters |= LEGENDARY_POKEMON

        self.blacklisted_trainer_pokemon = {
            species.species_id for species in self.modified_species.values()
            if species.name in self.options.trainer_blacklist.value
        }
        if "Legendaries" in self.options.trainer_blacklist.value:
            self.blacklisted_trainer_pokemon |= LEGENDARY_POKEMON

        self.blacklisted_abilities = {ability_name_map[name] for name in self.options.ability_blacklist.value}
        self.blacklisted_moves = {move_name_map[name] for name in self.options.move_blacklist.value}

        # Modify options that are incompatible with each other
        if self.options.kanto_only:
            if self.options.goal == Goal.option_champion_rematch:
                logging.warning("Pokemon FRLG: Goal for player %s (%s) incompatible with Kanto Only. "
                                "Setting goal to Champion.", self.player, self.player_name)
                self.options.goal.value = Goal.option_champion
            if (self.options.cerulean_cave_requirement == CeruleanCaveRequirement.option_vanilla or
                    self.options.cerulean_cave_requirement == CeruleanCaveRequirement.option_restore_network):
                logging.warning("Pokemon FRLG: Cerulean Cave Requirement for player %s (%s) "
                                "incompatible with Kanto Only. Setting requirement to Defeat Champion.",
                                self.player, self.player_name)
                self.options.cerulean_cave_requirement.value = CeruleanCaveRequirement.option_champion

        # Remove items from start inventory that are incompatible with certain settings
        card_key_vanilla = ["Card Key"]
        card_key_split = ["Card Key 2F", "Card Key 3F", "Card Key 4F", "Card Key 5F", "Card Key 6F",
                          "Card Key 7F", "Card Key 8F", "Card Key 9F", "Card Key 10F", "Card Key 11F"]
        card_key_progressive = ["Progressive Card Key"]
        passes_vanilla = ["Tri Pass", "Rainbow Pass"]
        passes_split = ["One Pass", "Two Pass", "Three Pass", "Four Pass", "Five Pass", "Six Pass", "Seven Pass"]
        passes_progressive = ["Progressive Pass"]
        tea_vanilla = ["Tea"]
        tea_split = ["Blue Tea", "Green Tea", "Purple Tea", "Red Tea"]
        not_allowed_card_key = []
        not_allowed_pass = []
        not_allowed_tea = []

        if self.options.card_key == SilphCoCardKey.option_vanilla:
            not_allowed_card_key.extend(card_key_split)
            not_allowed_card_key.extend(card_key_progressive)
        elif self.options.card_key == SilphCoCardKey.option_split:
            not_allowed_card_key.extend(card_key_vanilla)
            not_allowed_card_key.extend(card_key_progressive)
        elif self.options.card_key == SilphCoCardKey.option_progressive:
            not_allowed_card_key.extend(card_key_vanilla)
            not_allowed_card_key.extend(card_key_split)

        if not self.options.kanto_only:
            if self.options.island_passes == SeviiIslandPasses.option_vanilla:
                not_allowed_pass.extend(passes_split)
                not_allowed_pass.extend(passes_progressive)
            elif self.options.island_passes == SeviiIslandPasses.option_split:
                not_allowed_pass.extend(passes_vanilla)
                not_allowed_pass.extend(passes_progressive)
            elif (self.options.island_passes == SeviiIslandPasses.option_progressive or
                  self.options.island_passes == SeviiIslandPasses.option_progressive_split):
                not_allowed_pass.extend(passes_vanilla)
                not_allowed_pass.extend(passes_split)
        else:
            not_allowed_pass.extend(passes_vanilla)
            not_allowed_pass.extend(passes_split)
            not_allowed_pass.extend(passes_progressive)

        if self.options.split_teas:
            not_allowed_tea.extend(tea_vanilla)
        else:
            not_allowed_tea.extend(tea_split)

        self.options.start_inventory.value = {k: v for k, v in self.options.start_inventory.value.items()
                                              if k not in not_allowed_card_key}
        self.options.start_inventory.value = {k: v for k, v in self.options.start_inventory.value.items()
                                              if k not in not_allowed_pass}
        self.options.start_inventory.value = {k: v for k, v in self.options.start_inventory.value.items()
                                              if k not in not_allowed_tea}

        # Remove badges from non-local items if they are shuffled among gyms
        if not self.options.shuffle_badges:
            self.options.local_items.value.update(item_groups["Badges"])

        # Add starting items from settings
        if self.options.shuffle_running_shoes == ShuffleRunningShoes.option_start_with:
            self.options.start_inventory.value["Running Shoes"] = 1

        if (self.options.viridian_city_roadblock == ViridianCityRoadblock.option_early_parcel and
                not self.options.random_starting_town):
            self.multiworld.local_early_items[self.player]["Oak's Parcel"] = 1

        set_allowed_evo_methods(self)
        randomize_types(self)
        randomize_abilities(self)
        randomize_move_types(self)
        randomize_damage_categories(self)
        randomize_moves(self)
        randomize_wild_encounters(self)
        randomize_starters(self)
        randomize_legendaries(self)
        randomize_misc_pokemon(self)
        randomize_tm_hm_compatibility(self)
        self.create_hm_compatibility_dict()

    def create_regions(self) -> None:
        regions = create_regions(self)

        categories = {
            LocationCategory.BADGE,
            LocationCategory.HM,
            LocationCategory.KEY_ITEM,
            LocationCategory.FLY_UNLOCK,
            LocationCategory.ITEM_BALL,
            LocationCategory.STARTING_ITEM,
            LocationCategory.NPC_GIFT
        }
        if self.options.shuffle_hidden == ShuffleHiddenItems.option_all:
            categories.update([LocationCategory.HIDDEN_ITEM, LocationCategory.HIDDEN_ITEM_RECURRING])
        elif self.options.shuffle_hidden == ShuffleHiddenItems.option_nonrecurring:
            categories.add(LocationCategory.HIDDEN_ITEM)
        if self.options.extra_key_items:
            categories.add(LocationCategory.EXTRA_KEY_ITEM)
        if self.options.shopsanity:
            categories.add(LocationCategory.SHOPSANITY)
        if self.options.trainersanity != Trainersanity.special_range_names["none"]:
            categories.add(LocationCategory.TRAINERSANITY)
        if self.options.dexsanity != Dexsanity.special_range_names["none"]:
            categories.add(LocationCategory.DEXSANITY)
        if self.options.famesanity:
            categories.add(LocationCategory.FAMESANITY)
            if self.options.pokemon_request_locations:
                categories.add(LocationCategory.FAMESANITY_POKEMON_REQUEST)
        if self.options.pokemon_request_locations:
            categories.add(LocationCategory.POKEMON_REQUEST)
        if self.options.card_key != SilphCoCardKey.option_vanilla:
            categories.add(LocationCategory.SPLIT_CARD_KEY)
        if (self.options.island_passes == SeviiIslandPasses.option_split or
                self.options.island_passes == SeviiIslandPasses.option_progressive_split):
            categories.add(LocationCategory.SPLIT_ISLAND_PASS)
        if self.options.split_teas:
            categories.add(LocationCategory.SPLIT_TEA)
        if self.options.shuffle_running_shoes != ShuffleRunningShoes.option_vanilla:
            categories.add(LocationCategory.RUNNING_SHOES)
        if self.options.gym_keys:
            categories.add(LocationCategory.GYM_KEY)
        create_locations_from_categories(self, regions, categories)

        self.multiworld.regions.extend(regions.values())

        create_indirect_conditions(self)

        # Choose Selphy's requested Pokémon among available wild encounters if necessary
        if self.options.pokemon_request_locations and not self.options.kanto_only:
            self.resort_gorgeous_mon = NAME_TO_SPECIES_ID[self.random.choice(self.repeatable_pokemon)]

        randomize_requested_trade_pokemon(self)

        self.fill_unrandomized_locations()

        def exclude_locations(locations: List[str]):
            for location in locations:
                try:
                    self.multiworld.get_location(location, self.player).progress_type = LocationProgressType.EXCLUDED
                except KeyError:
                    continue

        if self.options.goal == Goal.option_champion:
            exclude_locations([
                "Lorelei's Room - Elite Four Lorelei Rematch Reward",
                "Bruno's Room - Elite Four Bruno Rematch Reward",
                "Agatha's Room - Elite Four Agatha Rematch Reward",
                "Lance's Room - Elite Four Lance Rematch Reward",
                "Champion's Room - Champion Rematch Reward",
                "Two Island Town - Beauty Info"
            ])

            if ((self.options.cerulean_cave_requirement == CeruleanCaveRequirement.option_vanilla
                    or self.options.cerulean_cave_requirement == CeruleanCaveRequirement.option_champion)
                    and self.options.dungeon_entrance_shuffle == DungeonEntranceShuffle.option_off):
                exclude_locations([
                    "Cerulean Cave 1F - Southwest Item",
                    "Cerulean Cave 1F - East Plateau Item",
                    "Cerulean Cave 1F - West Plateau Item",
                    "Cerulean Cave 2F - East Item",
                    "Cerulean Cave 2F - West Item",
                    "Cerulean Cave 2F - Center Item",
                    "Cerulean Cave B1F - Northeast Item",
                    "Cerulean Cave B1F - East Plateau Item",
                    "Cerulean Cave 1F - West Plateau Hidden Item"
                ])

            if "Early Gossipers" not in self.options.modify_world_state.value:
                exclude_locations([
                    "Professor Oak's Lab - Oak's Aide M Info (Right)",
                    "Professor Oak's Lab - Oak's Aide M Info (Left)",
                    "Cerulean Pokemon Center 1F - Bookshelf Info",
                    "Pokemon Fan Club - Worker Info",
                    "Lavender Pokemon Center 1F - Balding Man Info",
                    "Celadon Condominiums 1F - Tea Woman Info",
                    "Celadon Department Store 2F - Woman Info",
                    "Fuchsia City - Koga's Daughter Info",
                    "Pokemon Trainer Fan Club - Bookshelf Info",
                    "Saffron City - Battle Girl Info",
                    "Cinnabar Pokemon Center 1F - Bookshelf Info",
                    "Indigo Plateau Pokemon Center 1F - Black Belt Info 1",
                    "Indigo Plateau Pokemon Center 1F - Black Belt Info 2",
                    "Indigo Plateau Pokemon Center 1F - Bookshelf Info",
                    "Indigo Plateau Pokemon Center 1F - Cooltrainer Info",
                    "Ember Spa - Black Belt Info",
                    "Five Island Pokemon Center 1F - Bookshelf Info",
                    "Seven Island Pokemon Center 1F - Bookshelf Info"
                ])

    def fill_unrandomized_locations(self) -> None:
        def create_events_for_unrandomized_items(locations: Set[PokemonFRLGLocation]) -> None:
            for location in locations:
                location.place_locked_item(PokemonFRLGItem(self.item_id_to_name[location.default_item_id],
                                                           ItemClassification.progression,
                                                           None,
                                                           self.player))
                location.progress_type = LocationProgressType.DEFAULT
                location.address = None
                location.show_in_spoiler = False

        unrandomized_progression_locations = set()

        if self.options.shuffle_fly_unlocks == ShuffleFlyUnlocks.option_off:
            fly_locations = [loc for loc in self.get_locations() if loc.name in location_groups["Town Visits"]]
            unrandomized_progression_locations.update(fly_locations)
        elif self.options.shuffle_fly_unlocks == ShuffleFlyUnlocks.option_exclude_indigo:
            unrandomized_progression_locations.add(self.get_location("Indigo Plateau - Unlock Fly Destination"))

        if not self.options.shuffle_berry_pouch:
            unrandomized_progression_locations.add(self.get_location("Title Screen - Starting Item 1"))
        if not self.options.shuffle_tm_case:
            unrandomized_progression_locations.add(self.get_location("Title Screen - Starting Item 2"))

        create_events_for_unrandomized_items(unrandomized_progression_locations)

    def create_items(self) -> None:
        item_locations: List[PokemonFRLGLocation] = [
            location for location in self.get_locations() if location.address is not None
        ]

        self.itempool = [self.create_item_by_id(location.default_item_id) for location in item_locations]

        items_to_remove: List[PokemonFRLGItem] = list()
        items_to_add: List[PokemonFRLGItem] = list()

        if not self.options.shuffle_badges:
            badge_items = [self.create_item(badge) for badge in item_groups["Badges"]]
            items_to_remove.extend(badge_items)
            self.pre_fill_items.extend(badge_items)

        if self.options.card_key == SilphCoCardKey.option_split:
            items_to_remove.append(self.create_item("Card Key"))
            items_to_add.append(self.create_item("Card Key 3F"))
        elif self.options.card_key == SilphCoCardKey.option_progressive:
            for item in ["Card Key", "Card Key 2F", "Card Key 4F", "Card Key 5F", "Card Key 6F", "Card Key 7F",
                         "Card Key 8F", "Card Key 9F", "Card Key 10F", "Card Key 11F"]:
                items_to_remove.append(self.create_item(item))
            for _ in range(10):
                items_to_add.append(self.create_item("Progressive Card Key"))

        if not self.options.kanto_only:
            if self.options.island_passes == SeviiIslandPasses.option_progressive:
                for item in ["Tri Pass", "Rainbow Pass"]:
                    items_to_remove.append(self.create_item(item))
                for _ in range(2):
                    items_to_add.append(self.create_item("Progressive Pass"))
            elif self.options.island_passes == SeviiIslandPasses.option_split:
                for item in ["Tri Pass", "Rainbow Pass"]:
                    items_to_remove.append(self.create_item(item))
                for item in ["Three Pass", "Four Pass"]:
                    items_to_add.append(self.create_item(item))
            elif self.options.island_passes == SeviiIslandPasses.option_progressive_split:
                for item in ["Tri Pass", "One Pass", "Two Pass", "Rainbow Pass", "Five Pass", "Six Pass", "Seven Pass"]:
                    items_to_remove.append(self.create_item(item))
                for _ in range(7):
                    items_to_add.append(self.create_item("Progressive Pass"))

        if self.options.split_teas:
            items_to_remove.append(self.create_item("Tea"))
            items_to_add.append(self.create_item("Green Tea"))

        if self.options.gym_keys:
            items_to_remove.append(self.create_item("Secret Key"))
            items_to_add.append(self.create_item("Cinnabar Key"))

        for item in items_to_remove:
            self.itempool.remove(item)
        for item in items_to_add:
            self.itempool.append(item)

        # Remove duplicates of unique items from the itempool
        unique_items = set()
        for item in self.itempool.copy():
            if item.name in item_groups["Unique Items"]:
                if item in unique_items:
                    self.itempool.remove(item)
                    self.itempool.append(self.create_item(get_random_item(self, ItemClassification.filler)))
                else:
                    unique_items.add(item)

        filler_items = [item for item in self.itempool if item.classification == ItemClassification.filler and
                        item.name not in item_groups["Unique Items"]]
        self.random.shuffle(filler_items)

        # Add key items that are relevant in Kanto Only to the itempool
        if self.options.kanto_only:
            items_to_add = ["HM06 Rock Smash", "HM07 Waterfall", "Sun Stone"]
            for item_name in items_to_add:
                self.itempool.append(self.create_item(item_name))
                self.itempool.remove(filler_items.pop(0))

        # Remove copies of unique and progressive items based on how many are in the start inventory
        for item_name, quantity in self.options.start_inventory.value.items():
            if item_name in item_groups["Unique Items"] or item_name in item_groups["Progressive Items"]:
                removed_items_count = 0
                for _ in range(quantity):
                    try:
                        item_to_remove = next(i for i in self.itempool if i.name == item_name)
                        self.itempool.remove(item_to_remove)
                        removed_items_count += 1
                    except StopIteration:
                        break
                while removed_items_count > 0:
                    self.itempool.append(self.create_item(get_random_item(self, ItemClassification.filler)))
                    removed_items_count -= 1

        # Set evolution rules now, so we can know what evolutions are impossible in an all state
        set_evolution_rules(self)

        state = self.get_world_collection_state()
        filler_items = [item for item in self.itempool if item.classification == ItemClassification.filler and
                        item.name not in item_groups["Unique Items"]]
        self.random.shuffle(filler_items)

        # Delete evolutions that are not in logic in an all state so that the accessibility check doesn't fail
        evolution_region = self.multiworld.get_region("Evolutions", self.player)
        for location in evolution_region.locations.copy():
            pokemon = location.name.split(" - ")[1].strip()
            if not can_evolve(state, self, pokemon):
                evolution_region.locations.remove(location)

        # Delete trainersanity locations if there are more than the amount specified in the settings
        if self.options.trainersanity != Trainersanity.special_range_names["none"]:
            locations: List[PokemonFRLGLocation] = self.get_locations()
            trainer_locations = [loc for loc in locations if loc.category == LocationCategory.TRAINERSANITY]
            locs_to_remove = len(trainer_locations) - self.options.trainersanity.value
            if locs_to_remove > 0:
                priority_trainer_locations = [loc for loc in trainer_locations
                                              if loc.name in self.options.priority_locations.value]
                non_priority_trainer_locations = [loc for loc in trainer_locations
                                                  if loc.name not in self.options.priority_locations.value]
                self.random.shuffle(priority_trainer_locations)
                self.random.shuffle(non_priority_trainer_locations)
                trainer_locations = non_priority_trainer_locations + priority_trainer_locations
                for location in trainer_locations:
                    region = location.parent_region
                    region.locations.remove(location)
                    self.itempool.remove(filler_items.pop(0))
                    locs_to_remove -= 1
                    if locs_to_remove <= 0:
                        break

        if self.options.dexsanity != Dexsanity.special_range_names["none"]:
            # Delete dexsanity locations that are not in logic in an all state since they aren't accessible
            evos_allowed = "Dexsanity" in self.options.evolutions_required.value
            pokedex_region = self.multiworld.get_region("Pokedex", self.player)
            for location in pokedex_region.locations.copy():
                pokemon = location.name.split(" - ")[1].strip()
                if not has_pokemon(state, self, evos_allowed, pokemon):
                    pokedex_region.locations.remove(location)
                    self.itempool.remove(filler_items.pop(0))

            # Delete dexsanity locations if there are more than the amount specified in the settings
            if len(pokedex_region.locations) > self.options.dexsanity.value:
                pokedex_locations = pokedex_region.locations.copy()
                priority_pokedex_locations = [loc for loc in pokedex_locations
                                              if loc.name in self.options.priority_locations.value]
                non_priority_pokedex_locations = [loc for loc in pokedex_locations
                                                  if loc.name not in self.options.priority_locations.value]
                self.random.shuffle(priority_pokedex_locations)
                self.random.shuffle(non_priority_pokedex_locations)
                pokedex_locations = non_priority_pokedex_locations + priority_pokedex_locations
                for location in pokedex_locations:
                    pokedex_region.locations.remove(location)
                    self.itempool.remove(filler_items.pop(0))
                    if len(pokedex_region.locations) <= self.options.dexsanity.value:
                        break

        self.multiworld.itempool += self.itempool

    def set_rules(self) -> None:
        set_rules(self)

    def connect_entrances(self) -> None:
        self.verify_hm_accessibility()
        set_free_fly(self)
        if not self.options.shuffle_badges:
            self.shuffle_badges()
        if self.options.dungeon_entrance_shuffle != DungeonEntranceShuffle.option_off:
            shuffle_entrances(self)
            self.verify_hm_accessibility()

    def shuffle_badges(self) -> None:
        badge_items = list()
        badge_items.extend(self.get_pre_fill_items())
        self.pre_fill_items.clear()
        locations: List[PokemonFRLGLocation] = self.get_locations()
        for attempt in range(5):
            badge_locations: List[PokemonFRLGLocation] = [
                loc for loc in locations if loc.category == LocationCategory.BADGE and loc.item is None
            ]
            state = self.get_world_collection_state()
            # Try to place badges with current Pokemon and HM access
            # If it can't, try with all Pokemon collected and fix the HM access after
            if attempt > 1:
                for species in frlg_data.species.values():
                    state.collect(PokemonFRLGItem(species.name,
                                                      ItemClassification.progression_skip_balancing,
                                                      None,
                                                      self.player))
            state.sweep_for_advancements()
            self.random.shuffle(badge_items)
            self.random.shuffle(badge_locations)
            fill_restrictive(self.multiworld, state, badge_locations.copy(), badge_items,
                             single_player_placement=True, lock=True, allow_partial=True, allow_excluded=True)
            if len(badge_items) > 8 - len(badge_locations):
                for location in badge_locations:
                    if location.item:
                        badge_items.append(location.item)
                        location.item = None
                continue
            else:
                break
        else:
            raise FillError(f"Failed to place badges for player {self.player}")
        self.verify_hm_accessibility()

    def generate_basic(self) -> None:
        # Create auth
        self.auth = self.random.getrandbits(16 * 8).to_bytes(16, "little")

    @classmethod
    def stage_post_fill(cls, multiworld):
        # Change all but one instance of a Pokémon in each sphere to useful classification
        # This cuts down on time calculating the playthrough
        found_mons = set()
        pokemon = {species.name for species in frlg_data.species.values()}
        shop_locations: Dict[int, List[Set[PokemonFRLGLocation]]] = defaultdict(list)
        for sphere in multiworld.get_spheres():
            mon_locations_in_sphere = defaultdict(list)
            shop_locations_in_sphere = defaultdict(set)
            for location in sphere:
                if location.game == "Pokemon FireRed and LeafGreen":
                    assert isinstance(location, PokemonFRLGLocation)
                    if (location.item.game == "Pokemon FireRed and LeafGreen" and
                            (location.item.name in pokemon or
                             "Static " in location.item.name or
                             "Evolved " in location.item.name)
                            and location.item.advancement):
                        key = (location.player, location.item.name)
                        if key in found_mons:
                            location.item.classification = ItemClassification.useful
                        else:
                            mon_locations_in_sphere[key].append(location)
                    if location.category == LocationCategory.SHOPSANITY:
                        shop_locations_in_sphere[location.player].add(location)
            for key, mon_locations in mon_locations_in_sphere.items():
                found_mons.add(key)
                if len(mon_locations) > 1:
                    mon_locations.sort()
                    for location in mon_locations[1:]:
                        location.item.classification = ItemClassification.useful
            for player, locations in shop_locations_in_sphere.items():
                shop_locations[player].append(locations)
        for world in multiworld.get_game_worlds("Pokemon FireRed and LeafGreen"):
            if world.options.shopsanity:
                world.shop_locations_by_spheres = shop_locations[world.player]

    @classmethod
    def stage_generate_output(cls, multiworld, output_directory):
        level_scaling(multiworld)

    def generate_output(self, output_directory: str) -> None:
        # Modify catch rate
        min_catch_rate = min(self.options.min_catch_rate.value, 255)
        for species in self.modified_species.values():
            species.catch_rate = max(species.catch_rate, min_catch_rate)

        self.finished_level_scaling.wait()

        randomize_tm_moves(self)
        randomize_trainer_parties(self)

        if self.options.game_version == GameVersion.option_firered:
            patch = PokemonFireRedProcedurePatch(player=self.player, player_name=self.player_name)
            patch.write_file("base_patch_rev0.bsdiff4",
                             pkgutil.get_data(__name__, "data/base_patch_firered.bsdiff4"))
            patch.write_file("base_patch_rev1.bsdiff4",
                             pkgutil.get_data(__name__, "data/base_patch_firered_rev1.bsdiff4"))
        else:
            patch = PokemonLeafGreenProcedurePatch(player=self.player, player_name=self.player_name)
            patch.write_file("base_patch_rev0.bsdiff4",
                             pkgutil.get_data(__name__, "data/base_patch_leafgreen.bsdiff4"))
            patch.write_file("base_patch_rev1.bsdiff4",
                             pkgutil.get_data(__name__, "data/base_patch_leafgreen_rev1.bsdiff4"))

        tokens_rev0 = get_tokens(self, 0)
        tokens_rev1 = get_tokens(self, 1)

        patch.write_file("token_data_rev0.bin", tokens_rev0.get_token_binary())
        patch.write_file("token_data_rev1.bin", tokens_rev1.get_token_binary())

        # Write output
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))

        del self.modified_species
        del self.modified_maps
        del self.modified_starters
        del self.modified_events
        del self.modified_legendary_pokemon
        del self.modified_misc_pokemon
        del self.modified_trade_pokemon
        del self.modified_trainers
        del self.modified_tmhm_moves
        del self.modified_moves
        del self.modified_type_damage_categories

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if self.options.random_starting_town:
            starting_town = starting_town_map[self.starting_town]
            if starting_town == "Viridian City South" or starting_town == "Three Island Town South":
                starting_town = starting_town[:-6]
            spoiler_handle.write(f"Starting Town:                   {starting_town}\n")
        if self.options.free_fly_location:
            free_fly_location = self.multiworld.get_location("Free Fly Location", self.player)
            spoiler_handle.write(f"Free Fly Location:               {free_fly_location.item.name[4:]}\n")
        if self.options.town_map_fly_location:
            town_map_fly_location = self.multiworld.get_location("Town Map Fly Location", self.player)
            spoiler_handle.write(f"Town Map Fly Location:           {town_map_fly_location.item.name[4:]}\n")

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        # Add dungeon entrances to the spoiler log if they are shuffled
        if self.options.dungeon_entrance_shuffle != DungeonEntranceShuffle.option_off:
            spoiler_handle.write(f"\n\nDungeon Entrances ({self.multiworld.player_name[self.player]}):\n\n")
            for entrance, exit in self.er_placement_state.pairings:
                if entrance in self.er_spoiler_names:
                    spoiler_handle.write(f"{entrance} <=> {exit}\n")

        # Add fly destinations to the spoiler log if they are randomized
        if self.options.randomize_fly_destinations:
            spoiler_handle.write(f"\n\nFly Destinations ({self.multiworld.player_name[self.player]}):\n\n")
            for exit in self.get_region("Sky").exits:
                spoiler_handle.write(f"{exit.name}: {exit.connected_region.name}\n")

        wild_pokemon_randomized = self.options.wild_pokemon != RandomizeWildPokemon.option_vanilla
        static_pokemon_randomized = self.options.misc_pokemon != RandomizeMiscPokemon.option_vanilla
        legendary_pokemon_randomized = self.options.legendary_pokemon != RandomizeLegendaryPokemon.option_vanilla

        # Add Pokémon locations to the spoiler log if they are not vanilla
        if wild_pokemon_randomized or static_pokemon_randomized or legendary_pokemon_randomized:
            spoiler_handle.write(f"\n\nPokemon Locations ({self.multiworld.player_name[self.player]}):\n\n")

            species_locations = defaultdict(set)

            for location in self.get_locations():
                assert isinstance(location, PokemonFRLGLocation)
                if ((wild_pokemon_randomized and
                     location.category == LocationCategory.EVENT_WILD_POKEMON) or
                        (static_pokemon_randomized and
                         location.category == LocationCategory.EVENT_STATIC_POKEMON) or
                        (legendary_pokemon_randomized and
                         location.category == LocationCategory.EVENT_LEGENDARY_POKEMON)):
                    if location.item.name.startswith("Missable"):
                        continue
                    pokemon_name = location.item.name.replace("Static ", "")
                    species_locations[pokemon_name].add(location.spoiler_name)

            lines = [f"{species}: {', '.join(sorted(locations))}\n"
                     for species, locations in species_locations.items()]
            lines.sort()
            for line in lines:
                spoiler_handle.write(line)

    def extend_hint_information(self, hint_data):
        if self.options.dexsanity != Dexsanity.special_range_names["none"]:
            species_locations = defaultdict(set)

            for location in self.get_locations():
                assert isinstance(location, PokemonFRLGLocation)
                if location.category in [LocationCategory.EVENT_WILD_POKEMON,
                                         LocationCategory.EVENT_STATIC_POKEMON,
                                         LocationCategory.EVENT_LEGENDARY_POKEMON]:
                    if location.item.name.startswith("Missable"):
                        continue
                    pokemon_name = location.item.name.replace("Static ", "")
                    species_locations[pokemon_name].add(location.spoiler_name)

            hint_data[self.player] = {
                self.location_name_to_id[f"Pokedex - {species}"]: ", ".join(sorted(maps))
                for species, maps in species_locations.items()
            }

    def modify_multidata(self, multidata: Dict[str, Any]):
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = \
            multidata["connect_names"][self.player_name]

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            "game_version",
            "goal",
            "skip_elite_four",
            "kanto_only",
            "shuffle_badges",
            "shuffle_hidden",
            "extra_key_items",
            "shopsanity",
            "famesanity",
            "shuffle_fly_unlocks",
            "pokemon_request_locations",
            "shuffle_running_shoes",
            "shuffle_berry_pouch",
            "shuffle_tm_case",
            "card_key",
            "island_passes",
            "split_teas",
            "gym_keys",
            "itemfinder_required",
            "flash_required",
            "fame_checker_required",
            "remove_badge_requirement",
            "oaks_aide_route_2",
            "oaks_aide_route_10",
            "oaks_aide_route_11",
            "oaks_aide_route_16",
            "oaks_aide_route_15",
            "viridian_city_roadblock",
            "pewter_city_roadblock",
            "modify_world_state",
            "additional_dark_caves",
            "viridian_gym_requirement",
            "viridian_gym_count",
            "route22_gate_requirement",
            "route22_gate_count",
            "route23_guard_requirement",
            "route23_guard_count",
            "elite_four_requirement",
            "elite_four_count",
            "elite_four_rematch_count",
            "cerulean_cave_requirement",
            "cerulean_cave_count",
            "death_link",
            "provide_hints"
        )
        slot_data["trainersanity"] = 1 if self.options.trainersanity != Trainersanity.special_range_names["none"] else 0
        slot_data["elite_four_rematch_requirement"] = self.options.elite_four_requirement.value
        slot_data["starting_town"] = frlg_data.constants[self.starting_town]
        slot_data["free_fly_location_id"] = self.free_fly_location_id
        slot_data["town_map_fly_location_id"] = self.town_map_fly_location_id
        if self.options.randomize_fly_destinations:
            slot_data["randomize_fly_destinations"] = {}
            for exit in self.get_region("Sky").exits:
                slot_data["randomize_fly_destinations"][exit.name] = exit.connected_region.name
        if self.options.dungeon_entrance_shuffle != DungeonEntranceShuffle.option_off:
            slot_data["dungeon_entrance_shuffle"] = {}
            for source, dest in self.er_placement_state.pairings:
                slot_data["dungeon_entrance_shuffle"][source] = dest
        return slot_data

    def create_item(self, name: str) -> "PokemonFRLGItem":
        return self.create_item_by_id(self.item_name_to_id[name])

    def create_item_by_id(self, item_id: int):
        return PokemonFRLGItem(
            self.item_id_to_name[item_id],
            get_item_classification(item_id),
            item_id,
            self.player
        )

    def get_world_collection_state(self) -> CollectionState:
        state = CollectionState(self.multiworld)
        progression_items = [item for item in self.itempool if item.advancement]
        locations = self.get_locations()
        for item in progression_items:
            state.collect(item, True)
        for item in self.get_pre_fill_items():
            state.collect(item, True)
        state.sweep_for_advancements(locations)
        return state

    def get_pre_fill_items(self):
        return self.pre_fill_items

    def create_hm_compatibility_dict(self):
        hms = frozenset({"Cut", "Fly", "Surf", "Strength", "Flash", "Rock Smash", "Waterfall"})
        for hm in hms:
            self.hm_compatibility[hm] = set()
            for species in self.modified_species.values():
                combatibility_array = int_to_bool_array(species.tm_hm_compatibility)
                if combatibility_array[HM_TO_COMPATIBILITY_ID[hm]] == 1:
                    self.hm_compatibility[hm].add(species.name)

    def verify_hm_accessibility(self):
        def can_use_hm(state: CollectionState, hm: str):
            if hm == "Cut":
                return can_cut(state, self)
            elif hm == "Fly":
                return can_fly(state, self)
            elif hm == "Surf":
                return can_surf(state, self)
            elif hm == "Strength":
                return can_strength(state, self)
            elif hm == "Flash":
                return can_flash(state, self)
            elif hm == "Rock Smash":
                return can_rock_smash(state, self)
            elif hm == "Waterfall":
                return can_waterfall(state, self)

        hms: List[str] = ["Cut", "Fly", "Surf", "Strength", "Flash", "Rock Smash", "Waterfall"]
        self.random.shuffle(hms)
        last_hm_verified = None
        while len(hms) > 0:
            hm_to_verify = hms[0]
            state = self.get_world_collection_state()
            if (not can_use_hm(state, hm_to_verify) and
                    has_badge_requirement(state, self, hm_to_verify)):
                if hm_to_verify == last_hm_verified:
                    raise Exception(f"Failed to ensure access to {hm_to_verify} for player {self.player}")
                last_hm_verified = hm_to_verify
                valid_mons = [mon for mon in self.repeatable_pokemon if state.has(mon, self.player)]
                mon = self.random.choice(valid_mons)
                add_hm_compatability(self, mon, hm_to_verify)
                self.hm_compatibility[hm_to_verify].add(mon)
            else:
                hms.pop(0)
