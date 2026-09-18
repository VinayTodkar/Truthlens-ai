from fastapi import FastAPI

from backend.api.routes import router


app = FastAPI(
    title="TruthLens AI",
    description=(
        "AI-powered misinformation and "
        "fact verification system."
    ),
    version="1.0.0"
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "application": "TruthLens AI",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }