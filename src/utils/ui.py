from utils.logger import logger

class UI:
    @staticmethod
    def clear_screen():
        """Clears the terminal screen for a cleaner UI."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def header(title):
        logger.log(f"=== {title} ===", "info")

    @staticmethod
    def info(message):
        logger.log(message, "info")

    @staticmethod
    def warning(message):
        logger.log(message, "warning")

    @staticmethod
    def alert(message):
        logger.log(message, "alert")

    @staticmethod
    def hud(time_sys, weather, biome, player, inventory, base, skills, quests):
        # For TUI, we still print the HUD. For GUI, the GUI will handle this.
        hud_text = (
            f"\n{time_sys} | {weather}\n"
            f" Biome: {biome}\n"
            f" {player}\n"
            f" {inventory}\n"
            f" {base}"
        )
        print(hud_text)
