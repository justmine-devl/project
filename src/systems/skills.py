class SkillSystem:
    def __init__(self):
        # Skills: {name: {"level": 1, "xp": 0, "xp_next": 100}}
        self.skills = {
            "Gathering": {"level": 1, "xp": 0, "xp_next": 100},
            "Crafting": {"level": 1, "xp": 0, "xp_next": 100},
            "Combat": {"level": 1, "xp": 0, "xp_next": 100},
            "Survival": {"level": 1, "xp": 0, "xp_next": 100}
        }

    def gain_xp(self, skill_name, amount):
        """Adds XP to a skill and handles leveling up."""
        if skill_name not in self.skills:
            return
        
        skill = self.skills[skill_name]
        skill["xp"] += amount
        print(f"[*] Gained {amount} XP in {skill_name}!")
        
        if skill["xp"] >= skill["xp_next"]:
            skill["level"] += 1
            skill["xp"] -= skill["xp_next"]
            skill["xp_next"] = int(skill["xp_next"] * 1.5)
            print(f"*** LEVEL UP! {skill_name} is now level {skill['level']}! ***")

    def get_level(self, skill_name):
        return self.skills.get(skill_name, {}).get("level", 1)

    def __str__(self):
        lines = ["--- Player Skills ---"]
        for skill, data in self.skills.items():
            lines.append(f"{skill}: Lvl {data['level']} ({data['xp']}/{data['xp_next']} XP)")
        return "\n".join(lines)
