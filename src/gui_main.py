import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from entities.player import Player
from systems.world import World
from systems.inventory import Inventory
from systems.weather import Weather
from systems.crafting import CraftingSystem
from systems.combat import CombatSystem
from systems.time import TimeSystem
from systems.save_load import SaveSystem
from systems.biome import BiomeManager
from systems.exploration import ExplorationSystem, LootTable
from systems.base import Base
from systems.skills import SkillSystem
from systems.quests import QuestSystem
from systems.lore import LoreSystem
from utils.logger import logger

class SurvivalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Untitled Survival Project")
        self.root.geometry("1000x700")

        # Game State
        self.init_game()
        
        # Logger setup
        logger.add_listener(self.update_log)

        # UI Layout
        self.setup_ui()
        self.update_hud()

    def init_game(self):
        self.player = Player("Survivor")
        self.world = World()
        self.inventory = Inventory()
        self.weather = Weather()
        self.crafting = CraftingSystem()
        self.combat = CombatSystem()
        self.time_sys = TimeSystem()
        self.save_sys = SaveSystem()
        self.biome_sys = BiomeManager()
        self.loot_sys = LootTable()
        self.explor_sys = ExplorationSystem(self.loot_sys)
        self.base_sys = Base()
        self.skills = SkillSystem()
        self.quests = QuestSystem()
        self.lore = LoreSystem()

    def setup_ui(self):
        # Main Container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # TOP PANEL: HUD
        hud_frame = ttk.LabelFrame(main_frame, text="Survivor Status", padding="10")
        hud_frame.pack(fill=tk.X, pady=5)

        self.stat_label = ttk.Label(hud_frame, text="", font=("Courier", 10))
        self.stat_label.pack(side=tk.LEFT)

        self.env_label = ttk.Label(hud_frame, text="", font=("Courier", 10))
        self.env_label.pack(side=tk.RIGHT)

        # MIDDLE PANEL: Log and Actions
        mid_frame = ttk.Frame(main_frame)
        mid_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Action Buttons (Left)
        action_frame = ttk.LabelFrame(mid_frame, text="Actions", padding="10")
        action_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        actions = [
            ("Gather Resources", self.do_gather),
            ("Search Water", self.do_water),
            ("Explore Area", self.do_explore),
            ("Travel Region", self.do_travel),
            ("Eat/Drink", self.do_consume),
            ("Craft Item", self.do_craft),
            ("Manage Base", self.do_base),
            ("Rest", self.do_rest),
            ("Read Lore", self.do_lore),
            ("Start Quest", self.do_quest),
            ("Save Game", self.do_save),
        ]

        for text, cmd in actions:
            btn = ttk.Button(action_frame, text=text, command=cmd)
            btn.pack(fill=tk.X, pady=2)

        # Event Log (Right)
        log_frame = ttk.LabelFrame(mid_frame, text="Event Log", padding="10")
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        self.log_area = scrolledtext.ScrolledText(log_frame, state='disabled', height=20, font=("Courier", 10))
        self.log_area.pack(fill=tk.BOTH, expand=True)

        # BOTTOM PANEL: Inventory/Skills (Tabs)
        tab_control = ttk.Notebook(main_frame)
        tab_control.pack(fill=tk.X, pady=5)

        self.inv_tab = ttk.Frame(tab_control)
        self.skill_tab = ttk.Frame(tab_control)
        
        tab_control.add(self.inv_tab, text="Inventory")
        tab_control.add(self.skill_tab, text="Skills")

        self.inv_text = tk.Text(self.inv_tab, height=5, font=("Courier", 10), state='disabled')
        self.inv_text.pack(fill=tk.X)

        self.skill_text = tk.Text(self.skill_tab, height=5, font=("Courier", 10), state='disabled')
        self.skill_text.pack(fill=tk.X)

    def update_hud(self):
        # Player Stats
        stat_str = (f"HP: {self.player.health} | Hunger: {self.player.hunger} | "
                    f"Thirst: {self.player.thirst} | Stamina: {self.player.stamina} | "
                    f"Day: {self.time_sys.day} | Time: {self.time_sys.hour}:00")
        self.stat_label.config(text=stat_str)

        # Env Stats
        env_str = (f"Weather: {self.weather.weather_type} ({self.weather.temperature}°C) | "
                   f"Biome: {self.biome_sys.get_current_biome().name}")
        self.env_label.config(text=env_str)

        # Update Inventory Tab
        self.inv_text.config(state='normal')
        self.inv_text.delete('1.0', tk.END)
        self.inv_text.insert(tk.END, str(self.inventory))
        self.inv_text.config(state='disabled')

        # Update Skills Tab
        self.skill_text.config(state='normal')
        self.skill_text.delete('1.0', tk.END)
        self.skill_text.insert(tk.END, str(self.skills))
        self.skill_text.config(state='disabled')

    def update_log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        self.update_hud()

    # --- Game Action Wrappers ---
    def do_gather(self):
        res = self.world.gather_resource(self.player, self.biome_sys.get_current_biome())
        if res:
            self.inventory.add_item(res)
            self.skills.gain_xp("Gathering", 15)
        self.time_sys.advance_time(4)
        if random.random() < 0.2:
            enemy = self.combat.spawn_enemy()
            self.combat.resolve_combat_gui(self.player, enemy, self.inventory)
            self.skills.gain_xp("Combat", 30)
        self.end_turn()

    def do_water(self):
        res = self.world.search_for_water(self.player)
        if res:
            self.inventory.add_item(res)
            self.skills.gain_xp("Survival", 10)
        self.time_sys.advance_time(2)
        self.end_turn()

    def do_explore(self):
        self.time_sys.advance_time(6)
        poi = self.explor_sys.find_poi()
        if poi:
            logger.log(f"You found a Point of Interest: {poi}")
            # Simple GUI popup for exploration
            if messagebox.askyesno("Discovery", f"You found {poi.name}. Explore it?"):
                self.explor_sys.explore_poi(poi, self.inventory)
                if random.random() < 0.3:
                    frag_id = random.choice(["frag1", "frag2", "frag3"])
                    self.lore.add_fragment(frag_id)
        else:
            logger.log("You explored the area but found nothing special.")
        self.end_turn()

    def do_travel(self):
        self.biome_sys.move_to_random_biome()
        self.time_sys.advance_time(8)
        self.end_turn()

    def do_consume(self):
        # Simple popup for item selection
        item = "Berry" if random.random() < 0.5 else "Water" # Simplified for first pass
        if self.inventory.remove_item(item):
            if item == "Berry": self.player.eat(20)
            else: self.player.drink(30)
            logger.log(f"Consumed {item}!")
        else:
            logger.log(f"Not enough {item}!")
        self.update_hud()

    def do_craft(self):
        available = self.crafting.get_available_recipes(self.inventory, self.skills)
        if not available:
            logger.log("No craftable items available.")
            return
        
        # Simple selection popup
        recipe = random.choice(available) # Simplified for now
        if self.crafting.craft(recipe, self.inventory, self.skills):
            self.time_sys.advance_time(1)
        self.end_turn()

    def do_base(self):
        # Simplified base action
        if self.base_sys.build_shelter(self.inventory):
            logger.log("Built a shelter!")
        else:
            logger.log("Failed to build shelter (missing materials).")
        self.update_hud()

    def do_rest(self):
        self.player.recover_stamina(60)
        self.time_sys.advance_time(8)
        logger.log("You slept and recovered stamina.")
        self.end_turn()

    def do_lore(self):
        # Pop up the archives
        lore_text = "\n".join([str(f) for f in self.lore.found_fragments]) or "No fragments found."
        messagebox.showinfo("Archives", lore_text)

    def do_quest(self):
        if self.quests.available_quests:
            q = self.quests.available_quests[0]
            self.quests.start_quest(q.id)
            logger.log(f"Started Quest: {q.title}")
        else:
            logger.log("No available quests.")
        self.update_hud()

    def do_save(self):
        self.save_sys.save(self.player, self.inventory, self.time_sys, self.skills, self.quests, self.lore)
        logger.log("Game saved!")

    def end_turn(self):
        self.weather.update()
        final_temp = self.weather.temperature + self.biome_sys.get_current_biome().temp_mod
        self.player.update_stats(final_temp, self.base_sys.has_shelter)
        self.player.recover_stamina(5)
        self.quests.update_quests(self.inventory, self.skills)
        
        if not self.player.is_alive:
            messagebox.showerror("GAME OVER", f"Survivor {self.player.name} has died!")
            self.root.destroy()
        
        self.update_hud()

if __name__ == "__main__":
    import random
    root = tk.Tk()
    app = SurvivalGUI(root)
    root.mainloop()
