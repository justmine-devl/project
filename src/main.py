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
from systems.skills import SkillSystem
from systems.quests import QuestSystem
from systems.lore import LoreSystem
from utils.ui import UI
import random

def main():
    UI.clear_screen()
    UI.header("UNTITLED SURVIVAL PROJECT")
    print("Welcome to the final prototype build!")
    
    # Initialization
    player_name = input("\nEnter your survivor's name: ")
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
    skills = SkillSystem()
    quests = QuestSystem()
    lore = LoreSystem()
    
    # Optional Load
    load_choice = input("Load previous save? (y/n): ").lower()
    if load_choice == 'y':
        save_sys.load(player, inventory, time_sys, skills, quests, lore)

    while player.is_alive:
        UI.clear_screen()
        UI.header(f"Day {time_sys.day} - {player.name}")
        UI.hud(time_sys, weather, biome_sys.get_current_biome(), player, inventory, base_sys, skills, quests)
        
        print("\nWhat would you like to do?")
        print("1. Gather Resources (4h)")
        print("2. Search for Water (2h)")
        print("3. Explore Area (6h)")
        print("4. Travel to New Region (8h)")
        print("5. Eat/Drink (0h)")
        print("6. Craft Item (1h)")
        print("7. Manage Base (0h)")
        print("8. Rest (8h)")
        print("9. Read Lore (0h)")
        print("10. Start Quest (0h)")
        print("11. Save Game (0h)")
        print("12. Quit")
        
        choice = input("\n> ")
        
        if choice == "1":
            res = world.gather_resource(player, biome_sys.get_current_biome())
            if res:
                inventory.add_item(res)
                skills.gain_xp("Gathering", 15)
            time_sys.advance_time(4)
            if random.random() < 0.2:
                enemy = combat.spawn_enemy()
                combat.resolve_combat(player, enemy, inventory)
                skills.gain_xp("Combat", 30)

        elif choice == "2":
            res = world.search_for_water(player)
            if res:
                inventory.add_item(res)
                skills.gain_xp("Survival", 10)
            time_sys.advance_time(2)

        elif choice == "3":
            time_sys.advance_time(6)
            poi = explor_sys.find_poi()
            if poi:
                UI.info(f"You found a Point of Interest: {poi}")
                if input("Explore it? (y/n): ").lower() == 'y':
                    explor_sys.explore_poi(poi, inventory)
                    if random.random() < 0.3:
                        frag_id = random.choice(["frag1", "frag2", "frag3"])
                        lore.add_fragment(frag_id)
            else:
                UI.info("You explored the area but found nothing special.")

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
                UI.warning("Item not found or not consumable.")

        elif choice == "6":
            available = crafting.get_available_recipes(inventory, skills)
            if not available:
                UI.warning("You don't have materials or skill levels for any recipes.")
            else:
                print("Available Recipes:")
                for i, recipe in enumerate(available, 1):
                    print(f"{i}. {recipe}")
                
                rec_choice = input("Choose recipe number: ")
                try:
                    recipe_name = available[int(rec_choice)-1]
                    if crafting.craft(recipe_name, inventory, skills):
                        time_sys.advance_time(1)
                except (ValueError, IndexError):
                    UI.warning("Invalid selection.")

        elif choice == "7":
            print("\n--- Base Management ---")
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
            UI.info("You slept and recovered most of your stamina.")

        elif choice == "9":
            lore.read_lore()
            input("\nPress Enter to return...")

        elif choice == "10":
            print("\nAvailable Quests:")
            for i, q in enumerate(quests.available_quests, 1):
                print(f"{i}. {q.title}: {q.description}")
            q_choice = input("Choose quest number: ")
            try:
                q_id = quests.available_quests[int(q_choice)-1].id
                quests.start_quest(q_id)
            except (ValueError, IndexError):
                UI.warning("Invalid selection.")

        elif choice == "11":
            save_sys.save(player, inventory, time_sys, skills, quests, lore)

        elif choice == "12":
            print("Exiting game...")
            break
        else:
            UI.warning("Invalid choice.")

        # End of Turn Updates
        weather.update()
        final_temp = weather.temperature + biome_sys.get_current_biome().temp_mod
        player.update_stats(final_temp, base_sys.has_shelter)
        player.recover_stamina(5)
        quests.update_quests(inventory, skills)

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
from systems.biome import BiomeManager
from systems.exploration import ExplorationSystem, LootTable
from systems.base import Base
from systems.skills import SkillSystem
from systems.quests import QuestSystem
from systems.lore import LoreSystem
from utils.ui import UI
import random

