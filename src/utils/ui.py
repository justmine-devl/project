import os

class UI:
    @staticmethod
    def clear_screen():
        """Clears the terminal screen for a cleaner UI."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def header(title):
        print("\n" + "="*50)
        print(f" {title.center(48)} ")
        print("="*50)

    @staticmethod
    def info(message):
        print(f"[*] {message}")

    @staticmethod
    def warning(message):
        print(f"[!] {message}")

    @staticmethod
    def alert(message):
        print(f"*** {message} ***")

    @staticmethod
    def hud(time_sys, weather, biome, player, inventory, base, skills, quests):
        print("\n" + "-"*50)
        print(f" {time_sys} | {weather}")
        print(f" Biome: {biome}")
        print(f" {player}")
        print(f" {inventory}")
        print(f" {base}")
        print("-"*50)
