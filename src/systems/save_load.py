import json
import os

class SaveSystem:
    def __init__(self, filename="savegame.json"):
        self.filename = filename

    def save(self, player, inventory, time_system):
        """Saves the current game state to a JSON file."""
        data = {
            "player": {
                "name": player.name,
                "health": player.health,
                "hunger": player.hunger,
                "thirst": player.thirst,
                "stamina": player.stamina
            },
            "inventory": inventory.items,
            "time": {
                "day": time_system.day,
                "hour": time_system.hour
            }
        }
        
        try:
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=4)
            print(f"[*] Game saved successfully to {self.filename}.")
        except Exception as e:
            print(f"[!] Error saving game: {e}")

    def load(self, player, inventory, time_system):
        """Loads game state from a JSON file."""
        if not os.path.exists(self.filename):
            print("[!] No save file found.")
            return False
        
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
            
            # Restore player
            player.name = data["player"]["name"]
            player.health = data["player"]["health"]
            player.hunger = data["player"]["hunger"]
            player.thirst = data["player"]["thirst"]
            player.stamina = data["player"]["stamina"]
            
            # Restore inventory
            inventory.items = data["inventory"]
            
            # Restore time
            time_system.day = data["time"]["day"]
            time_system.hour = data["time"]["hour"]
            time_system.is_night = time_system.hour >= 20 or time_system.hour < 6
            
            print(f"[*] Game loaded successfully from {self.filename}.")
            return True
        except Exception as e:
            print(f"[!] Error loading game: {e}")
            return False