def main():
    UI.clear_screen()
    UI.header("UNTITLED SURVIVAL PROJECT")
    print("Welcome to the final prototype build!")
    
    # Initialization
    player_name = input("\nEnter your survivor's name: ")
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
    skills = SkillSystem()
    quests = QuestSystem()
    lore = LoreSystem()
    
    # Optional Load
    load_choice = input("Load previous save? (y/n): ").lower()
    if load_choice == 'y':
        save_sys.load(player, inventory, time_sys, skills, quests, lore)

    while player.is_alive:
        UI.clear_screen()
        UI.header(f"Day {time_sys.day} - {player.name}")
        UI.hud(time_sys, weather, biome_sys.get_current_biome(), player, inventory, base_sys, skills, quests)
        
        print("\nWhat would you like to do?")
        print("1. Gather Resources (4h)")
        print("2. Search for Water (2h)")
        print("3. Explore Area (6h)")
        print("4. Travel to New Region (8h)")
        print("5. Eat/Drink (0h)")
        print("6. Craft Item (1h)")
        print("7. Manage Base (0h)")
        print("8. Rest (8h)")
        print("9. Read Lore (0h)")
        print("10. Start Quest (0h)")
        print("11. Save Game (0h)")
        print("12. Quit")
        
        choice = input("\n> ")
        
        if choice == "1":
            res = world.gather_resource(player, biome_sys.get_current_biome())
            if res:
                inventory.add_item(res)
                skills.gain_xp("Gathering", 15)
            time_sys.advance_time(4)
            if random.random() < 0.2:
                enemy = combat.spawn_enemy()
                combat.resolve_combat(player, enemy, inventory)
                skills.gain_xp("Combat", 30)

        elif choice == "2":
            res = world.search_for_water(player)
            if res:
                inventory.add_item(res)
                skills.gain_xp("Survival", 10)
            time_sys.advance_time(2)

        elif choice == "3":
            time_sys.advance_time(6)
            poi = explor_sys.find_poi()
            if poi:
                UI.info(f"You found a Point of Interest: {poi}")
                if input("Explore it? (y/n): ").lower() == 'y':
                    explor_sys.explore_poi(poi, inventory)
                    if random.random() < 0.3:
                        frag_id = random.choice(["frag1", "frag2", "frag3"])
                        lore.add_fragment(frag_id)
            else:
                UI.info("You explored the area but found nothing special.")

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
                UI.warning("Item not found or not consumable.")

        elif choice == "6":
            available = crafting.get_available_recipes(inventory, skills)
            if not available:
                UI.warning("You don't have materials or skill levels for any recipes.")
            else:
                print("Available Recipes:")
                for i, recipe in enumerate(available, 1):
                    print(f"{i}. {recipe}")
                
                rec_choice = input("Choose recipe number: ")
                try:
                    recipe_name = available[int(rec_choice)-1]
                    if crafting.craft(recipe_name, inventory, skills):
                        time_sys.advance_time(1)
                except (ValueError, IndexError):
                    UI.warning("Invalid selection.")

        elif choice == "7":
            print("\n--- Base Management ---")
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
            UI.info("You slept and recovered most of your stamina.")

        elif choice == "9":
            lore.read_lore()
            input("\nPress Enter to return...")

        elif choice == "10":
            print("\nAvailable Quests:")
            for i, q in enumerate(quests.available_quests, 1):
                print(f"{i}. {q.title}: {q.description}")
            q_choice = input("Choose quest number: ")
            try:
                q_id = quests.available_quests[int(q_choice)-1].id
                quests.start_quest(q_id)
            except (ValueError, IndexError):
                UI.warning("Invalid selection.")

        elif choice == "11":
            save_sys.save(player, inventory, time_sys, skills, quests, lore)

        elif choice == "12":
            print("Exiting game...")
            break
        else:
            UI.warning("Invalid choice.")

        # End of Turn Updates
        weather.update()
        final_temp = weather.temperature + biome_sys.get_current_biome().temp_mod
        player.update_stats(final_temp, base_sys.has_shelter)
        player.recover_stamina(5)
        quests.update_quests(inventory, skills)

    print("\nGAME OVER")
    print(f"Survivor {player.name} lasted until Day {time_sys.day}.")

if __name__ == "__main__":
    main()
