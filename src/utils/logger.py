class GameLogger:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener_func):
        """Add a function that will be called whenever a message is logged."""
        self.listeners.append(listener_func)

    def log(self, message, level="info"):
        # Default terminal output
        prefix = {
            "info": "[*]",
            "warning": "[!]",
            "alert": "***",
            "combat": "[COMBAT]"
        }.get(level, "[*]")
        
        formatted_message = f"{prefix} {message}"
        
        # Print to console by default
        print(formatted_message)
        
        # Notify all GUI listeners
        for listener in self.listeners:
            listener(formatted_message)

# Global logger instance
logger = GameLogger()
