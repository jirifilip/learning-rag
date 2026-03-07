import os

import logfire
from fastapi import FastAPI
from pydantic_ai import Agent

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


@app.post("/ask")
async def ask(question: str) -> dict[str, str]:
    result = await agent.run(question)
    return {"result": result.output}
