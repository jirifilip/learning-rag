from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource.create({
    "service.name": "learning-rag"
})

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

exporter = OTLPSpanExporter("http://localhost:4318/v1/traces")
processor = BatchSpanProcessor(exporter)
provider.add_span_processor(processor)

app = FastAPI()

FastAPIInstrumentor().instrument_app(app)
tracer = trace.get_tracer(__name__)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/test-trace")
async def test_trace() -> dict[str, str]:
    with tracer.start_as_current_span("parent-span") as parent:
        parent.set_attribute("app.feature", "tracing-demo")

        with tracer.start_as_current_span("child-span") as child:
            child.set_attribute("app.feature", "tracing-demo")
            child.add_event("Doing some work...")


    return {"message": "Created spans."}