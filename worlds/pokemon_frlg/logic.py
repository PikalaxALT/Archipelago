import re
from typing import TYPE_CHECKING, Dict, List
from BaseClasses import CollectionState
from .data import data, EvolutionMethodEnum
from .options import (CeruleanCaveRequirement, EliteFourRequirement, FlashRequired, PewterCityRoadblock,
                      Route22GateRequirement, Route23GuardRequirement, SeviiIslandPasses, ViridianCityRoadblock,
                      ViridianGymRequirement)

if TYPE_CHECKING:
    from . import PokemonFRLGWorld


badge_requirements: Dict[str, str] = {
    "Cut": "Cascade Badge",
    "Fly": "Thunder Badge",
    "Surf": "Soul Badge",
    "Strength": "Rainbow Badge",
    "Flash": "Boulder Badge",
    "Rock Smash": "Marsh Badge",
    "Waterfall": "Volcano Badge"
}

island_passes: Dict[int, List[str]] = {
    1: ["Tri Pass", "One Pass"],
    2: ["Tri Pass", "Two Pass"],
    3: ["Tri Pass", "Three Pass"],
    4: ["Rainbow Pass", "Four Pass"],
    5: ["Rainbow Pass", "Five Pass"],
    6: ["Rainbow Pass", "Six Pass"],
    7: ["Rainbow Pass", "Seven Pass"]
}

evo_methods_level = [
    EvolutionMethodEnum.LEVEL,
    EvolutionMethodEnum.LEVEL_NINJASK,
    EvolutionMethodEnum.LEVEL_SHEDINJA
]

evo_methods_tyrogue_level = [
    EvolutionMethodEnum.LEVEL_ATK_LT_DEF,
    EvolutionMethodEnum.LEVEL_ATK_EQ_DEF,
    EvolutionMethodEnum.LEVEL_ATK_GT_DEF
]

evo_methods_wurmple_level = [
    EvolutionMethodEnum.LEVEL_SILCOON,
    EvolutionMethodEnum.LEVEL_CASCOON
]

evo_methods_item = [
    EvolutionMethodEnum.ITEM
]

evo_methods_held_item = [
    EvolutionMethodEnum.ITEM_HELD
]

evo_methods_friendship = [
    EvolutionMethodEnum.FRIENDSHIP
]


def set_allowed_evo_methods(world: "PokemonFRLGWorld"):
    if "Level" in world.options.evolution_methods_required.value:
        world.allowed_evo_methods.extend(evo_methods_level)
    if "Level Tyrogue" in world.options.evolution_methods_required.value:
        world.allowed_evo_methods.extend(evo_methods_tyrogue_level)
    if "Level Wurmple" in world.options.evolution_methods_required.value:
        world.allowed_evo_methods.extend(evo_methods_wurmple_level)
    if "Evo Item" in world.options.evolution_methods_required.value:
        world.allowed_evo_methods.extend(evo_methods_item)
    if "Evo & Held Item" in world.options.evolution_methods_required.value:
        world.allowed_evo_methods.extend(evo_methods_held_item)
    if "Friendship" in world.options.evolution_methods_required.value:
        world.allowed_evo_methods.extend(evo_methods_friendship)


def has_badge_requirement(state: CollectionState, world: "PokemonFRLGWorld", hm: str):
    return hm in world.options.remove_badge_requirement.value or state.has(badge_requirements[hm], world.player)


def can_use_hm(state: CollectionState, world: "PokemonFRLGWorld", hm: str):
    evos_allowed = "HM Requirement" in world.options.evolutions_required.value
    for species in world.hm_compatibility[hm]:
        if state.has(species, world.player) or (state.has(f"Evolved {species}", world.player) and evos_allowed):
            return True
    return False


def can_cut(state: CollectionState, world: "PokemonFRLGWorld"):
    return (state.has_all(["HM01 Cut", "TM Case"], world.player) and
            has_badge_requirement(state, world, "Cut")
            and can_use_hm(state, world, "Cut"))


def can_fly(state: CollectionState, world: "PokemonFRLGWorld"):
    return (state.has_all(["HM02 Fly", "TM Case"], world.player) and
            has_badge_requirement(state, world, "Fly")
            and can_use_hm(state, world, "Fly"))


def can_surf(state: CollectionState, world: "PokemonFRLGWorld"):
    return (state.has_all(["HM03 Surf", "TM Case"], world.player) and
            has_badge_requirement(state, world, "Surf")
            and can_use_hm(state, world, "Surf"))


