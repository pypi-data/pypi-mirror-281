from langroid.utils.configuration import settings as lsettings
lsettings.cache_type = "fakeredis"
import langroid as lr
from pydantic import BaseModel


# Wrapper for langroid agents
class Agent(BaseModel):
    agent: lr.ChatAgent
    task: lr.Task = None
    msgs: int = 0
    class Config:
        arbitrary_types_allowed = True

### Models for Kopi

### Models for Lumina

### Other Models

# Define the ANSI escape sequences for various colors and reset
class Colors(BaseModel):
    RED: str = "\033[31m"
    BLUE: str = "\033[34m"
    GREEN: str = "\033[32m"
    ORANGE: str = "\033[33m"  # no standard ANSI color for orange; using yellow
    CYAN: str = "\033[36m"
    MAGENTA: str = "\033[35m"
    YELLOW: str = "\033[33m"
    BLACK: str = "\033[30m"
    RESET: str = "\033[0m"

