class LoreItem:
    def __init__(self, name, content, fragment_id):
        self.name = name
        self.content = content
        self.fragment_id = fragment_id

    def __str__(self):
        return f"Lore Fragment [{self.fragment_id}]: {self.name}\n\"{self.content}\""

class LoreSystem:
    def __init__(self):
        self.found_fragments = []
        self.all_lore = {
            "frag1": LoreItem("The Arrival", "The sky turned red, and the cities fell. We fled to the forests...", "frag1"),
            "frag2": LoreItem("The Sickness", "The water began to taste like iron. Then the people began to change...", "frag2"),
            "frag3": LoreItem("The Last Hope", "They say there is a sanctuary in the North. If you find the map...", "frag3")
        }

    def add_fragment(self, frag_id):
        if frag_id in self.all_lore and frag_id not in self.found_fragments:
            fragment = self.all_lore[frag_id]
            self.found_fragments.append(fragment)
            print(f"[*] You found a piece of history: {fragment.name}!")
            return fragment
        return None

    def read_lore(self):
        if not self.found_fragments:
            print("[!] You haven't found any lore fragments yet.")
            return
        
        print("\n=== ARCHIVES ===")
        for frag in self.found_fragments:
            print(frag)
            print("-" * 20)
