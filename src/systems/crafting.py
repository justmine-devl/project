class CraftingSystem:
    def __init__(self):
        # Recipes: {result: {ingredient: amount}}
        self.recipes = {
            "Basic Axe": {"ingredients": {"Wood": 3, "Stone": 2}, "level": 1, "skill": "Crafting"},
            "Stone Pickaxe": {"ingredients": {"Wood": 2, "Stone": 3}, "level": 1, "skill": "Crafting"},
            "Campfire": {"ingredients": {"Wood": 5, "Stone": 1}, "level": 1, "skill": "Crafting"},
            "Simple Shelter": {"ingredients": {"Wood": 10, "Cloth": 2}, "level": 1, "skill": "Crafting"},
            "Advanced Axe": {"ingredients": {"Metal": 5, "Wood": 3}, "level": 3, "skill": "Crafting"},
            "Reinforced Wall": {"ingredients": {"Metal": 10, "Stone": 10}, "level": 5, "skill": "Crafting"},
            "Medicine": {"ingredients": {"Berry": 5, "Cloth": 1}, "level": 2, "skill": "Crafting"}
        }

    def get_available_recipes(self, inventory, skill_system):
        """Returns a list of recipes the player can currently craft based on materials and skills."""
        available = []
        for item, data in self.recipes.items():
            ingredients = data["ingredients"]
            req_level = data["level"]
            req_skill = data["skill"]
            
            # Check skill level
            if skill_system.get_level(req_skill) < req_level:
                continue
                
            # Check materials
            can_craft = True
            for ing, amt in ingredients.items():
                if not inventory.has_item(ing, amt):
                    can_craft = False
                    break
            if can_craft:
                available.append(item)
        return available

    def craft(self, item_name, inventory, skill_system):
        """Attempts to craft an item by consuming ingredients and granting XP."""
        if item_name not in self.recipes:
            print("[!] Recipe not found.")
            return False
        
        data = self.recipes[item_name]
        ingredients = data["ingredients"]
        req_level = data["level"]
        req_skill = data["skill"]

        # Check skill level
        if skill_system.get_level(req_skill) < req_level:
            print(f"[!] Your {req_skill} level is too low!")
            return False

        # Double check availability
        for ing, amt in ingredients.items():
            if not inventory.has_item(ing, amt):
                print(f"[!] Missing materials for {item_name}!")
                return False
        
        # Consume materials
        for ing, amt in ingredients.items():
            inventory.remove_item(ing, amt)
            
        inventory.add_item(item_name)
        skill_system.gain_xp(req_skill, 20)
        print(f"[*] Successfully crafted: {item_name}!")
        return True
