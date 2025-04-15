import hashlib
import hmac
from contextlib import asynccontextmanager
from datetime import datetime

import httpx
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Configuration model
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_url: str = Field(
        "https://api.sms-gate.app/3rdparty/v1", validation_alias="SMS_GATE_API_URL"
    )
    api_username: str | None = Field(None, validation_alias="SMS_GATE_API_USERNAME")
    api_password: str | None = Field(None, validation_alias="SMS_GATE_API_PASSWORD")

    webhook_secret: str | None = Field(None, validation_alias="WEBHOOK_SECRET")
    webhook_url: str | None = Field(None, validation_alias="WEBHOOK_URL")

    ssl_cert: str | None = Field(None, validation_alias="SSL_CERT_PATH")
    ssl_key: str | None = Field(None, validation_alias="SSL_KEY_PATH")


# Webhook payload models
class SMSReceivedData(BaseModel):
    message: str
    received_at: datetime = Field(alias="receivedAt")
    message_id: str = Field(alias="messageId")
    phone_number: str = Field(alias="phoneNumber")
    sim_number: int = Field(alias="simNumber")


class WebhookPayload(BaseModel):
    device_id: str = Field(..., alias="deviceId")
    event: str = Field(..., pattern="^(sms:received)$")
    id: str
    webhook_id: str = Field(..., alias="webhookId")
    payload: SMSReceivedData


settings = Settings()
print(settings.model_dump())


async def register_webhook(app: FastAPI):
    """Register webhook on application startup"""

    if (
        not settings.api_username
        or not settings.api_password
        or not settings.webhook_url
    ):
        return

    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.api_url + "/webhooks",
            auth=httpx.BasicAuth(settings.api_username, settings.api_password),
            json={
                "url": settings.webhook_url,
                "event": "sms:received",
            },
        )
        response.raise_for_status()
        webhook_data = response.json()
        app.state.webhook_id = webhook_data["id"]
        print(f"Registered webhook with ID: {webhook_data['id']}")


async def unregister_webhook(app: FastAPI):
    """Unregister webhook on application shutdown"""

    if (
        not settings.api_username
        or not settings.api_password
        or not settings.webhook_url
        or not hasattr(app.state, "webhook_id")
    ):
        return

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            settings.api_url + f"/webhooks/{app.state.webhook_id}",
            auth=httpx.BasicAuth(settings.api_username, settings.api_password),
        )
        response.raise_for_status()
        print(f"Unregistered webhook ID: {app.state.webhook_id}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the lifespan of the FastAPI application.
    """

    await register_webhook(app)
    yield
    await unregister_webhook(app)


app = FastAPI(lifespan=lifespan)


@app.post("/webhook/sms-received")
async def handle_sms_webhook(request: Request):
    """Handle incoming SMS received webhooks"""
    # Verify HMAC signature
    body = await request.body()

    if settings.webhook_secret:
        signature = request.headers.get("X-Signature")
        timestamp = request.headers.get("X-Timestamp")
        if not signature or not timestamp:
            raise HTTPException(status_code=401, detail="Missing signature header")

        expected_signature = hmac.new(
            settings.webhook_secret.encode(), body + timestamp.encode(), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse and validate payload
    try:
        payload = WebhookPayload.model_validate_json(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid payload format") from e

    if payload.webhook_id != app.state.webhook_id:
        raise HTTPException(status_code=400, detail="Invalid webhook ID")

    # Print received payload to console
    print("Received SMS:")
    print(f"SIM: {payload.payload.sim_number}")
    print(f"From: {payload.payload.phone_number}")
    print(f"Message: {payload.payload.message}")
    print(f"Received at: {payload.payload.received_at}")

    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080 if not settings.ssl_cert or not settings.ssl_key else 8443,
        ssl_keyfile=settings.ssl_key,
        ssl_certfile=settings.ssl_cert,
    )
