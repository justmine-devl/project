import random

class Biome:
    def __init__(self, name, temp_mod, resource_modifiers, description):
        self.name = name
        self.temp_mod = temp_mod # Added to base temperature
        self.resource_modifiers = resource_modifiers # {resource_name: multiplier}
        self.description = description

    def __str__(self):
        return f"{self.name} ({self.description})"

class BiomeManager:
    def __init__(self):
        self.biomes = {
            "Forest": Biome("Forest", 0, {"Wood": 1.5, "Berry": 1.2, "Stone": 0.8}, "A lush green forest"),
            "Desert": Biome("Desert", 10, {"Stone": 1.2, "Water": 0.2, "Wood": 0.1}, "A scorching wasteland"),
            "Tundra": Biome("Tundra", -15, {"Stone": 1.0, "Wood": 0.3, "Water": 0.5}, "A frozen wasteland"),
            "Swamp": Biome("Swamp", 2, {"Wood": 0.8, "Berry": 0.5, "Stone": 0.5}, "A murky, damp marsh")
        }
        self.current_biome = self.biomes["Forest"]

    def move_to_random_biome(self):
        """Simulate traveling to a new area."""
        self.current_biome = random.choice(list(self.biomes.values()))
        print(f"[*] You have traveled to the {self.current_biome.name}!")
        print(f"    {self.current_biome.description}")

    def get_current_biome(self):
        return self.current_biome