def can_strength(state: CollectionState, world: "PokemonFRLGWorld"):
    return (state.has_all(["HM04 Strength", "TM Case"], world.player) and
            has_badge_requirement(state, world, "Strength")
            and can_use_hm(state, world, "Strength"))


def can_flash(state: CollectionState, world: "PokemonFRLGWorld"):
    return (state.has_all(["HM05 Flash", "TM Case"], world.player) and
            has_badge_requirement(state, world, "Flash")
            and can_use_hm(state, world, "Flash"))


def can_rock_smash(state: CollectionState, world: "PokemonFRLGWorld"):
    return (state.has_all(["HM06 Rock Smash", "TM Case"], world.player) and
            has_badge_requirement(state, world, "Rock Smash")
            and can_use_hm(state, world, "Rock Smash"))


def can_waterfall(state: CollectionState, world: "PokemonFRLGWorld"):
    return (state.has_all(["HM07 Waterfall", "TM Case"], world.player) and
            has_badge_requirement(state, world, "Waterfall")
            and can_use_hm(state, world, "Waterfall"))


def has_n_badges(state: CollectionState, world: "PokemonFRLGWorld", n: int):
    badges = ["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge",
              "Soul Badge", "Marsh Badge", "Volcano Badge", "Earth Badge"]
    return sum([state.has(badge, world.player) for badge in badges]) >= n


def has_n_gyms(state: CollectionState, world: "PokemonFRLGWorld", n: int):
    gyms = ["Defeat Brock", "Defeat Misty", "Defeat Lt. Surge", "Defeat Erika",
            "Defeat Koga", "Defeat Sabrina", "Defeat Blaine", "Defeat Giovanni"]
    return sum([state.has(gym, world.player) for gym in gyms]) >= n


def has_n_pokemon(state: CollectionState, world: "PokemonFRLGWorld", evos_allowed: bool, n: int):
    count = 0
    for species in data.species.values():
        if (state.has(species.name, world.player)
                or state.has(f"Static {species.name}", world.player)
                or (state.has(f"Evolved {species.name}", world.player) and evos_allowed)):
            count += 1
        if count >= n:
            return True
    return False


def has_pokemon(state: CollectionState, world: "PokemonFRLGWorld", evos_allowed: bool, pokemon: str):
    if evos_allowed:
        return state.has_any([pokemon, f"Static {pokemon}", f"Evolved {pokemon}"], world.player)
    else:
        return state.has_any([pokemon, f"Static {pokemon}"], world.player)


def can_leave_viridian(state: CollectionState, world: "PokemonFRLGWorld"):
    if world.options.viridian_city_roadblock != ViridianCityRoadblock.option_open:
        return state.has("Deliver Oak's Parcel", world.player)
    return True


def can_challenge_giovanni(state: CollectionState, world: "PokemonFRLGWorld"):
    requirement = world.options.viridian_gym_requirement
    count = world.options.viridian_gym_count.value
    if requirement == ViridianGymRequirement.option_badges:
        return has_n_badges(state, world, count)
    elif requirement == ViridianGymRequirement.option_gyms:
        return has_n_gyms(state, world, count)


def can_enter_viridian_gym(state: CollectionState, world: "PokemonFRLGWorld"):
    return not world.options.gym_keys or state.has("Viridian Key", world.player)


def can_pass_route_22_gate(state: CollectionState, world: "PokemonFRLGWorld"):
    requirement = world.options.route22_gate_requirement
    count = world.options.route22_gate_count.value
    if requirement == Route22GateRequirement.option_badges:
        return has_n_badges(state, world, count)
    elif requirement == Route22GateRequirement.option_gyms:
        return has_n_gyms(state, world, count)


def can_enter_pewter_gym(state: CollectionState, world: "PokemonFRLGWorld"):
    return not world.options.gym_keys or state.has("Pewter Key", world.player)


def can_leave_pewter(state: CollectionState, world: "PokemonFRLGWorld"):
    requirement = world.options.pewter_city_roadblock
    if requirement == PewterCityRoadblock.option_brock:
        return state.has("Defeat Brock", world.player)
    elif requirement == PewterCityRoadblock.option_any_gym:
        return has_n_gyms(state, world, 1)
    elif requirement == PewterCityRoadblock.option_boulder_badge:
        return state.has("Boulder Badge", world.player)
    elif requirement == PewterCityRoadblock.option_any_badge:
        return has_n_badges(state, world, 1)
    return True


