import random

class Enemy:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

    def attack(self, player):
        damage = self.attack_power
        player.health -= damage
        print(f"[!] {self.name} attacked you for {damage} damage!")

class CombatSystem:
    def __init__(self):
        self.enemy_types = [
            {"name": "Wild Wolf", "health": 30, "attack": 10},
            {"name": "Feral Zombie", "health": 50, "attack": 5},
            {"name": "Giant Spider", "health": 40, "attack": 15}
        ]

    def spawn_enemy(self):
        data = random.choice(self.enemy_types)
        return Enemy(data["name"], data["health"], data["attack"])

    def resolve_combat(self, player, enemy, inventory):
        """
        Simple turn-based combat.
        """
        print(f"\n--- COMBAT: {player.name} vs {enemy.name} ---")
        
        while enemy.health > 0 and player.is_alive:
            print(f"\n{player.name}: {player.health} HP | {enemy.name}: {enemy.health} HP")
            print("1. Attack")
            print("2. Attempt to flee")
            
            choice = input("> ")
            if choice == "1":
                # Determine damage based on tools
                damage = 10
                if inventory.has_item("Basic Axe"):
                    damage = 20
                    print("[*] You attack with your Basic Axe!")
                else:
                    print("[*] You attack with your bare hands!")
                
                if enemy.take_damage(damage):
                    print(f"[*] You defeated the {enemy.name}!")
                    break
                
                # Enemy attacks back
                enemy.attack(player)
                if player.health <= 0:
                    player.is_alive = False
                    print(f"[-] You were slain by the {enemy.name}...")
            
            elif choice == "2":
                if random.random() < 0.4:
                    print("[*] You successfully fled!")
                    return "fled"
                else:
                    print("[!] You failed to flee!")
                    enemy.attack(player)
                    if player.health <= 0:
                        player.is_alive = False
            else:
                print("[!] Invalid choice.")
        
        return "won" if enemy.health <= 0 else "lost"
