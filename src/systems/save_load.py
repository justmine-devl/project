import json
import os

class SaveSystem:
    def __init__(self, filename="savegame.json"):
        self.filename = filename

    def save(self, player, inventory, time_system, skills, quests, lore):
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
            },
            "skills": skills.skills,
            "quests": {
                "active": [q.id for q in quests.active_quests],
                "completed": [q.id for q in quests.completed_quests]
            },
            "lore": [f.fragment_id for f in lore.found_fragments]
        }
        
        try:
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=4)
            print(f"[*] Game saved successfully to {self.filename}.")
        except Exception as e:
            print(f"[!] Error saving game: {e}")

    def load(self, player, inventory, time_system, skills, quests, lore):
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
            
            # Restore skills
            skills.skills = data.get("skills", skills.skills)
            
            # Restore quests
            if "quests" in data:
                # Clear and rebuild from IDs
                quests.active_quests = []
                quests.completed_quests = []
                # This is a simplification; in a real game we'd map IDs back to Quest objects
                # For the prototype, we'll just mark them as started/completed if they exist in available
                for q_id in data["quests"].get("active", []):
                    quests.start_quest(q_id)
                for q_id in data["quests"].get("completed", []):
                    # Find quest by ID and add to completed
                    for q in quests.available_quests + quests.active_quests:
                        if q.id == q_id:
                            quests.completed_quests.append(q)
                            if q in quests.active_quests:
                                quests.active_quests.remove(q)
            
            # Restore lore
            if "lore" in data:
                for frag_id in data["lore"]:
                    lore.add_fragment(frag_id)
            
            print(f"[*] Game loaded successfully from {self.filename}.")
            return True
        except Exception as e:
            print(f"[!] Error loading game: {e}")
            return False
