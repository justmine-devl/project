from entities.player import Player
from systems.world import World
from systems.inventory import Inventory
from systems.weather import Weather
from systems.crafting import CraftingSystem
from systems.combat import CombatSystem
from systems.time import TimeSystem
from systems.save_load import SaveSystem
import random

def main():
    print("=== Welcome to the Untitled Survival Project: Phase 2 Core ===")
    
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
    
    # Optional Load
    load_choice = input("Load previous save? (y/n): ").lower()
    if load_choice == 'y':
        save_sys.load(player, inventory, time_sys)

    while player.is_alive:
        # Current State
        print("\n" + "="*40)
        print(f" {time_sys} | {weather}")
        print(player)
        print(inventory)
        print("="*40)
        
        print("\nWhat would you like to do?")
        print("1. Gather Resources (4h)")
        print("2. Search for Water (2h)")
        print("3. Eat/Drink from Inventory (0h)")
        print("4. Craft Item (1h)")
        print("5. Rest (8h)")
        print("6. Save Game (0h)")
        print("7. Quit")
        
        choice = input("> ")
        
        if choice == "1":
            res = world.gather_resource(player)
            if res:
                inventory.add_item(res)
            time_sys.advance_time(4)
            
            # Random Encounter Chance
            if random.random() < 0.2:
                enemy = combat.spawn_enemy()
                combat.resolve_combat(player, enemy, inventory)

        elif choice == "2":
            res = world.search_for_water(player)
            if res:
                inventory.add_item(res)
            time_sys.advance_time(2)

        elif choice == "3":
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

        elif choice == "4":
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

        elif choice == "5":
            player.recover_stamina(60)
            time_sys.advance_time(8)
            print("[*] You slept and recovered most of your stamina.")

        elif choice == "6":
            save_sys.save(player, inventory, time_sys)

        elif choice == "7":
            print("Exiting game...")
            break
        else:
            print("[!] Invalid choice.")

        # End of Turn Updates
        weather.update() # Change weather occasionally
        player.update_stats(weather.temperature)
        player.recover_stamina(5)

    print("\nGAME OVER")
    print(f"Survivor {player.name} lasted until Day {time_sys.day}.")

if __name__ == "__main__":
    main()
EOF > /workspace/project/project/src/main.py
from entities.player import Player
from systems.world import World
from systems.inventory import Inventory
from systems.weather import Weather
from systems.crafting import CraftingSystem
from systems.combat import CombatSystem
from systems.time import TimeSystem
from systems.save_load import SaveSystem
import random

def main():
    print("=== Welcome to the Untitled Survival Project: Phase 2 Core ===")
    
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
    
    # Optional Load
    load_choice = input("Load previous save? (y/n): ").lower()
    if load_choice == 'y':
        save_sys.load(player, inventory, time_sys)

    while player.is_alive:
        # Current State
        print("\n" + "="*40)
        print(f" {time_sys} | {weather}")
        print(player)
        print(inventory)
        print("="*40)
        
        print("\nWhat would you like to do?")
        print("1. Gather Resources (4h)")
        print("2. Search for Water (2h)")
        print("3. Eat/Drink from Inventory (0h)")
        print("4. Craft Item (1h)")
        print("5. Rest (8h)")
        print("6. Save Game (0h)")
        print("7. Quit")
        
        choice = input("> ")
        
        if choice == "1":
            res = world.gather_resource(player)
            if res:
                inventory.add_item(res)
            time_sys.advance_time(4)
            
            # Random Encounter Chance
            if random.random() < 0.2:
                enemy = combat.spawn_enemy()
                combat.resolve_combat(player, enemy, inventory)

        elif choice == "2":
            res = world.search_for_water(player)
            if res:
                inventory.add_item(res)
            time_sys.advance_time(2)

        elif choice == "3":
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

        elif choice == "4":
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

        elif choice == "5":
            player.recover_stamina(60)
            time_sys.advance_time(8)
            print("[*] You slept and recovered most of your stamina.")

        elif choice == "6":
            save_sys.save(player, inventory, time_sys)

        elif choice == "7":
            print("Exiting game...")
            break
        else:
            print("[!] Invalid choice.")

        # End of Turn Updates
        weather.update() # Change weather occasionally
        player.update_stats(weather.temperature)
        player.recover_stamina(5)

    print("\nGAME OVER")
    print(f"Survivor {player.name} lasted until Day {time_sys.day}.")

if __name__ == "__main__":
    main()
