class Inventory:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.items = {}

    def add_item(self, item_name, amount=1):
        if len(self.items) >= self.capacity and item_name not in self.items:
            print("[!] Inventory full! Cannot carry more unique items.")
            return False
        
        self.items[item_name] = self.items.get(item_name, 0) + amount
        print(f"[*] Added {amount}x {item_name} to inventory.")
        return True

    def remove_item(self, item_name, amount=1):
        if item_name in self.items and self.items[item_name] >= amount:
            self.items[item_name] -= amount
            if self.items[item_name] == 0:
                del self.items[item_name]
            return True
        
        print(f"[!] Not enough {item_name} in inventory!")
        return False

    def has_item(self, item_name, amount=1):
        return self.items.get(item_name, 0) >= amount

    def __str__(self):
        if not self.items:
            return "Inventory is empty."
        
        lines = [f"Inventory ({len(self.items)}/{self.capacity}):"]
        for item, qty in self.items.items():
            lines.append(f" - {item}: {qty}")
        return "\n".join(lines)
