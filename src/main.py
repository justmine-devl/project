from entities.player import Player
from systems.world import World
from systems.inventory import Inventory
from systems.weather import Weather
from systems.crafting import CraftingSystem
from systems.combat import CombatSystem
from systems.time import TimeSystem
from systems.save_load import SaveSystem
from systems.biome import BiomeManager
from systems.exploration import ExplorationSystem, LootTable
from systems.base import Base
import random

def main():
    print("=== Welcome to the Untitled Survival Project: Phase 3 World ===")
    
    # Initialization
    player_name = input("Enter your survivor's name: ")
    player = Player(player_name)
    world = World()
    inventory = Inventory()
    weather = Weather()
    crafting = CraftingSystem()
    combat = CombatSystem()
    time_sys = TimeSystem()
    save_sys = SaveSystem()
    biome_sys = BiomeManager()
    loot_sys = LootTable()
    explor_sys = ExplorationSystem(loot_sys)
    base_sys = Base()
    
    # Optional Load
    load_choice = input("Load previous save? (y/n): ").lower()
    if load_choice == 'y':
        save_sys.load(player, inventory, time_sys)

    while player.is_alive:
        # Current State
        print("\n" + "="*40)
        print(f" {time_sys} | {weather}")
        print(f"Current Biome: {biome_sys.get_current_biome()}")
        print(player)
        print(inventory)
        print(base_sys)
        print("="*40)
        
        print("\nWhat would you like to do?")
        print("1. Gather Resources (4h)")
        print("2. Search for Water (2h)")
        print("3. Explore Area (6h)")
        print("4. Travel to New Region (8h)")
        print("5. Eat/Drink from Inventory (0h)")
        print("6. Craft Item (1h)")
        print("7. Manage Base (0h)")
        print("8. Rest (8h)")
        print("9. Save Game (0h)")
        print("10. Quit")
        
        choice = input("> ")
        
        if choice == "1":
            res = world.gather_resource(player, biome_sys.get_current_biome())
            if res:
                inventory.add_item(res)
            time_sys.advance_time(4)
            if random.random() < 0.2:
                enemy = combat.spawn_enemy()
                combat.resolve_combat(player, enemy, inventory)

        elif choice == "2":
            res = world.search_for_water(player)
            if res:
                inventory.add_item(res)
            time_sys.advance_time(2)

        elif choice == "3":
            time_sys.advance_time(6)
            poi = explor_sys.find_poi()
            if poi:
                print(f"[*] You found a Point of Interest: {poi}")
                if input("Explore it? (y/n): ").lower() == 'y':
                    explor_sys.explore_poi(poi, inventory)
            else:
                print("[*] You explored the area but found nothing special.")

        elif choice == "4":
            biome_sys.move_to_random_biome()
            time_sys.advance_time(8)

        elif choice == "5":
            print("What to consume? (Berry/Water): ")
            item = input("> ")
            if item == "Berry":
                if inventory.remove_item("Berry"):
                    player.eat(20)
            elif item == "Water":
                if inventory.remove_item("Water"):
                    player.drink(30)
            else:
                print("[!] Item not found or not consumable.")

        elif choice == "6":
            available = crafting.get_available_recipes(inventory)
            if not available:
                print("[!] You don't have materials for any recipes.")
            else:
                print("Available Recipes:")
                for i, recipe in enumerate(available, 1):
                    print(f"{i}. {recipe}")
                
                rec_choice = input("Choose recipe number: ")
                try:
                    recipe_name = available[int(rec_choice)-1]
                    if crafting.craft(recipe_name, inventory):
                        time_sys.advance_time(1)
                except (ValueError, IndexError):
                    print("[!] Invalid selection.")

        elif choice == "7":
            print("Base Management:")
            print("1. Build/Repair Shelter")
            print("2. Upgrade Fortification")
            print("3. Store Item")
            print("4. Retrieve Item")
            print("5. Back")
            b_choice = input("> ")
            if b_choice == "1":
                base_sys.build_shelter(inventory)
            elif b_choice == "2":
                base_sys.upgrade_fortification(inventory)
            elif b_choice == "3":
                item = input("Item to store: ")
                amt = int(input("Amount: "))
                base_sys.store_item(item, amt, inventory)
            elif b_choice == "4":
                item = input("Item to retrieve: ")
                amt = int(input("Amount: "))
                base_sys.retrieve_item(item, amt, inventory)

        elif choice == "8":
            player.recover_stamina(60)
            time_sys.advance_time(8)
            print("[*] You slept and recovered most of your stamina.")

        elif choice == "9":
            save_sys.save(player, inventory, time_sys)

        elif choice == "10":
            print("Exiting game...")
            break
        else:
            print("[!] Invalid choice.")

        # End of Turn Updates
        weather.update()
        # Apply biome temperature modifier to base weather temperature
        final_temp = weather.temperature + biome_sys.get_current_biome().temp_mod
        player.update_stats(final_temp, base_sys.has_shelter)
        player.recover_stamina(5)

    print("\nGAME OVER")
    print(f"Survivor {player.name} lasted until Day {time_sys.day}.")

if __name__ == "__main__":
    main()
