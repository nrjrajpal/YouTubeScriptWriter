class ProjectNotFoundError(Exception):
    """Exception raised when a project is not found in the database."""
    def __init__(self, message="Project not found"):
        self.message = message
        super().__init__(self.message)

class KeyNotFoundError(Exception):
    """Exception raised when a specific key is not found in a database record."""
    def __init__(self, message="Key not found in the database record."):
        self.message = message
        super().__init__(self.message)
        
class GroqAPIKeyNotFoundError(Exception):
    """Exception raised when a specific Groq Api Key is not found in a database record."""
    def __init__(self, message="Groq Api Key not found in the database record."):
        self.message = message
        super().__init__(self.message)
        
class TavilyAPIKeyNotFoundError(Exception):
    """Exception raised when a specific Tavily Api Key is not found in a database record."""
    def __init__(self, message="Tavily Api Key not found in the database record."):
        self.message = message
        super().__init__(self.message)
        
class SerperAPIKeyNotFoundError(Exception):
    """Exception raised when a specific Serper Api Key is not found in a database record."""
    def __init__(self, message="Serper Api Key not found in the database record."):
        self.message = message
        super().__init__(self.message)
        
class UserNotFoundError(Exception):
    """Exception raised when a user is not found in the database."""
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)
