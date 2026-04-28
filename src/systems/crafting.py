class CraftingSystem:
    def __init__(self):
        # Recipes: {result: {ingredient: amount}}
        self.recipes = {
            "Basic Axe": {"Wood": 3, "Stone": 2},
            "Stone Pickaxe": {"Wood": 2, "Stone": 3},
            "Campfire": {"Wood": 5, "Stone": 1},
            "Simple Shelter": {"Wood": 10, "Cloth": 2}
        }

    def get_available_recipes(self, inventory):
        """Returns a list of recipes the player can currently craft."""
        available = []
        for item, ingredients in self.recipes.items():
            can_craft = True
            for ing, amt in ingredients.items():
                if not inventory.has_item(ing, amt):
                    can_craft = False
                    break
            if can_craft:
                available.append(item)
        return available

    def craft(self, item_name, inventory):
        """Attempts to craft an item by consuming ingredients."""
        if item_name not in self.recipes:
            print("[!] Recipe not found.")
            return False
        
        ingredients = self.recipes[item_name]
        # Double check availability
        for ing, amt in ingredients.items():
            if not inventory.has_item(ing, amt):
                print(f"[!] Missing materials for {item_name}!")
                return False
        
        # Consume materials
        for ing, amt in ingredients.items():
            inventory.remove_item(ing, amt)
            
        inventory.add_item(item_name)
        print(f"[*] Successfully crafted: {item_name}!")
        return True
