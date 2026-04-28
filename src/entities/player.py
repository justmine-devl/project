class Player:
    def __init__(self, name="Survivor"):
        self.name = name
        # Survival Stats
        self.health = 100
        self.hunger = 100
        self.thirst = 100
        self.stamina = 100
        self.is_alive = True

    def update_stats(self):
        """Simulate time passing: decrease hunger and thirst."""
        self.hunger -= 1
        self.thirst -= 2
        
        if self.hunger <= 0 or self.thirst <= 0:
            self.health -= 5
            print(f"[!] Warning: Starvation or Dehydration! Health is dropping!")
        
        if self.health <= 0:
            self.is_alive = False
            print(f"[-] {self.name} has died.")

    def eat(self, amount):
        self.hunger = min(100, self.hunger + amount)
        print(f"[*] You ate some food. Hunger increased by {amount}.")

    def drink(self, amount):
        self.thirst = min(100, self.thirst + amount)
        print(f"[*] You drank some water. Thirst increased by {amount}.")

    def use_stamina(self, amount):
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        else:
            print("[!] Not enough stamina!")
            return False

    def recover_stamina(self, amount):
        self.stamina = min(100, self.stamina + amount)

    def __str__(self):
        return (f"--- {self.name}'s Status ---\n"
                f"Health: {self.health} | Hunger: {self.hunger} | "
                f"Thirst: {self.thirst} | Stamina: {self.stamina}\n"
                f"Alive: {self.is_alive}")
