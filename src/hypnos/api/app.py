from fastapi import FastAPI

from hypnos.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="HYPNOS Gateway", version="0.1.0")

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok", "env": settings.app_env}

    return app


app = create_app()
