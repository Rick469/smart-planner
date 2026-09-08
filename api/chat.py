from fastapi import APIRouter, Request

from models.schema import IntentRequest
from service.chat_service import ChatService
from starlette.responses import StreamingResponse

from utils.sse import sse

router=APIRouter()



@router.post("/stream")
async def chat(
    req:Request,
    body:IntentRequest
):

    chat_service = req.app.state.chat_service

    async def generator():

        async for event in chat_service.stream_chat(body):

            yield sse(event)



    return StreamingResponse(
        generator(),
        media_type="text/event-stream"
    )