from enum import Enum

from pydantic import BaseModel


class EventType(str, Enum):

    TOKEN = "token"

    THINKING_START = "thinking_start"

    THINKING_END = "thinking_end"

    TOOL_START = "tool_start"

    TOOL_END = "tool_end"

    ERROR = "error"

    DONE = "done"


class ChatEvent(BaseModel):

    type: EventType

    content: str | None = None

    title: str | None = None

    tool: str | None = None

    message: str | None = None