def can_enter_cerulean_gym(state: CollectionState, world: "PokemonFRLGWorld"):
    return not world.options.gym_keys or state.has("Cerulean Key", world.player)


def can_leave_cerulean(state: CollectionState, world: "PokemonFRLGWorld"):
    if "Remove Cerulean Roadblocks" in world.options.modify_world_state.value:
        return True
    return state.has("Help Bill", world.player)


def can_enter_route_9(state: CollectionState, world: "PokemonFRLGWorld"):
    if "Modify Route 9" in world.options.modify_world_state.value:
        return can_rock_smash(state, world)
    return can_cut(state, world)


def can_enter_cerulean_cave(state: CollectionState, world: "PokemonFRLGWorld"):
    requirement = world.options.cerulean_cave_requirement
    count = world.options.cerulean_cave_count.value
    if requirement == CeruleanCaveRequirement.option_vanilla:
        return state.has_all(["Defeat Champion", "Restore Pokemon Network Machine"], world.player)
    elif requirement == CeruleanCaveRequirement.option_champion:
        return state.has("Defeat Champion", world.player)
    elif requirement == CeruleanCaveRequirement.option_restore_network:
        return state.has("Restore Pokemon Network Machine", world.player)
    elif requirement == CeruleanCaveRequirement.option_badges:
        return has_n_badges(state, world, count)
    elif requirement == CeruleanCaveRequirement.option_gyms:
        return has_n_gyms(state, world, count)


def can_enter_vermilion_gym(state: CollectionState, world: "PokemonFRLGWorld"):
    return not world.options.gym_keys or state.has("Vermilion Key", world.player)


def can_enter_route_12(state: CollectionState, world: "PokemonFRLGWorld"):
    if "Route 12 Boulders" in world.options.modify_world_state.value:
        return can_strength(state, world)
    return True


def can_navigate_dark_caves(state: CollectionState, world: "PokemonFRLGWorld"):
    if world.options.flash_required != FlashRequired.option_off:
        return can_flash(state, world)
    return True


def route_10_waterfall_exists(world: "PokemonFRLGWorld"):
    return "Modify Route 10" in world.options.modify_world_state.value


def pokemon_tower_1f_ghost_exists(world: "PokemonFRLGWorld"):
    return "Block Tower" in world.options.modify_world_state.value


def can_enter_celadon_gym(state: CollectionState, world: "PokemonFRLGWorld"):
    return not world.options.gym_keys or state.has("Celadon Key", world.player)


def can_surf_past_snorlax(world: "PokemonFRLGWorld"):
    return "Modify Route 12" not in world.options.modify_world_state.value


def can_rock_smash_past_snorlax(state: CollectionState, world: "PokemonFRLGWorld"):
    if "Modify Route 16" in world.options.modify_world_state.value:
        return can_rock_smash(state, world)
    return False


def can_enter_fuchsia_gym(state: CollectionState, world: "PokemonFRLGWorld"):
    return not world.options.gym_keys or state.has("Fuchsia Key", world.player)


def can_enter_silph(state: CollectionState, world: "PokemonFRLGWorld"):
    if "Open Silph" in world.options.modify_world_state.value:
        return True
    return state.has("Rescue Mr. Fuji", world.player)


def can_open_silph_door(state: CollectionState, world: "PokemonFRLGWorld", floor: int):
    return (state.has_any(["Card Key", f"Card Key {floor}F"], world.player) or
            state.has("Progressive Card Key", world.player, floor - 1))


def saffron_rockets_gone(state: CollectionState, world: "PokemonFRLGWorld"):
    if "Remove Saffron Rockets" in world.options.modify_world_state.value:
        return True
    return state.has("Liberate Silph Co.", world.player)


def can_enter_saffron_gym(state: CollectionState, world: "PokemonFRLGWorld"):
    return not world.options.gym_keys or state.has("Saffron Key", world.player)


def can_stop_seafoam_b3f_current(state: CollectionState, world: "PokemonFRLGWorld"):
    return can_strength(state, world) and state.can_reach_region("Seafoam Islands 1F", world.player)


def can_stop_seafoam_b4f_current(state: CollectionState, world: "PokemonFRLGWorld"):
    return can_strength(state, world) and state.can_reach_region("Seafoam Islands B3F Southwest", world.player)


