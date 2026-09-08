import json

from models.event import ChatEvent


def sse(data: ChatEvent):

    return f"data:{data.model_dump_json()}\n\n"