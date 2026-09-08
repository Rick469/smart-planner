from enum import Enum
from dataclasses import dataclass


class WorkflowEventType(str, Enum):

    THINKING_START = "thinking_start"

    THINKING_END = "thinking_end"

    TOOL_START = "tool_start"

    TOOL_END = "tool_end"

    TOKEN = "token"


@dataclass
class WorkflowEvent:

    type: WorkflowEventType

    content: str | None = None

    title: str | None = None

    tool: str | None = None