class Base:
    def __init__(self):
        self.has_shelter = False
        self.fortification_level = 0
        self.storage = {}

    def build_shelter(self, inventory):
        """Builds a basic shelter if player has materials."""
        # Requirement: 10 Wood, 2 Cloth
        if inventory.remove_item("Wood", 10) and inventory.remove_item("Cloth", 2):
            self.has_shelter = True
            print("[*] You built a basic shelter! You are now protected from weather.")
            return True
        
        print("[!] Not enough materials to build a shelter (Requires 10 Wood, 2 Cloth).")
        return False

    def upgrade_fortification(self, inventory):
        """Upgrades base defenses."""
        # Requirement: 5 Stone, 5 Wood
        if inventory.remove_item("Stone", 5) and inventory.remove_item("Wood", 5):
            self.fortification_level += 1
            print(f"[*] Base fortified! Level: {self.fortification_level}")
            return True
        
        print("[!] Not enough materials to upgrade (Requires 5 Stone, 5 Wood).")
        return False

    def store_item(self, item_name, amount, inventory):
        if inventory.remove_item(item_name, amount):
            self.storage[item_name] = self.storage.get(item_name, 0) + amount
            print(f"[*] Stored {amount}x {item_name} in base storage.")
            return True
        return False

    def retrieve_item(self, item_name, amount, inventory):
        if self.storage.get(item_name, 0) >= amount:
            self.storage[item_name] -= amount
            if self.storage[item_name] == 0:
                del self.storage[item_name]
            inventory.add_item(item_name, amount)
            print(f"[*] Retrieved {amount}x {item_name} from storage.")
            return True
        
        print(f"[!] Not enough {item_name} in storage!")
        return False

    def __str__(self):
        shelter_status = "Protected" if self.has_shelter else "Exposed"
        return f"Base: [Shelter: {shelter_status} | Fortification: {self.fortification_level}]"
