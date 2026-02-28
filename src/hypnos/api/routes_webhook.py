from fastapi import APIRouter, Query, Response, status
from fastapi.responses import PlainTextResponse

from hypnos.config import settings

router = APIRouter()


@router.get("/webhook")
def verify_webhook(
    hub_mode: str | None = Query(default=None, alias="hub.mode"),
    hub_verify_token: str | None = Query(default=None, alias="hub.verify_token"),
    hub_challenge: str | None = Query(default=None, alias="hub.challenge"),
) -> Response:
    """
    WhatsApp webhook verification handshake.

    Meta sends query params named hub.mode, hub.verify_token, hub.challenge.
    FastAPI does not convert dots to underscores, so Query aliases are required.
    """
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        return PlainTextResponse(content=hub_challenge or "", status_code=status.HTTP_200_OK)

    return PlainTextResponse(content="forbidden", status_code=status.HTTP_403_FORBIDDEN)
