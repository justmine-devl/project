import random

class Weather:
    def __init__(self):
        self.conditions = ["Sunny", "Rainy", "Stormy", "Cold Snap", "Heatwave"]
        self.current_condition = "Sunny"
        self.temperature = 20 # Celsius

    def update(self):
        """Change weather randomly every few turns."""
        self.current_condition = random.choice(self.conditions)
        
        if self.current_condition == "Sunny":
            self.temperature = random.randint(15, 25)
        elif self.current_condition == "Rainy":
            self.temperature = random.randint(10, 18)
        elif self.current_condition == "Stormy":
            self.temperature = random.randint(5, 15)
        elif self.current_condition == "Cold Snap":
            self.temperature = random.randint(-10, 5)
        elif self.current_condition == "Heatwave":
            self.temperature = random.randint(30, 40)
        
        print(f"[*] Weather changed to {self.current_condition}. Temperature: {self.temperature}°C")

    def __str__(self):
        return f"Weather: {self.current_condition} | Temp: {self.temperature}°C"
