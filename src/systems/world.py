import random

class Resource:
    def __init__(self, name, rarity=1.0):
        self.name = name
        self.rarity = rarity # Higher means more common

    def __repr__(self):
        return f"{self.name}"

class World:
    def __init__(self):
        self.resources = {
            "Wood": Resource("Wood", rarity=0.8),
            "Stone": Resource("Stone", rarity=0.5),
            "Berry": Resource("Berry", rarity=0.6),
            "Water": Resource("Water", rarity=0.4)
        }

    def gather_resource(self, player):
        """
        Attempts to gather a random resource based on rarity.
        Costs stamina.
        """
        if not player.use_stamina(15):
            return None

        # Simple weighted random choice
        possible_resources = list(self.resources.keys())
        weights = [r.rarity for r in self.resources.values()]
        
        gathered = random.choices(possible_resources, weights=weights, k=1)[0]
        print(f"[*] You spent some effort and found: {gathered}!")
        return gathered

    def search_for_water(self, player):
        """Specific action to find water."""
        if not player.use_stamina(10):
            return None
        
        if random.random() < 0.5:
            print("[*] You found a clean stream!")
            return "Water"
        else:
            print("[!] No water found here.")
            return None
