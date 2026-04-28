class TimeSystem:
    def __init__(self):
        self.hour = 8 # Start at 8 AM
        self.day = 1
        self.is_night = False

    def advance_time(self, hours=4):
        """Advances time. Each action usually takes some hours."""
        self.hour += hours
        
        if self.hour >= 24:
            self.hour -= 24
            self.day += 1
            print(f"\n*** Day {self.day} has dawned! ***")
        
        # Night is between 8 PM (20) and 6 AM (6)
        self.is_night = self.hour >= 20 or self.hour < 6
        
        time_str = f"{self.hour:02d}:00"
        period = "Night" if self.is_night else "Day"
        print(f"[*] Time is now {time_str} ({period})")

    def __str__(self):
        period = "Night" if self.is_night else "Day"
        return f"Day {self.day} | Time: {self.hour:02d}:00 ({period})"
