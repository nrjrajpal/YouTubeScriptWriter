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

class ContentNotFoundError(Exception):
    """Exception raised when the raw content from a given url is unavailable."""
    def __init__(self, message="Raw Content not available for the given url"):
        self.message = message
        super().__init__(self.message)