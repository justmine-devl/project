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

    def gather_resource(self, player, biome=None):
        """
        Attempts to gather a random resource based on rarity.
        Costs stamina.
        """
        if not player.use_stamina(15):
            return None

        # Base resources and their default weights
        base_resources = {
            "Wood": 0.8,
            "Stone": 0.5,
            "Berry": 0.6,
            "Water": 0.4
        }
        
        # Apply biome modifiers if present
        weights = []
        possible_resources = []
        for res, weight in base_resources.items():
            mod = biome.resource_modifiers.get(res, 1.0) if biome else 1.0
            weights.append(weight * mod)
            possible_resources.append(res)

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
