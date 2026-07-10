from fastapi import APIRouter, Request

from service.chat_service import ChatService
from starlette.responses import StreamingResponse

router=APIRouter()



@router.post("/chat/stream")
async def chat(
    req:Request,
    body:dict
):


    agents=req.app.state.agents


    chat_service = ChatService(agents)

    async def generator():


        async for item in chat_service.stream_chat(
            body["message"]
        ):

            yield item



    return StreamingResponse(
        generator(),
        media_type="text/event-stream"
    )