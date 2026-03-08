import os
from contextlib import asynccontextmanager
from typing import Annotated

import aio_pika
import logfire
from aio_pika.abc import AbstractRobustChannel
from fastapi import FastAPI, Depends
from pydantic_ai import Agent

from learning_rag.dependencies import get_rabbitmq_client

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4318"

logfire.configure(send_to_logfire=False, service_name="learning-rag")
logfire.instrument_pydantic_ai()

app = FastAPI()
logfire.instrument_fastapi(app)

agent = Agent(
    "openai:gpt-5-nano",
    output_type=str,
    system_prompt="Answer questions like a bored programmer in short sentences."
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/test-trace")
async def test_trace() -> dict[str, str]:
    with logfire.span("parent-span") as parent:
        parent.set_attribute("app.feature", "tracing-demo")

        with logfire.span("child-span") as child:
            child.set_attribute("app.feature", "tracing-demo")
            child.add_event("Doing some work...")


    return {"message": "Created spans."}


@app.post("/test-rabbitmq")
async def test_rabbitmq(rabbit_channel: Annotated[AbstractRobustChannel, Depends(get_rabbitmq_client)]) -> dict[str, str]:
    queue_name = "hello_world_queue"
    await rabbit_channel.declare_queue(queue_name)

    with logfire.span("testing_rabbit_mq") as span_rabbitmq:
        await rabbit_channel.default_exchange.publish(
            aio_pika.Message(body='{"hello": "world"}'.encode()),
            routing_key=queue_name
        )

    return {"message": "Message sent."}


@app.post("/ask")
async def ask(question: str) -> dict[str, str]:
    result = await agent.run(question)
    return {"result": result.output}
