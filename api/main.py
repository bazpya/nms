from fastapi import FastAPI
from pydantic import BaseModel


class Message(BaseModel):
    title: str
    body: str


app = FastAPI()


@app.get("/")
async def root() -> str:
    message = """To try this API using Swagger UI browse /docs.
    To see its interface definition browse /redoc"""
    return message


@app.get("/echo/{text}")
async def echo(text: str) -> str:
    return f"You said: {text}"


@app.get("/version")
async def echo() -> str:
    return app.version


@app.post("/echo")
async def parse_message(message: Message) -> Message:
    return message
