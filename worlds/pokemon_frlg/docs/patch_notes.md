# 0.9.0
## Updates
+ The Berry Pouch and TM Case are now given to the player at the start of the game instead of when the first berry and HM/TM are obtained
+ If a gym door is locked, such as the Cinnabar or Viridian Gym, then you now need to interact with the door to unlock it
+ When you receive a fly unlock it will now tell you what location it allows you to fly to
+ Interacting with the Receptionist on the far right of the 2F of Pokémon Centers will allow you to purchase various consumable items that you have already obtained
+ The species that is requested for in-game trades are now randomized. Dex info will be given for the requested species after talking to the trade NPC
+ New option `skip_elite_four`
  + Makes it so that entering the Pokémon League takes the player directly to the Champion battle. Any location checks that would require fighting the Elite Four will not exist
+ New option `dungeon_entrance_shuffle`
  + Simple: Single entrance dungeons and multi entrance dungeons are shuffled separately from each other. Both entrances for multi entrance dungeons will connect to the same dungeon
  + Restricted: Single entrance dungeons and multi entrance dungeons are shuffled separately from each other. Both entrances for multi entrance dungeons do not need to lead to the same dungeon
  + Full: All dungeon entrances are shuffled together
+ New option `shopsanity`
  + Shuffles shop items into the item pool. The Celadon Department Store 4F Held Item Shop is not shuffled
+ New option `shop_prices`
  + Sets how shop prices are determined (by spheres, by item classification, by both, or completely random)
+ New options `minimum_shop_price` and `maximum_shop_price`
  + Sets the minimum and maximum prices that shop items can be when `shopsanity` is on
+ New options `shuffle_berry_pouch` and `shuffle_tm_case`
  + Shuffles the Berry Pouch and TM Case into the item pool. Creates a location check that is given at the start of the game for each one shuffled
+ New option `gym_keys`
  + Adds keys into the item pool that are needed to unlock each gym (renames the Secret Key to the Cinnabar Key)
+ New option `evolutions_required`
  + Sets which types of locations and/or access rules that evolutions may be logically required for
+ New option `evolution_methods_required`
  + Sets which types of evolutions may be logically required
+ New options `move_match_type_bias` and `move_normal_type_bias`
  + Sets the probability that a randomized move will match the Pokémon's type or will be a Normal move
+ New option `physical_special_split`
  + Changes the damage category that moves use to match the categories since the Gen IV physical/special split instead of the damage category being determined by the move's type
+ New option `move_types`
  + Randomizes the type for each move
+ New option `damage_categories`
  + Randomizes the damage category for each move/type. Will randomized the damage category of the moves individually or by each type depending on if the `physical_special_split` option is on
+ Changed the warps in the Lost Cave item rooms to return you to the previous room instead of back to the start

## Bug Fixes
+ Fixed a few typos in the game
+ Fixed an issue where setting the in-game Experience option to NONE still gave 1 exp
+ Fixed an issue where catching the Snorlax on Route 12 & 16 showed the text saying they returned to the mountains
+ Fixed an issue where a fly point randomized to take you in front of the Pewter Museum east entrance actually placed you to the left of the Pewter Pokémon Center