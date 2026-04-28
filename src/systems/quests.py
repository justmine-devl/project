class Quest:
    def __init__(self, id, title, description, goal_item=None, goal_amount=0, reward_xp=50, reward_item=None):
        self.id = id
        self.title = title
        self.description = description
        self.goal_item = goal_item
        self.goal_amount = goal_amount
        self.reward_xp = reward_xp
        self.reward_item = reward_item
        self.is_completed = False

    def check_completion(self, inventory):
        if self.goal_item and inventory.has_item(self.goal_item, self.goal_amount):
            self.is_completed = True
            return True
        return False

class QuestSystem:
    def __init__(self):
        self.active_quests = []
        self.completed_quests = []
        self.available_quests = [
            Quest("q1", "The Basics", "Gather 5 Wood to start your camp.", "Wood", 5, 50, "Berry"),
            Quest("q2", "Stone Age", "Gather 5 Stone to make tools.", "Stone", 5, 50, "Berry"),
            Quest("q3", "First Tool", "Craft a Basic Axe.", "Basic Axe", 1, 100, "Water")
        ]

    def start_quest(self, quest_id):
        for q in self.available_quests:
            if q.id == quest_id:
                self.active_quests.append(q)
                self.available_quests.remove(q)
                print(f"[*] Quest Started: {q.title} - {q.description}")
                return True
        return False

    def update_quests(self, inventory, skill_system):
        """Checks if any active quests are completed."""
        for q in self.active_quests[:]:
            if q.check_completion(inventory):
                print(f"*** QUEST COMPLETED: {q.title}! ***")
                # Grant rewards
                skill_system.gain_xp("Survival", q.reward_xp)
                if q.reward_item:
                    inventory.add_item(q.reward_item)
                
                self.completed_quests.append(q)
                self.active_quests.remove(q)

    def __str__(self):
        if not self.active_quests:
            return "No active quests."
        lines = ["--- Active Quests ---"]
        for q in self.active_quests:
            status = "DONE" if q.is_completed else "In Progress"
            lines.append(f"- {q.title}: {q.description} ({status})")
        return "\n".join(lines)
