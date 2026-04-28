import random

class LootTable:
    def __init__(self):
        # Format: {category: {item: weight}}
        self.tables = {
            "common_poi": {
                "Wood": 50,
                "Stone": 30,
                "Berry": 20,
                "Cloth": 10
            },
            "rare_poi": {
                "Metal": 40,
                "Cloth": 30,
                "Rare Metal": 10,
                "Water": 20
            },
            "enemy_drop": {
                "Cloth": 40,
                "Meat": 30,
                "Bone": 20,
                "Rare Metal": 10
            }
        }

    def roll(self, category, count=1):
        """Rolls for loot based on a category."""
        if category not in self.tables:
            return []
        
        table = self.tables[category]
        items = list(table.keys())
        weights = list(table.values())
        
        results = random.choices(items, weights=weights, k=count)
        return results

class PointOfInterest:
    def __init__(self, name, category, description):
        self.name = name
        self.category = category # "common_poi" or "rare_poi"
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"

class ExplorationSystem:
    def __init__(self, loot_table):
        self.loot_table = loot_table
        self.poi_types = [
            PointOfInterest("Abandoned Hut", "common_poi", "A small, decayed wooden hut."),
            PointOfInterest("Deep Cave", "rare_poi", "A dark, echoing cavern."),
            PointOfInterest("Ruined Outpost", "rare_poi", "Remnants of a former military post."),
            PointOfInterest("Berry Patch", "common_poi", "A dense cluster of wild berries.")
        ]

    def find_poi(self):
        """Randomly determines if a POI is found while exploring."""
        if random.random() < 0.3: # 30% chance to find a POI
            return random.choice(self.poi_types)
        return None

    def explore_poi(self, poi, inventory):
        """Allows player to explore a POI and get loot."""
        print(f"[*] You are exploring {poi.name}...")
        loot = self.loot_table.roll(poi.category, count=random.randint(1, 3))
        
        for item in loot:
            inventory.add_item(item)
        
        return loot
