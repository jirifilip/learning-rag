from fastapi import FastAPI
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from pydantic_ai import Agent

resource = Resource.create({
    "service.name": "learning-rag"
})


provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

exporter = OTLPSpanExporter("http://localhost:4318/v1/traces")
processor = BatchSpanProcessor(exporter)
provider.add_span_processor(processor)


metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://localhost:4318/v1/metrics")
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

app = FastAPI()

FastAPIInstrumentor().instrument_app(app)
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)


request_counter = meter.create_counter(
    "app.requests",
    description="Number of requests to the app",
    unit="1"
)


Agent.instrument_all()
agent = Agent(
    "openai:gpt-5-nano",
    output_type=str,
    system_prompt="Answer questions like a bored programmer in short sentences."
)


@app.get("/")
async def root() -> dict[str, str]:
    request_counter.add(1, {"endpoint": "root"})
    return {"message": "Hello World"}


@app.get("/test-trace")
async def test_trace() -> dict[str, str]:
    request_counter.add(1, {"endpoint": "test-trace"})
    with tracer.start_as_current_span("parent-span") as parent:
        parent.set_attribute("app.feature", "tracing-demo")

        with tracer.start_as_current_span("child-span") as child:
            child.set_attribute("app.feature", "tracing-demo")
            child.add_event("Doing some work...")


    return {"message": "Created spans."}


@app.post("/ask")
async def ask(question: str) -> dict[str, str]:
    request_counter.add(1, {"endpoint": "ask"})
    result = await agent.run(question)
    return {"result": result.output}
