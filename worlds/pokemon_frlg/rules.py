"""
Logic rule definitions for Pokémon FireRed and LeafGreen
"""
from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule
from .data import data, LocationCategory
from .locations import PokemonFRLGLocation
from .logic import (can_challenge_elite_four, can_challenge_elite_four_rematch, can_challenge_giovanni, can_cut,
                    can_enter_celadon_gym, can_enter_cerulean_cave, can_enter_cerulean_gym, can_enter_cinnabar_gym,
                    can_enter_fuchsia_gym, can_enter_pewter_gym, can_enter_route_9, can_enter_route_12,
                    can_enter_saffron_gym, can_enter_silph, can_enter_vermilion_gym, can_enter_viridian_gym,
                    can_evolve, can_fly, can_leave_cerulean, can_leave_pewter, can_leave_viridian,
                    can_navigate_dark_caves, can_open_silph_door, can_pass_route_22_gate, can_pass_route_23_guard,
                    can_remove_victory_road_barrier, can_rock_smash, can_rock_smash_past_snorlax, can_sail_island,
                    can_sail_vermilion, can_stop_seafoam_b3f_current, can_stop_seafoam_b4f_current, can_strength,
                    can_surf, can_surf_past_snorlax, can_waterfall,  has_n_pokemon, has_pokemon, has_trade_pokemon,
                    pokemon_tower_1f_ghost_exists, post_game_gossipers, route_10_waterfall_exists, saffron_rockets_gone,
                    two_island_shop_expansion)
from .options import Goal, ItemfinderRequired

if TYPE_CHECKING:
    from . import PokemonFRLGWorld


def set_evolution_rules(world: "PokemonFRLGWorld"):
    for location in world.get_locations():
        assert isinstance(location, PokemonFRLGLocation)
        if location.category == LocationCategory.EVENT_EVOLUTION_POKEMON:
            pokemon_name = location.name.split(" - ")[1].strip()
            add_rule(location, lambda state, pokemon=pokemon_name: can_evolve(state, world, pokemon))


