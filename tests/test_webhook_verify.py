from fastapi import FastAPI
from fastapi.testclient import TestClient

from hypnos.api.routes_webhook import router


def make_client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_verify_webhook_success(monkeypatch) -> None:
    # Ensure predictable token for test
    monkeypatch.setattr("hypnos.config.settings.whatsapp_verify_token", "test-token")

    client = make_client()
    resp = client.get(
        "/webhook",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "test-token",
            "hub.challenge": "123",
        },
    )

    assert resp.status_code == 200
    assert resp.text == "123"
    assert resp.headers["content-type"].startswith("text/plain")


def test_verify_webhook_wrong_token(monkeypatch) -> None:
    monkeypatch.setattr("hypnos.config.settings.whatsapp_verify_token", "test-token")

    client = make_client()
    resp = client.get(
        "/webhook",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "nope",
            "hub.challenge": "123",
        },
    )

    assert resp.status_code == 403
    assert resp.text == "forbidden"


def test_verify_webhook_missing_params(monkeypatch) -> None:
    monkeypatch.setattr("hypnos.config.settings.whatsapp_verify_token", "test-token")

    client = make_client()
    resp = client.get("/webhook")

    assert resp.status_code == 403
    assert resp.text == "forbidden"


def test_verify_webhook_missing_challenge(monkeypatch) -> None:
    monkeypatch.setattr("hypnos.config.settings.whatsapp_verify_token", "test-token")

    client = make_client()
    resp = client.get(
        "/webhook",
        params={"hub.mode": "subscribe", "hub.verify_token": "test-token"},
    )

    assert resp.status_code == 403
    assert resp.text == "forbidden"