def can_enter_cinnabar_gym(state: CollectionState, world: "PokemonFRLGWorld"):
    return state.has("Secret Key", world.player) or state.has("Cinnabar Key", world.player)


def can_pass_route_23_guard(state: CollectionState, world: "PokemonFRLGWorld"):
    requirement = world.options.route23_guard_requirement
    count = world.options.route23_guard_count.value
    if requirement == Route23GuardRequirement.option_badges:
        return has_n_badges(state, world, count)
    elif requirement == Route23GuardRequirement.option_gyms:
        return has_n_gyms(state, world, count)


def can_remove_victory_road_barrier(state: CollectionState, world: "PokemonFRLGWorld"):
    if "Victory Road Rocks" in world.options.modify_world_state.value:
        return can_strength(state, world) and can_rock_smash(state, world)
    return can_strength(state, world)


def can_challenge_elite_four(state: CollectionState, world: "PokemonFRLGWorld"):
    requirement = world.options.elite_four_requirement
    count = world.options.elite_four_count.value
    if requirement == EliteFourRequirement.option_badges:
        return has_n_badges(state, world, count)
    elif requirement == EliteFourRequirement.option_gyms:
        return has_n_gyms(state, world, count)


def can_challenge_elite_four_rematch(state: CollectionState, world: "PokemonFRLGWorld"):
    requirement = world.options.elite_four_requirement
    count = world.options.elite_four_rematch_count.value
    if state.has_all(["Defeat Champion", "Restore Pokemon Network Machine"], world.player):
        if requirement == EliteFourRequirement.option_badges:
            return has_n_badges(state, world, count)
        elif requirement == EliteFourRequirement.option_gyms:
            return has_n_gyms(state, world, count)
    return False


def can_sail_vermilion(state: CollectionState, world: "PokemonFRLGWorld"):
    if "Block Vermilion Sailing" not in world.options.modify_world_state.value:
        return True
    return state.has("S.S. Ticket", world.player)


def can_sail_island(state: CollectionState, world: "PokemonFRLGWorld", island: int):
    if world.options.island_passes in [SeviiIslandPasses.option_vanilla, SeviiIslandPasses.option_progressive]:
        progressive_passes = [1, 1, 1, 2, 2, 2, 2]
    else:
        progressive_passes = [1, 2, 3, 4, 5, 6, 7]
    return (state.has_any(island_passes[island], world.player) or
            state.has("Progressive Pass", world.player, progressive_passes[island - 1]))


def two_island_shop_expansion(state: CollectionState, world: "PokemonFRLGWorld", level: int):
    if level == 1:
        return state.has("Rescue Lostelle", world.player)
    elif level == 2:
        return state.has_all(["Rescue Lostelle", "Defeat Champion"], world.player)
    elif level == 3:
        return state.has_all(["Rescue Lostelle", "Defeat Champion", "Restore Pokemon Network Machine"], world.player)
    return False


def post_game_gossipers(state: CollectionState, world: "PokemonFRLGWorld"):
    if "Early Gossipers" in world.options.modify_world_state.value:
        return True
    return state.has("Defeat Champion", world.player)


def can_evolve(state: CollectionState, world: "PokemonFRLGWorld", pokemon: str):
    evolution_data = data.evolutions[pokemon]
    pokemon = re.sub(r'\d+', '', pokemon)
    if ((state.has(pokemon, world.player) or state.has(f"Evolved {pokemon}", world.player))
            and evolution_data.method in world.allowed_evo_methods):
        if evolution_data.method in evo_methods_item:
            return state.has(world.item_id_to_name[evolution_data.param], world.player)
        elif evolution_data.method in evo_methods_held_item:
            return state.has_all([world.item_id_to_name[evolution_data.param],
                                  world.item_id_to_name[evolution_data.param2]],
                                 world.player)
        elif (evolution_data.method in evo_methods_level
              or evolution_data.method in evo_methods_tyrogue_level
              or evolution_data.method in evo_methods_wurmple_level):
            return has_n_gyms(state, world, evolution_data.param / 7)
        elif evolution_data.method in evo_methods_friendship:
            return True
    return False


def has_trade_pokemon(state: CollectionState, world: "PokemonFRLGWorld", location: str):
    return state.has(world.required_trade_pokemon[location], world.player)