def set_rules(world: "PokemonFRLGWorld"):
    player = world.player
    options = world.options
    evos_oaks_aides = "Oak's Aides" in options.evolutions_required.value
    evos_dexsanity = "Dexsanity" in world.options.evolutions_required.value

    if options.goal == Goal.option_champion:
        world.multiworld.completion_condition[player] = lambda state: state.has("Defeat Champion", player)
    elif options.goal == Goal.option_champion_rematch:
        world.multiworld.completion_condition[player] = lambda state: state.has("Defeat Champion (Rematch)", player)

    entrance_rules = {
        # Sky
        "Flying": lambda state: can_fly(state, world),
        "Pallet Town Fly Destination": lambda state: state.has("Fly Unlock (Pallet Town)", player),
        "Viridian City Fly Destination": lambda state: state.has("Fly Unlock (Viridian City)", player),
        "Pewter City Fly Destination": lambda state: state.has("Fly Unlock (Pewter City)", player),
        "Route 4 Fly Destination": lambda state: state.has("Fly Unlock (Route 4)", player),
        "Cerulean City Fly Destination": lambda state: state.has("Fly Unlock (Cerulean City)", player),
        "Vermilion City Fly Destination": lambda state: state.has("Fly Unlock (Vermilion City)", player),
        "Route 10 Fly Destination": lambda state: state.has("Fly Unlock (Route 10)", player),
        "Lavender Town Fly Destination": lambda state: state.has("Fly Unlock (Lavender Town)", player),
        "Celadon City Fly Destination": lambda state: state.has("Fly Unlock (Celadon City)", player),
        "Fuchsia City Fly Destination": lambda state: state.has("Fly Unlock (Fuchsia City)", player),
        "Saffron City Fly Destination": lambda state: state.has("Fly Unlock (Saffron City)", player),
        "Cinnabar Island Fly Destination": lambda state: state.has("Fly Unlock (Cinnabar Island)", player),
        "Indigo Plateau Fly Destination": lambda state: state.has("Fly Unlock (Indigo Plateau)", player),
        "One Island Fly Destination": lambda state: state.has("Fly Unlock (One Island)", player),
        "Two Island Fly Destination": lambda state: state.has("Fly Unlock (Two Island)", player),
        "Three Island Fly Destination": lambda state: state.has("Fly Unlock (Three Island)", player),
        "Four Island Fly Destination": lambda state: state.has("Fly Unlock (Four Island)", player),
        "Five Island Fly Destination": lambda state: state.has("Fly Unlock (Five Island)", player),
        "Six Island Fly Destination": lambda state: state.has("Fly Unlock (Six Island)", player),
        "Seven Island Fly Destination": lambda state: state.has("Fly Unlock (Seven Island)", player),

        # Seagallop
        "Vermilion City Arrival": lambda state: can_sail_vermilion(state, world),
        "One Island Arrival": lambda state: can_sail_island(state, world, 1),
        "Two Island Arrival": lambda state: can_sail_island(state, world, 2),
        "Three Island Arrival": lambda state: can_sail_island(state, world, 3),
        "Four Island Arrival": lambda state: can_sail_island(state, world, 4),
        "Five Island Arrival": lambda state: can_sail_island(state, world, 5),
        "Six Island Arrival": lambda state: can_sail_island(state, world, 6),
        "Seven Island Arrival": lambda state: can_sail_island(state, world, 7),
        "Navel Rock Arrival": lambda state: state.has("Mystic Ticket", player) and
                                            state.can_reach_region("Vermilion City", player),
        "Birth Island Arrival": lambda state: state.has("Aurora Ticket", player) and
                                              state.can_reach_region("Vermilion City", player),

        # Pallet Town
        "Pallet Town Surfing Spot": lambda state: can_surf(state, world),

        # Viridian City
        "Viridian City South Roadblock": lambda state: can_leave_viridian(state, world) or
                                                       can_cut(state, world),
        "Viridian City South Surfing Spot": lambda state: can_surf(state, world),
        "Viridian Gym": lambda state: can_challenge_giovanni(state, world) and
                                      can_enter_viridian_gym(state, world),

        # Route 22
        "Route 22 Surfing Spot": lambda state: can_surf(state, world),
        "Route 22 Gate Exit (North)": lambda state: can_pass_route_22_gate(state, world),

        # Route 2
        "Route 2 Southwest Cuttable Trees": lambda state: can_cut(state, world),
        "Route 2 East Cuttable Tree": lambda state: can_cut(state, world),
        "Route 2 Northwest Cuttable Tree": lambda state: can_cut(state, world),
        "Route 2 Northeast Cuttable Tree (North)": lambda state: can_cut(state, world),
        "Route 2 Northeast Cuttable Tree (South)": lambda state: can_cut(state, world),
        "Route 2 Northwest Smashable Rock": lambda state: can_rock_smash(state, world),
        "Route 2 Northeast Smashable Rock": lambda state: can_rock_smash(state, world),
        "Route 2 Northeast Cuttable Tree": lambda state: can_cut(state, world),

        # Pewter City
        "Pewter City Cuttable Tree": lambda state: can_cut(state, world),
        "Pewter City Exit (East)": lambda state: can_leave_pewter(state, world),
        "Pewter Gym": lambda state: can_enter_pewter_gym(state, world),

        # Cerulean City
        "Cerulean City Cuttable Tree": lambda state: can_leave_cerulean(state, world) and
                                                     can_cut(state, world),
        "Robbed House (Front)": lambda state: can_leave_cerulean(state, world),
        "Cerulean Gym": lambda state: can_enter_cerulean_gym(state, world),
        "Cerulean City Outskirts Exit (East)": lambda state: can_enter_route_9(state, world),
        "Cerulean City Near Cave Surfing Spot": lambda state: can_surf(state, world),
        "Cerulean Cave": lambda state: can_enter_cerulean_cave(state, world),

        # Route 24
        "Route 24 Surfing Spot": lambda state: can_surf(state, world),

        # Route 25
        "Route 25 Surfing Spot": lambda state: can_surf(state, world),

        # Route 5
        "Route 5 Gate North Guard Checkpoint": lambda state: state.has_any(["Tea", "Blue Tea"], player),
        "Route 5 Gate South Guard Checkpoint": lambda state: state.has_any(["Tea", "Blue Tea"], player),
        "Route 5 Smashable Rocks": lambda state: can_rock_smash(state, world),
        "Route 5 Near Tunnel Smashable Rocks": lambda state: can_rock_smash(state, world),

        # Route 6
        "Route 6 Surfing Spot": lambda state: can_surf(state, world),
        "Route 6 Gate South Guard Checkpoint": lambda state: state.has_any(["Tea", "Red Tea"], player),
        "Route 6 Gate North Guard Checkpoint": lambda state: state.has_any(["Tea", "Red Tea"], player),
        "Route 6 Smashable Rocks": lambda state: can_rock_smash(state, world),
        "Route 6 Near Tunnel Smashable Rocks": lambda state: can_rock_smash(state, world),

        # Vermilion City
        "Vermilion City Cuttable Tree": lambda state: can_cut(state, world),
        "Vermilion City Surfing Spot": lambda state: can_surf(state, world),
        "Vermilion City Checkpoint": lambda state: state.has("S.S. Ticket", player),
        "Vermilion City Near Gym Cuttable Tree": lambda state: can_cut(state, world),
        "Vermilion City Near Gym Surfing Spot": lambda state: can_surf(state, world),
        "Vermilion Gym": lambda state: can_enter_vermilion_gym(state, world),

        # S.S. Anne
        "S.S. Anne Exterior Surfing Spot": lambda state: can_surf(state, world),

        # Route 11
        "Route 11 West Surfing Spot": lambda state: can_surf(state, world),
        "Route 11 East Exit": lambda state: can_enter_route_12(state, world),

        # Route 9
        "Route 9 Exit (West)": lambda state: can_enter_route_9(state, world),

        # Route 10
        "Route 10 North Surfing Spot": lambda state: can_surf(state, world),
        "Route 10 Near Power Plant Surfing Spot": lambda state: can_surf(state, world),
        "Power Plant (Front)": lambda state: state.has("Machine Part", player) or
                                             not options.extra_key_items,
        "Route 10 Waterfall Drop": lambda state: can_waterfall(state, world),
        "Route 10 Waterfall Ascend": lambda state: can_waterfall(state, world),
        "Route 10 South Surfing Spot": lambda state: route_10_waterfall_exists(world) and
                                                     can_surf(state, world),
        "Route 10 South Landing": lambda state: route_10_waterfall_exists(world),
        "Route 10 South (Fishing Battle)": lambda state: route_10_waterfall_exists(world),

        # Lavender Town
        "Lavender Town Exit (South)": lambda state: can_enter_route_12(state, world),

        # Route 8
        "Route 8 Cuttable Trees": lambda state: can_cut(state, world),
        "Route 8 Gate East Guard Checkpoint": lambda state: state.has_any(["Tea", "Purple Tea"], player),
        "Route 8 Gate West Guard Checkpoint": lambda state: state.has_any(["Tea", "Purple Tea"], player),
        "Route 8 Smashable Rocks": lambda state: can_rock_smash(state, world),
        "Route 8 Near Tunnel Smashable Rocks": lambda state: can_rock_smash(state, world),

        # Route 7
        "Route 7 Gate West Guard Checkpoint": lambda state: state.has_any(["Tea", "Green Tea"], player),
        "Route 7 Gate East Guard Checkpoint": lambda state: state.has_any(["Tea", "Green Tea"], player),
        "Route 7 Smashable Rocks": lambda state: can_rock_smash(state, world),
        "Route 7 Near Tunnel Smashable Rocks": lambda state: can_rock_smash(state, world),

        # Celadon City
        "Celadon City Cuttable Tree": lambda state: can_cut(state, world),
        "Celadon City Surfing Spot": lambda state: can_surf(state, world),
        "Celadon City Near Gym Cuttable Tree": lambda state: can_cut(state, world),
        "Celadon Gym": lambda state: can_enter_celadon_gym(state, world),
        "Rocket Hideout": lambda state: state.has("Hideout Key", player) or
                                        not options.extra_key_items,
        "Celadon Gym Cuttable Trees": lambda state: can_cut(state, world),

        # Rocket Hideout
        "Rocket Hideout Elevator B1F Stop": lambda state: state.has("Lift Key", player),
        "Rocket Hideout Elevator B2F Stop": lambda state: state.has("Lift Key", player),
        "Rocket Hideout Elevator B4F Stop": lambda state: state.has("Lift Key", player),

        # Pokemon Tower
        "Pokemon Tower 1F Reveal Ghost": lambda state: pokemon_tower_1f_ghost_exists(world) and
                                                       state.has("Silph Scope", player),
        "Pokemon Tower 6F Reveal Ghost": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 1F (Ghost Battle)": lambda state: pokemon_tower_1f_ghost_exists(world) and
                                                         state.has("Silph Scope", player),
        "Pokemon Tower 6F (Ghost Battle)": lambda state: state.has("Silph Scope", player),

        # Route 12
        "Route 12 West Exit": lambda state: can_enter_route_12(state, world),
        "Route 12 North Exit": lambda state: can_enter_route_12(state, world),
        "Route 12 South Exit": lambda state: can_enter_route_12(state, world),
        "Route 12 West Play Poke Flute": lambda state: state.has("Poke Flute", player),
        "Route 12 North Surfing Spot": lambda state: can_surf(state, world),
        "Route 12 Center Surfing Spot": lambda state: can_surf(state, world),
        "Route 12 Center Play Poke Flute": lambda state: state.has("Poke Flute", player),
        "Route 12 Center Water Unobstructed Path": lambda state: can_surf_past_snorlax(world),
        "Route 12 South Surfing Spot": lambda state: can_surf(state, world),
        "Route 12 South Cuttable Tree (North)": lambda state: can_cut(state, world),
        "Route 12 South Cuttable Tree (South)": lambda state: can_cut(state, world),
        "Route 12 South Play Poke Flute": lambda state: state.has("Poke Flute", player),
        "Route 12 South Water Unobstructed Path": lambda state: can_surf_past_snorlax(world),

        # Route 13
        "Route 13 Exit (East)": lambda state: can_enter_route_12(state, world),
        "Route 13 Surfing Spot": lambda state: can_surf(state, world),
        "Route 13 Cuttable Tree": lambda state: can_cut(state, world),

        # Route 14
        "Route 14 Cuttable Tree (North)": lambda state: can_cut(state, world),
        "Route 14 Cuttable Tree (South)": lambda state: can_cut(state, world),

        # Route 16
        "Route 16 Southeast Cuttable Tree": lambda state: can_cut(state, world),
        "Route 16 Southeast Play Poke Flute": lambda state: state.has("Poke Flute", player),
        "Route 16 Northeast Cuttable Tree": lambda state: can_cut(state, world),
        "Route 16 Northeast Smashable Rock": lambda state: can_rock_smash_past_snorlax(state, world),
        "Route 16 Center Play Poke Flute": lambda state: state.has("Poke Flute", player),
        "Route 16 Center Smashable Rock": lambda state: can_rock_smash_past_snorlax(state, world),
        "Route 16 Gate 1F Southeast Bike Checkpoint": lambda state: state.has("Bicycle", player),

        # Route 18
        "Route 18 Gate 1F East Bike Checkpoint": lambda state: state.has("Bicycle", player),

        # Fuchsia City
        "Fuchsia Gym": lambda state: can_enter_fuchsia_gym(state, world),
        "Fuchsia City Backyard Surfing Spot": lambda state: can_surf(state, world),
        "Safari Zone": lambda state: state.has("Safari Pass", player) or
                                     not options.extra_key_items,

        # Safari Zone
        "Safari Zone Center Area South Surfing Spot": lambda state: can_surf(state, world),
        "Safari Zone Center Area Northwest Surfing Spot": lambda state: can_surf(state, world),
        "Safari Zone Center Area Northeast Surfing Spot": lambda state: can_surf(state, world),
        "Safari Zone East Area Surfing Spot": lambda state: can_surf(state, world),
        "Safari Zone North Area Surfing Spot": lambda state: can_surf(state, world),
        "Safari Zone West Area North Surfing Spot": lambda state: can_surf(state, world),
        "Safari Zone West Area South Surfing Spot": lambda state: can_surf(state, world),

        # Saffron City
        "Silph Co.": lambda state: can_enter_silph(state, world) or
                                   saffron_rockets_gone(state, world),
        "Copycat's House": lambda state: saffron_rockets_gone(state, world),
        "Saffron Gym": lambda state: saffron_rockets_gone(state, world) and
                                     can_enter_saffron_gym(state, world),
        "Saffron Pidgey House": lambda state: saffron_rockets_gone(state, world),

        # Silph Co.
        "Silph Co. 2F Barrier (Northwest)": lambda state: can_open_silph_door(state, world, 2),
        "Silph Co. 2F Barrier (Southwest)": lambda state: can_open_silph_door(state, world, 2),
        "Silph Co. 2F Northwest Room Barrier": lambda state: can_open_silph_door(state, world, 2),
        "Silph Co. 2F Southwest Room Barrier": lambda state: can_open_silph_door(state, world, 2),
        "Silph Co. 3F Barrier": lambda state: can_open_silph_door(state, world, 3),
        "Silph Co. 3F Center Room Barrier (East)": lambda state: can_open_silph_door(state, world, 3),
        "Silph Co. 3F Center Room Barrier (West)": lambda state: can_open_silph_door(state, world, 3),
        "Silph Co. 3F West Room Barrier": lambda state: can_open_silph_door(state, world, 3),
        "Silph Co. 4F Barrier (West)": lambda state: can_open_silph_door(state, world, 4),
        "Silph Co. 4F Barrier (Center)": lambda state: can_open_silph_door(state, world, 4),
        "Silph Co. 4F North Room Barrier": lambda state: can_open_silph_door(state, world, 4),
        "Silph Co. 5F Barrier (Northwest)": lambda state: can_open_silph_door(state, world, 5),
        "Silph Co. 5F Barrier (Center)": lambda state: can_open_silph_door(state, world, 5),
        "Silph Co. 5F Barrier (Southwest)": lambda state: can_open_silph_door(state, world, 5),
        "Silph Co. 5F Southwest Room Barrier": lambda state: can_open_silph_door(state, world, 5),
        "Silph Co. 6F Barrier": lambda state: can_open_silph_door(state, world, 6),
        "Silph Co. 7F Barrier (Center)": lambda state: can_open_silph_door(state, world, 7),
        "Silph Co. 7F Barrier (East)": lambda state: can_open_silph_door(state, world, 7),
        "Silph Co. 7F East Room Barrier (North)": lambda state: can_open_silph_door(state, world, 7),
        "Silph Co. 7F East Room Barrier (South)": lambda state: can_open_silph_door(state, world, 7),
        "Silph Co. 7F Southeast Room Barrier": lambda state: can_open_silph_door(state, world, 7),
        "Silph Co. 8F Barrier": lambda state: can_open_silph_door(state, world, 8),
        "Silph Co. 8F West Room Barrier": lambda state: can_open_silph_door(state, world, 8),
        "Silph Co. 9F Barrier": lambda state: can_open_silph_door(state, world, 9),
        "Silph Co. 9F Northwest Room Barrier": lambda state: can_open_silph_door(state, world, 9),
        "Silph Co. 9F Southwest Room Barrier (East)": lambda state: can_open_silph_door(state, world, 9),
        "Silph Co. 9F Southwest Room Barrier (West)": lambda state: can_open_silph_door(state, world, 9),
        "Silph Co. 10F Barrier": lambda state: can_open_silph_door(state, world, 10),
        "Silph Co. 10F Southeast Room Barrier": lambda state: can_open_silph_door(state, world, 10),
        "Silph Co. 11F West Barrier": lambda state: can_open_silph_door(state, world, 11),

        # Route 19
        "Route 19 Surfing Spot": lambda state: can_surf(state, world),

        # Route 20
        "Route 20 Near North Cave Surfing Spot": lambda state: can_surf(state, world),
        "Route 20 Near South Cave Surfing Spot": lambda state: can_surf(state, world),

        # Seafoam Islands
        "Seafoam Islands B3F Southwest Surfing Spot": lambda state: can_surf(state, world) and
                                                                    can_stop_seafoam_b3f_current(state, world),
        "Seafoam Islands B3F Southwest Landing": lambda state: can_stop_seafoam_b3f_current(state, world),
        "Seafoam Islands B3F South Water (Water Battle)": lambda state: can_stop_seafoam_b3f_current(state, world),
        "Seafoam Islands B3F East Landing (South)": lambda state: can_stop_seafoam_b3f_current(state, world),
        "Seafoam Islands B3F East Surfing Spot (South)": lambda state: can_surf(state, world) and
                                                                       can_stop_seafoam_b3f_current(state, world),
        "Seafoam Islands B3F East Surfing Spot (North)": lambda state: can_surf(state, world),
        "Seafoam Islands B3F Waterfall Ascend (Northeast)": lambda state: can_waterfall(state, world),
        "Seafoam Islands B3F Waterfall Drop (Northeast)": lambda state: can_waterfall(state, world),
        "Seafoam Islands B3F Waterfall Drop (Northwest)": lambda state: can_waterfall(state, world),
        "Seafoam Islands B3F Waterfall Ascend (Northwest)": lambda state: can_waterfall(state, world),
        "Seafoam Islands B3F Northwest Surfing Spot": lambda state: can_surf(state, world),
        "Seafoam Islands B4F Surfing Spot (West)": lambda state: can_surf(state, world) and
                                                                 can_stop_seafoam_b4f_current(state, world),
        "Seafoam Islands B4F Near Articuno Landing": lambda state: can_stop_seafoam_b4f_current(state, world),

        # Cinnabar Island
        "Cinnabar Island Surfing Spot": lambda state: can_surf(state, world),
        "Cinnabar Gym": lambda state: can_enter_cinnabar_gym(state, world),
        "Pokemon Mansion": lambda state: state.has("Letter", player) or
                                         not options.extra_key_items,
        "Follow Bill": lambda state: state.has("Defeat Blaine", player),
        "Pokemon Mansion 1F Southeast Exit": lambda state: not world.randomizing_entrances,

        # Route 23
        "Route 23 South Surfing Spot": lambda state: can_surf(state, world),
        "Route 23 Near Water Surfing Spot": lambda state: can_surf(state, world),
        "Route 23 Center Guard Checkpoint": lambda state: can_pass_route_23_guard(state, world),
        "Route 23 Near Water Cuttable Trees": lambda state: can_cut(state, world),
        "Route 23 Center Cuttable Trees": lambda state: can_cut(state, world),
        "Route 23 Waterfall Ascend": lambda state: can_waterfall(state, world),
        "Route 23 Waterfall Drop": lambda state: can_waterfall(state, world),

        # Victory Road
        "Victory Road 1F South Rock Barrier": lambda state: can_remove_victory_road_barrier(state, world),
        "Victory Road 1F North Strength Boulder": lambda state: can_strength(state, world),
        "Victory Road 2F Southwest Rock Barrier": lambda state: can_remove_victory_road_barrier(state, world),
        "Victory Road 2F Center Rock Barrier":
            lambda state: can_strength(state, world) and
                          state.can_reach_region("Victory Road 3F Southwest", player),
        "Victory Road 2F Northwest Strength Boulder": lambda state: can_strength(state, world),
        "Victory Road 3F North Rock Barrier": lambda state: can_remove_victory_road_barrier(state, world),
        "Victory Road 3F Southwest Strength Boulder": lambda state: can_strength(state, world),
        "Victory Road 3F Southeast Strength Boulder": lambda state: can_strength(state, world),

        # Indigo Plateau
        "Pokemon League": lambda state: can_challenge_elite_four(state, world),

        # One Island Town
        "One Island Town Surfing Spot": lambda state: can_surf(state, world),

        # Kindle Road
        "Kindle Road South Surfing Spot": lambda state: can_surf(state, world),
        "Kindle Road Center Surfing Spot (South)": lambda state: can_surf(state, world),
        "Kindle Road Center Surfing Spot (North)": lambda state: can_surf(state, world),
        "Kindle Road North Surfing Spot": lambda state: can_surf(state, world),

        # Mt. Ember
        "Mt. Ember Exterior South Strength Boulders": lambda state: can_strength(state, world),
        "Mt. Ember Ruby Path": lambda state: state.has("Deliver Meteorite", player),
        "Mt. Ember Ruby Path B2F West Strength Boulders": lambda state: can_strength(state, world),
        "Mt. Ember Ruby Path B2F East Strength Boulders": lambda state: can_strength(state, world),
        "Mt. Ember Ruby Path B3F Northwest Strength Boulder (Southwest)": lambda state: can_strength(state, world),
        "Mt. Ember Ruby Path B3F Northwest Strength Boulder (Southeast)": lambda state: can_strength(state, world),
        "Mt. Ember Ruby Path B3F Southwest Strength Boulder (Northwest)": lambda state: can_strength(state, world),
        "Mt. Ember Ruby Path B3F Southwest Strength Boulder (Southeast)": lambda state: can_strength(state, world),
        "Mt. Ember Ruby Path B3F Southeast Strength Boulder (Northwest)": lambda state: can_strength(state, world),
        "Mt. Ember Ruby Path B3F Southeast Strength Boulder (Southwest)": lambda state: can_strength(state, world),

        # Cape Brink
        "Cape Brink Surfing Spot": lambda state: can_surf(state, world),

        # Bond Bridge
        "Bond Bridge Surfing Spot": lambda state: can_surf(state, world),

        # Berry Forest
        "Berry Forest Surfing Spot": lambda state: can_surf(state, world),

        # Four Island Town
        "Four Island Town Surfing Spot": lambda state: can_surf(state, world),
        "Four Island Town Near Cave Surfing Spot": lambda state: can_surf(state, world),

        # Icefall Cave
        "Icefall Cave Front South Surfing Spot": lambda state: can_surf(state, world),
        "Icefall Cave Front Waterfall Ascend": lambda state: can_waterfall(state, world),
        "Icefall Cave Front Waterfall Drop": lambda state: can_waterfall(state, world),
        "Icefall Cave Front Center Surfing Spot": lambda state: can_surf(state, world),
        "Icefall Cave Front North Surfing Spot": lambda state: can_surf(state, world),
        "Icefall Cave Back Surfing Spot": lambda state: can_surf(state, world),

        # Five Island Town
        "Five Island Town Surfing Spot": lambda state: can_surf(state, world),

        # Five Isle Meadow
        "Five Isle Meadow Surfing Spot": lambda state: can_surf(state, world),
        "Rocket Warehouse": lambda state: state.has_all(["Learn Goldeen Need Log", "Learn Yes Nah Chansey"], player),

        # Resort Gorgeous
        "Resort Gorgeous Near Resort Surfing Spot": lambda state: can_surf(state, world),
        "Resort Gorgeous Near Cave Surfing Spot": lambda state: can_surf(state, world),

        # Water Path
        "Water Path South Surfing Spot": lambda state: can_surf(state, world),
        "Water Path North Surfing Spot (South)": lambda state: can_surf(state, world),
        "Water Path North Surfing Spot (North)": lambda state: can_surf(state, world),

        # Ruin Valley
        "Ruin Valley Surfing Spot": lambda state: can_surf(state, world),
        "Dotted Hole": lambda state: state.has("Help Lorelei", player) and
                                     can_cut(state, world),

        # Green Path
        "Green Path West Surfing Spot": lambda state: can_surf(state, world),

        # Outcast Island
        "Outcast Island Surfing Spot": lambda state: can_surf(state, world),

        # Tanoby Ruins
        "Tanoby Ruins Surfing Spot": lambda state: can_surf(state, world),
        "Tanoby Ruins Monean Island Surfing Spot": lambda state: can_surf(state, world),
        "Tanoby Ruins Liptoo Island Surfing Spot": lambda state: can_surf(state, world),
        "Tanoby Ruins Weepth Island Surfing Spot": lambda state: can_surf(state, world),
        "Tanoby Ruins Dilford Island Surfing Spot": lambda state: can_surf(state, world),
        "Tanoby Ruins Scufib Island Surfing Spot": lambda state: can_surf(state, world),
        "Tanoby Ruins Rixy Island Surfing Spot": lambda state: can_surf(state, world),
        "Tanoby Ruins Viapois Island Surfing Spot": lambda state: can_surf(state, world),

        # Monean Chamber
        "Monean Chamber (Land Battle)": lambda state: state.has("Unlock Ruins", player),

        # Liptoo Chamber
        "Liptoo Chamber (Land Battle)": lambda state: state.has("Unlock Ruins", player),

        # Weepth Chamber
        "Weepth Chamber (Land Battle)": lambda state: state.has("Unlock Ruins", player),

        # Dilford Chamber
        "Dilford Chamber (Land Battle)": lambda state: state.has("Unlock Ruins", player),

        # Scufib Chamber
        "Scufib Chamber (Land Battle)": lambda state: state.has("Unlock Ruins", player),

        # Rixy Chamber
        "Rixy Chamber (Land Battle)": lambda state: state.has("Unlock Ruins", player),

        # Viapois Chamber
        "Viapos Chamber (Land Battle)": lambda state: state.has("Unlock Ruins", player),

        # Trainer Tower
        "Trainer Tower Exterior South Surfing Spot": lambda state: can_surf(state, world),
        "Trainer Tower Exterior North Surfing Spot": lambda state: can_surf(state, world),

        # Cerulean Cave
        "Cerulean Cave 1F Southeast Surfing Spot": lambda state: can_surf(state, world),
        "Cerulean Cave 1F Northeast Surfing Spot": lambda state: can_surf(state, world),
        "Cerulean Cave 1F Surfing Spot": lambda state: can_surf(state, world),
        "Cerulean Cave B1F Surfing Spot": lambda state: can_surf(state, world),

        # Navel Rock
        "Navel Rock Seagallop": lambda state: can_sail_vermilion(state, world),

        # Birth Island
        "Birth Island Seagallop": lambda state: can_sail_vermilion(state, world),
    }

    location_rules = {
        # Pallet Town
        "Rival's House - Daisy Gift": lambda state: state.has("Deliver Oak's Parcel", player),
        "Professor Oak's Lab - Oak Gift (Deliver Parcel)": lambda state: state.has("Oak's Parcel", player),
        "Professor Oak's Lab - Oak Gift (Post Route 22 Rival)":
            lambda state: state.has("Defeat Route 22 Rival", player),
        "Professor Oak's Lab - Oak's Delivery": lambda state: state.has("Oak's Parcel", player),
        "Professor Oak's Lab - Oak's Aide M Info (Right)": lambda state: post_game_gossipers(state, world),
        "Professor Oak's Lab - Oak Info": lambda state: post_game_gossipers(state, world),
        "Professor Oak's Lab - Oak's Aide M Info (Left)": lambda state: post_game_gossipers(state, world),

        # Viridian City
        "Viridian City - Tutorial Man Gift": lambda state: can_leave_viridian(state, world),
        "Viridian Gym - Hidden Item Under Giovanni": lambda state: state.has("Itemfinder", player),
        "Viridian Gym - Gym Guy Info": lambda state: state.has("Defeat Giovanni", player),
        "Viridian City - Old Man Gift": lambda state: can_challenge_giovanni(state, world),

        # Route 22
        "Route 22 - Early Rival Battle": lambda state: state.has("Deliver Oak's Parcel", player),
        "Route 22 - Early Rival Reward": lambda state: state.has("Deliver Oak's Parcel", player),
        "Route 22 - Late Rival Reward":
            lambda state: state.has_all(["Defeat Route 22 Rival", "Defeat Giovanni"], player),
        "Route 22 Early Rival Scaling": lambda state: state.has("Deliver Oak's Parcel", player),
        "Route 22 Late Rival Scaling":
            lambda state: state.has_all(["Defeat Route 22 Rival", "Defeat Giovanni"], player),

        # Route 2
        "Route 2 Gate - Oak's Aide Gift (Pokedex Progress)":
            lambda state: has_n_pokemon(state, world, evos_oaks_aides, options.oaks_aide_route_2.value),
        "Route 2 Trade House - Trade Pokemon":
            lambda state: has_trade_pokemon(state, world, "Route 2 Trade House - Trade Pokemon"),

        # Pewter City
        "Pewter City - Gift from Mom": lambda state: state.has("Defeat Brock", player) and
                                                     state.can_reach_region("Route 3", player),

        # Cerulean City
        "Berry Powder Man's House - Berry Powder Man Gift": lambda state: state.has("Berry Pouch", player),
        "Bike Shop - Bicycle Purchase": lambda state: state.has("Bike Voucher", player),
        "Cerulean Trade House - Trade Pokemon":
            lambda state: has_trade_pokemon(state, world, "Cerulean Trade House - Trade Pokemon"),
        "Cerulean Gym - Hidden Item in Water": lambda state: can_surf(state, world) and
                                                             state.has("Itemfinder", player),
        "Cerulean Pokemon Center 1F - Bookshelf Info": lambda state: post_game_gossipers(state, world),

        # Route 25
        "Route 25 - Item Near Bush": lambda state: can_cut(state, world),

        # Underground Path North-South Tunnel
        "Underground Path North Entrance - Trade Pokemon":
            lambda state: has_trade_pokemon(state, world, "Underground Path North Entrance - Trade Pokemon"),

        # Vermilion City
        "Vermilion Trade House - Trade Pokemon":
            lambda state: has_trade_pokemon(state, world, "Vermilion Trade House - Trade Pokemon"),
        "Pokemon Fan Club - Worker Info": lambda state: post_game_gossipers(state, world),
        "Vermilion Pokemon Center 1F - Bookshelf Info": lambda state: state.has("Defeat Lt. Surge", player),

        # Route 11
        "Route 11 Gate 2F - Oak's Aide Gift (Pokedex Progress)":
            lambda state: has_n_pokemon(state, world, evos_oaks_aides, options.oaks_aide_route_11.value),
        "Route 11 Gate 2F - Trade Pokemon":
            lambda state: has_trade_pokemon(state, world, "Route 11 Gate 2F - Trade Pokemon"),

        # Route 10
        "Route 10 Pokemon Center 1F - Oak's Aide Gift (Pokedex Progress)":
            lambda state: has_n_pokemon(state, world, evos_oaks_aides, options.oaks_aide_route_10.value),
        "Route 10 - Hidden Item Behind Cuttable Tree": lambda state: can_cut(state, world),

        # Lavender Town
        "Volunteer Pokemon House - Mr. Fuji Gift": lambda state: state.has("Rescue Mr. Fuji", player),
        "Lavender Pokemon Center 1F - Balding Man Info": lambda state: post_game_gossipers(state, world),

        # Route 8
        "Route 8 - Twins Eli & Anne Reward": lambda state: state.has_any(world.repeatable_pokemon, player),

        # Celadon City
        "Celadon Game Corner - Fisherman Gift": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Scientist Gift": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Gentleman Gift": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner Prize Room - Prize Pokemon 1": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner Prize Room - Prize Pokemon 2": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner Prize Room - Prize Pokemon 3": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner Prize Room - Prize Pokemon 4": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner Prize Room - Prize Pokemon 5": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Northwest Hidden Item": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - North Hidden Item (Left)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - North Hidden Item (Right)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Northeast Hidden Item": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - West Hidden Item": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Center Hidden Item": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - East Hidden Item (Left)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - East Hidden Item (Right)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Southwest Hidden Item": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - South Hidden Item (Left)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - South Hidden Item (Right)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Southeast Hidden Item": lambda state: state.has("Coin Case", player),
        "Celadon Condominiums 1F - Tea Woman Info": lambda state: post_game_gossipers(state, world),
        "Celadon Condominiums 2F - Bookshelf Info": lambda state: state.has("Defeat Erika", player),
        "Celadon Department Store 2F - Woman Info": lambda state: post_game_gossipers(state, world),
        "Celadon Condominiums 1F - Brock Gift": lambda state: state.has("Defeat Brock", player),
        "Celadon Condominiums 1F - Misty Gift": lambda state: state.has("Defeat Misty", player),
        "Celadon Condominiums 1F - Erika Gift": lambda state: state.has("Defeat Erika", player),
        "Prize Pokemon 1 Scaling": lambda state: state.has("Coin Case", player),
        "Prize Pokemon 2 Scaling": lambda state: state.has("Coin Case", player),
        "Prize Pokemon 3 Scaling": lambda state: state.has("Coin Case", player),
        "Prize Pokemon 4 Scaling": lambda state: state.has("Coin Case", player),
        "Prize Pokemon 5 Scaling": lambda state: state.has("Coin Case", player),

        # Pokemon Tower
        "Pokemon Tower 6F - Ghost Pokemon": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 3F - Land Encounter 1": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 3F - Land Encounter 2": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 3F - Land Encounter 3": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 4F - Land Encounter 1": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 4F - Land Encounter 2": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 4F - Land Encounter 3": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 5F - Land Encounter 1": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 5F - Land Encounter 2": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 5F - Land Encounter 3": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 6F - Land Encounter 1": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 6F - Land Encounter 2": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 6F - Land Encounter 3": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 7F - Land Encounter 1": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 7F - Land Encounter 2": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 7F - Land Encounter 3": lambda state: state.has("Silph Scope", player),
        "Pokemon Tower 7F - Hidden Item Under Mr. Fuji": lambda state: state.has("Itemfinder", player),
        "Static Marowak Scaling": lambda state: state.has("Silph Scope", player),

        # Route 12
        "Route 12 - Hidden Item Under Snorlax": lambda state: state.has("Itemfinder", player),
        "Route 12 - Young Couple Gia & Jes Reward": lambda state: state.has_any(world.repeatable_pokemon, player),
        "Route 12 Fishing House - Fishing Guru Gift (Show Magikarp)": lambda state: state.has("Magikarp", player),

        # Route 14
        "Route 14 - Twins Kiri & Jan Reward": lambda state: state.has_any(world.repeatable_pokemon, player),

        # Route 15
        "Route 15 Gate 2F - Oak's Aide Gift (Pokedex Progress)":
            lambda state: has_n_pokemon(state, world, evos_oaks_aides, options.oaks_aide_route_15.value),
        "Route 15 - Crush Kin Ron & Mya Reward": lambda state: state.has_any(world.repeatable_pokemon, player),

        # Route 16
        "Route 16 Gate 2F - Oak's Aide Gift (Pokedex Progress)":
            lambda state: has_n_pokemon(state, world, evos_oaks_aides, options.oaks_aide_route_16.value),
        "Route 16 - Hidden Item Under Snorlax": lambda state: state.has("Itemfinder", player),
        "Route 16 - Young Couple Lea & Jed Reward": lambda state: state.has_any(world.repeatable_pokemon, player),

        # Route 18
        "Route 18 Gate 2F - Trade Pokemon":
            lambda state: has_trade_pokemon(state, world, "Route 18 Gate 2F - Trade Pokemon"),

        # Fuchsia City
        "Safari Zone Warden's House - Warden Gift (Return Teeth)": lambda state: state.has("Gold Teeth", player),
        "Safari Zone Warden's House - Item": lambda state: can_strength(state, world),
        "Fuchsia City - Koga's Daughter Info": lambda state: post_game_gossipers(state, world),
        "Safari Zone Warden's House - Bookshelf Info": lambda state: state.has("Defeat Koga", player),

        # Saffron City
        "Pokemon Trainer Fan Club - Bookshelf Info": lambda state: post_game_gossipers(state, world),
        "Saffron City - Battle Girl Info": lambda state: post_game_gossipers(state, world),
        "Saffron Pokemon Center 1F - Bookshelf Info": lambda state: state.has("Defeat Sabrina", player),

        # Route 19
        "Route 19 - Sis and Bro Lia & Luc Reward": lambda state: state.has_any(world.repeatable_pokemon, player),

        # Cinnabar Island
        "Pokemon Lab Lounge - Trade Pokemon 1":
            lambda state: has_trade_pokemon(state, world, "Pokemon Lab Lounge - Trade Pokemon 1"),
        "Pokemon Lab Lounge - Trade Pokemon 2":
            lambda state: has_trade_pokemon(state, world, "Pokemon Lab Lounge - Trade Pokemon 2"),
        "Pokemon Lab Experiment Room - Revive Helix Fossil": lambda state: state.has("Helix Fossil", player),
        "Pokemon Lab Experiment Room - Revive Dome Fossil": lambda state: state.has("Dome Fossil", player),
        "Pokemon Lab Experiment Room - Revive Old Amber": lambda state: state.has("Old Amber", player),
        "Pokemon Lab Experiment Room - Trade Pokemon":
            lambda state: has_trade_pokemon(state, world, "Pokemon Lab Experiment Room - Trade Pokemon"),
        "Cinnabar Pokemon Center 1F - Bookshelf Info": lambda state: post_game_gossipers(state, world),
        "Cinnabar Pokemon Center 1F - Bill Gift": lambda state: state.has("Defeat Blaine", player),
        "Gift Omanyte Scaling": lambda state: state.has("Helix Fossil", player),
        "Gift Kabuto Scaling": lambda state: state.has("Dome Fossil", player),
        "Gift Aerodactyl Scaling": lambda state: state.has("Old Amber", player),

        # Route 21
        "Route 21 - Sis and Bro Lil & Ian Reward": lambda state: state.has_any(world.repeatable_pokemon, player),

        # Victory Road
        "Victory Road 1F - North Item (Left)": lambda state: can_strength(state, world),
        "Victory Road 1F - North Item (Right)": lambda state: can_strength(state, world),
        "Victory Road 3F - Cool Couple Ray & Tyra Reward":
            lambda state: state.has_any(world.repeatable_pokemon, player),

        # Indigo Plateau
        "Champion's Room - Champion Rematch Battle": lambda state: can_challenge_elite_four_rematch(state, world),
        "Lorelei's Room - Elite Four Lorelei Rematch Reward":
            lambda state: can_challenge_elite_four_rematch(state, world),
        "Bruno's Room - Elite Four Bruno Rematch Reward": lambda state: can_challenge_elite_four_rematch(state, world),
        "Agatha's Room - Elite Four Agatha Rematch Reward":
            lambda state: can_challenge_elite_four_rematch(state, world),
        "Lance's Room - Elite Four Lance Rematch Reward": lambda state: can_challenge_elite_four_rematch(state, world),
        "Champion's Room - Champion Rematch Reward": lambda state: can_challenge_elite_four_rematch(state, world),
        "Indigo Plateau Pokemon Center 1F - Black Belt Info 1": lambda state: post_game_gossipers(state, world),
        "Indigo Plateau Pokemon Center 1F - Black Belt Info 2": lambda state: post_game_gossipers(state, world),
        "Indigo Plateau Pokemon Center 1F - Bookshelf Info": lambda state: post_game_gossipers(state, world),
        "Indigo Plateau Pokemon Center 1F - Cooltrainer Info": lambda state: post_game_gossipers(state, world),
        "Elite Four Rematch Scaling": lambda state: can_challenge_elite_four_rematch(state, world),
        "Champion Rematch Scaling": lambda state: can_challenge_elite_four_rematch(state, world),

        # One Island Town
        "One Island Pokemon Center 1F - Celio Gift (Deliver Ruby)":
            lambda state: state.has_all(["Deliver Meteorite", "Ruby"], player),
        "One Island Pokemon Center 1F - Help Celio":
            lambda state: state.has_all(["Deliver Meteorite", "Ruby", "Free Captured Pokemon", "Sapphire"], player),
        "One Island Pokemon Center 1F - Celio Info 1":
            lambda state: state.has("Restore Pokemon Network Machine", player),
        "One Island Pokemon Center 1F - Celio Info 2":
            lambda state: state.has("Restore Pokemon Network Machine", player),
        "One Island Pokemon Center 1F - Celio Info 3":
            lambda state: state.has("Restore Pokemon Network Machine", player),
        "One Island Pokemon Center 1F - Celio Gift (Deliver Sapphire)":
            lambda state: state.has_all(["Deliver Meteorite", "Ruby", "Free Captured Pokemon", "Sapphire"], player),
        
        # Kindle Road
        "Kindle Road - Plateau Item": lambda state: can_rock_smash(state, world),
        "Kindle Road - Item Behind Smashable Rock": lambda state: can_rock_smash(state, world),
        "Kindle Road - Crush Kin Mik & Kia Reward": lambda state: state.has_any(world.repeatable_pokemon, player),

        # Ember Spa
        "Ember Spa - Black Belt Info": lambda state: post_game_gossipers(state, world),

        # Mt. Ember
        "Mt. Ember Exterior - Item Near Summit": lambda state: can_strength(state, world) and
                                                               can_rock_smash(state, world),
        "Mt. Ember Exterior - Eavesdrop on Team Rocket Grunts": lambda state: state.has("Deliver Meteorite", player),
        "Mt. Ember Summit - Legendary Pokemon": lambda state: can_strength(state, world),
        "Mt. Ember Exterior - Team Rocket Grunt Reward (Left)": lambda state: state.has("Deliver Meteorite", player),
        "Mt. Ember Exterior - Team Rocket Grunt Reward (Right)": lambda state: state.has("Deliver Meteorite", player),
        "Team Rocket Grunt 43 Scaling": lambda state: state.has("Deliver Meteorite", player),
        "Team Rocket Grunt 44 Scaling": lambda state: state.has("Deliver Meteorite", player),
        "Legendary Moltres Scaling": lambda state: can_strength(state, world),

        # Two Island Town
        "Two Island Town - Item Behind Cuttable Tree": lambda state: can_cut(state, world),
        "Two Island Game Corner - Lostelle's Dad Gift (Deliver Meteorite)":
            lambda state: state.has_all(["Rescue Lostelle", "Meteorite"], player),
        "Two Island Game Corner - Lostelle's Dad's Delivery":
            lambda state: state.has_all(["Rescue Lostelle", "Meteorite"], player),
        "Two Island Town - Market Stall Item 2": lambda state: two_island_shop_expansion(state, world, 1),
        "Two Island Town - Market Stall Item 3": lambda state: two_island_shop_expansion(state, world, 3),
        "Two Island Town - Market Stall Item 4": lambda state: two_island_shop_expansion(state, world, 3),
        "Two Island Town - Market Stall Item 5": lambda state: two_island_shop_expansion(state, world, 2),
        "Two Island Town - Market Stall Item 6": lambda state: two_island_shop_expansion(state, world, 1),
        "Two Island Town - Market Stall Item 8": lambda state: two_island_shop_expansion(state, world, 2),
        "Two Island Town - Market Stall Item 9": lambda state: two_island_shop_expansion(state, world, 3),
        "Two Island Town - Beauty Info": lambda state: two_island_shop_expansion(state, world, 2),

        # Cape Brink
        "Cape Brink - Hidden Item Across Pond": lambda state: state.has("Itemfinder", player),

        # Three Island Town
        "Three Island Town - Item Behind East Fence": lambda state: can_cut(state, world),
        "Three Island Town - Hidden Item Behind West Fence": lambda state: can_cut(state, world),
        "Lostelle's House - Lostelle Gift": lambda state: state.has("Deliver Meteorite", player),

        # Bond Bridge
        "Bond Bridge - Twins Joy & Meg Reward": lambda state: state.has_any(world.repeatable_pokemon, player),

        # Berry Forest
        "Berry Forest - Item Past Southwest Pond": lambda state: can_cut(state, world),

        # Four Island Town
        "Four Island Town - Beach Item": lambda state: can_rock_smash(state, world),
        "Four Island Town - Old Woman Info": lambda state: state.has("Restore Pokemon Network Machine", player),

        # Five Island Town
        "Five Island Pokemon Center 1F - Bookshelf Info": lambda state: post_game_gossipers(state, world),

        # Five Isle Meadow
        "Five Isle Meadow - Item Behind Cuttable Tree": lambda state: can_cut(state, world),

        # Rocket Warehouse
        "Rocket Warehouse - Scientist Gideon Info": lambda state: state.has("Restore Pokemon Network Machine", player),

        # Memorial Pillar
        "Memorial Pillar - Memorial Man Gift": lambda state: state.has("Lemonade", player),

        # Water Labyrinth
        "Water Labyrinth - Gentleman Info": lambda state: state.has_any(["Togepi", "Togetic"], player),

        # Resort Gorgeous
        "Resort Gorgeous House - Selphy Gift (Show Pokemon)":
            lambda state: state.has_all(["Rescue Selphy", data.species[world.resort_gorgeous_mon].name], player),

        # Water Path
        "Water Path - Twins Miu & Mia Reward": lambda state: state.has_any(world.repeatable_pokemon, player),
        "Water Path Heracross Woman's House - Woman Gift (Show Heracross)":
            lambda state: state.has("Heracross", player),

        # Ruin Valley
        "Ruin Valley - Plateau Item": lambda state: can_strength(state, world),
        "Ruin Valley - Southwest Item": lambda state: can_strength(state, world),
        "Ruin Valley - Southeast Item": lambda state: can_strength(state, world),

        # Dotted Hole
        "Dotted Hole 1F - Dropped Item": lambda state: state.has("Learn Yes Nah Chansey", player),

        # Outcast Island
        "Outcast Island - Sis and Bro Ava & Geb Reward": lambda state: state.has_any(world.repeatable_pokemon, player),

        # Seven Island Town
        "Seven Island Town - Scientist Gift 1 (Trade Scanner)": lambda state: state.has("Scanner", player),
        "Seven Island Town - Scientist Gift 2 (Trade Scanner)": lambda state: state.has("Scanner", player),
        "Seven Island Pokemon Center 1F - Bookshelf Info": lambda state: post_game_gossipers(state, world),

        # Canyon Entrance
        "Canyon Entrance - Young Couple Eve & Jon Reward":
            lambda state: state.has_any(world.repeatable_pokemon, player),

        # Sevault Canyon
        "Sevault Canyon - Item Behind Smashable Rocks": lambda state: can_strength(state, world) and
                                                                      can_rock_smash(state, world),
        "Sevault Canyon - Cool Couple Lex & Nya Reward": lambda state: state.has_any(world.repeatable_pokemon, player),

        # Tanoby Key
        "Tanoby Key - Solve Puzzle": lambda state: can_strength(state, world),

        # Tanoby Ruins
        "Tanoby Ruins - Island Item": lambda state: state.has("Unlock Ruins", player),

        # Cerulean Cave
        "Cerulean Cave 2F - East Item": lambda state: can_rock_smash(state, world),
        "Cerulean Cave 2F - West Item": lambda state: can_rock_smash(state, world),
        "Cerulean Cave 2F - Center Item": lambda state: can_rock_smash(state, world),

        # Navel Rock
        "Navel Rock - Hidden Item Near Ho-Oh": lambda state: state.has("Itemfinder", player)
    }

    mt_moon_regions = ["Mt. Moon 1F", "Mt. Moon B1F First Tunnel", "Mt. Moon B1F Second Tunnel",
                       "Mt. Moon B1F Third Tunnel", "Mt. Moon B1F Fourth Tunnel", "Mt. Moon B2F South",
                       "Mt. Moon B2F Northeast", "Mt. Moon B2F", "Mt. Moon 1F Land Encounters",
                       "Mt. Moon B1F Land Encounters", "Mt. Moon B2F Land Encounters"]
    digletts_cave_regions = ["Diglett's Cave B1F", "Diglett's Cave B1F Land Encounters"]
    rock_tunnel_regions = ["Rock Tunnel 1F Northeast", "Rock Tunnel 1F Northwest", "Rock Tunnel 1F South",
                           "Rock Tunnel B1F Southeast", "Rock Tunnel B1F Northwest",
                           "Rock Tunnel 1F Land Encounters",
                           "Rock Tunnel B1F Land Encounters"]
    victory_road_regions = ["Victory Road 1F South", "Victory Road 1F North", "Victory Road 2F Southwest",
                            "Victory Road 2F Center", "Victory Road 2F Northwest", "Victory Road 2F Southeast",
                            "Victory Road 2F East", "Victory Road 3F North", "Victory Road 3F Southwest",
                            "Victory Road 3F Southeast", "Victory Road 1F Land Encounters",
                            "Victory Road 2F Land Encounters", "Victory Road 3F Land Encounters"]

    for entrance in world.get_entrances():
        if entrance.name in entrance_rules.keys():
            add_rule(entrance, entrance_rules[entrance.name])

    for location in world.get_locations():
        assert isinstance(location, PokemonFRLGLocation)
        if location.name in location_rules.keys():
            add_rule(location, location_rules[location.name])
        if (world.options.itemfinder_required != ItemfinderRequired.option_off and
                location.category in [LocationCategory.HIDDEN_ITEM, LocationCategory.HIDDEN_ITEM_RECURRING]):
            add_rule(location, lambda state: state.has("Itemfinder", player))
        if world.options.fame_checker_required and location.category == LocationCategory.FAMESANITY:
            add_rule(location, lambda state: state.has("Fame Checker", player))
        if location.category == LocationCategory.DEXSANITY:
            name = location.name.split(" - ")[1].strip()
            add_rule(location, lambda state, pokemon=name: has_pokemon(state, world, evos_dexsanity, pokemon))

    dark_cave_regions = list()
    dark_cave_regions.extend(rock_tunnel_regions)
    if "Mt. Moon" in options.additional_dark_caves.value:
        dark_cave_regions.extend(mt_moon_regions)
    if "Diglett's Cave" in options.additional_dark_caves.value:
        dark_cave_regions.extend(digletts_cave_regions)
    if "Victory Road" in options.additional_dark_caves.value:
        dark_cave_regions.extend(victory_road_regions)

    for region in dark_cave_regions:
        for entrance in world.get_region(region).entrances:
            add_rule(entrance, lambda state: can_navigate_dark_caves(state, world))
        for location in world.get_region(region).locations:
            add_rule(location, lambda state: can_navigate_dark_caves(state, world))
