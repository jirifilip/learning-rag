from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


app = FastAPI()

FastAPIInstrumentor().instrument_app(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}
