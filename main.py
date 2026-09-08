from contextlib import asynccontextmanager
from fastapi import FastAPI
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from utils.logger import log
import os
from service.agent_registry import AgentRegistry
from service.chat_service import ChatService
from api.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app:FastAPI):

    db_url=os.getenv("DB_URL")
    if not db_url:
        raise ValueError('DB_URL未配置！')


    async with AsyncPostgresSaver.from_conn_string(db_url) as checkpointer:

        await checkpointer.setup()


        app.state.agents = AgentRegistry(checkpointer)
        app.state.chat_service = ChatService(app.state.agents)
        log.info('Agent注册完成...')

        yield


app = FastAPI(

    title="Smart Planner",

    lifespan=lifespan

)

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

    expose_headers=[
        "Content-Type"
    ]

)

app.include_router(
    chat_router,
    prefix="/api/chat",
    tags=["chat"]
)