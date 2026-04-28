from entities.player import Player
from systems.world import World
from systems.inventory import Inventory

def main():
    print("=== Welcome to the Untitled Survival Project Prototype ===")
    player_name = input("Enter your survivor's name: ")
    player = Player(player_name)
    world = World()
    inventory = Inventory()
    
    turn = 1
    while player.is_alive:
        print(f"\n--- Day {turn} ---")
        print(player)
        print(inventory)
        print("\nWhat would you like to do?")
        print("1. Gather Resources (Costs Stamina)")
        print("2. Search for Water (Costs Stamina)")
        print("3. Eat Berries (from inventory)")
        print("4. Drink Water (from inventory)")
        print("5. Rest (Recover Stamina)")
        print("6. Quit")
        
        choice = input("> ")
        
        if choice == "1":
            res = world.gather_resource(player)
            if res:
                inventory.add_item(res)
        elif choice == "2":
            res = world.search_for_water(player)
            if res:
                inventory.add_item(res)
        elif choice == "3":
            if inventory.remove_item("Berry"):
                player.eat(20)
        elif choice == "4":
            if inventory.remove_item("Water"):
                player.drink(30)
        elif choice == "5":
            player.recover_stamina(40)
            print("[*] You rested and recovered some stamina.")
        elif choice == "6":
            print("Exiting game...")
            break
        else:
            print("[!] Invalid choice.")

        # End of turn updates
        player.update_stats()
        turn += 1
        # Slowly recover stamina over time
        player.recover_stamina(5)

    print("\nGAME OVER")
    print(f"Survivor {player.name} lasted {turn} turns.")

if __name__ == "__main__":
    main()
