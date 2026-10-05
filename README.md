# 🧪 SMSGate Webhook Processor (FastAPI)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stars][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

A FastAPI example that registers an SMS webhook with the SMS Gateway API, validates incoming payloads (HMAC signature and schema), and prints received messages. Part of the SMSGate ecosystem - see the [webhooks guide](https://docs.sms-gate.app/getting-started/webhooks/).

## 📖 About

This example ([main.py](main.py)) demonstrates the full webhook lifecycle: it registers a webhook with the SMS Gateway 3rd-party API on startup, receives `sms:received` events, verifies the optional HMAC signature, validates the payload with Pydantic models, and unregisters the webhook on shutdown.

## 📚 Table of Contents

- [📖 About](#-about)
- [📚 Table of Contents](#-table-of-contents)
- [⭐ Features](#-features)
- [📦 Prerequisites](#-prerequisites)
- [🚀 Quickstart](#-quickstart)
- [💻 Usage](#-usage)
- [🔌 How It Works](#-how-it-works)
- [📚 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)
- [⚖️ License](#️-license)

## ⭐ Features

- Webhook registration and deregistration in the app lifespan
- Optional HMAC-SHA256 signature verification (`X-Signature` / `X-Timestamp` headers)
- Pydantic payload validation (`WebhookPayload` / `SMSReceivedData` models)
- HTTPS mode with configurable SSL certificate and key

## 📦 Prerequisites

- Python 3.11+ (per [Pipfile](Pipfile))
- SMS Gateway for Android installed and configured on a device
- SMS Gateway API username and password
- A publicly reachable HTTPS URL (or tunnel) for webhook delivery - see the [webhooks guide](https://docs.sms-gate.app/getting-started/webhooks/)

## 🚀 Quickstart

1. Clone and install dependencies:

```bash
git clone https://github.com/android-sms-gateway/example-webhooks-fastapi.git
cd example-webhooks-fastapi
pip install -r requirements.txt
```

Pipenv users can run `pipenv install` instead.

2. Configure the environment:

```bash
cp .env.example .env
```

Set at least `SMS_GATE_API_USERNAME`, `SMS_GATE_API_PASSWORD`, and `WEBHOOK_URL` (the public URL of your server, e.g. `https://yourhost/webhook/sms-received`). See [.env.example](.env.example) for all variables:

| Variable | Description |
| -------- | ----------- |
| `SMS_GATE_API_URL` | API root (default `https://api.sms-gate.app/3rdparty/v1`) |
| `SMS_GATE_API_USERNAME` | SMS Gateway API username |
| `SMS_GATE_API_PASSWORD` | SMS Gateway API password |
| `WEBHOOK_SECRET` | Signing key for HMAC headers (optional) |
| `WEBHOOK_URL` | Public URL of the webhook endpoint |
| `SSL_CERT_PATH`, `SSL_KEY_PATH` | Serve HTTPS on 8443 instead of HTTP on 8080 (optional) |

3. Start the server:

```bash
uvicorn main:app --reload
```

Without SSL the server listens on `http://0.0.0.0:8080`; with `SSL_CERT_PATH` and `SSL_KEY_PATH` set it listens on `https://0.0.0.0:8443` (`python main.py` runs the same app). On startup the app registers the webhook with the API and prints its ID - keep it for the verification step below.

## 💻 Usage

Verify the webhook end to end:

1. Keep the server running and note the registered webhook ID from the startup log.
2. Open [requests.http](requests.http), replace the `webhookId` value with the registered ID, and send the POST via the REST Client extension - or use curl:

```bash
curl -X POST http://localhost:8080/webhook/sms-received \
  -H "Content-Type: application/json" \
  -d '{"deviceId":"demo-device","event":"sms:received","id":"req-1","webhookId":"<REGISTERED_ID>","payload":{"message":"Hello from SMSGate","receivedAt":"2026-08-22T12:00:00.000+07:00","messageId":"m1","phoneNumber":"+12025550123","simNumber":1}}'
```

3. The received SMS is printed to the server console and the API answers `{"status": "ok"}`.

When `WEBHOOK_SECRET` is set, the server requires `X-Signature` and `X-Timestamp` headers: `X-Signature` is the lowercase hex HMAC-SHA256 of the raw request body concatenated with the `X-Timestamp` value.

## 🔌 How It Works

All logic lives in [main.py](main.py):

1. `Settings` (Pydantic `BaseSettings`) loads configuration from `.env`
2. `register_webhook` / `unregister_webhook` manage the webhook in the app lifespan
3. `handle_sms_webhook` verifies the HMAC signature (when `WEBHOOK_SECRET` is set), validates the payload against the Pydantic models, checks the webhook ID, and prints the received message

## 📚 Documentation

- [Central docs](https://docs.sms-gate.app/)
- [Webhooks guide](https://docs.sms-gate.app/getting-started/webhooks/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [GitHub repository](https://github.com/android-sms-gateway/example-webhooks-fastapi)

## 🤝 Contributing

Contributions are welcome - open an issue or submit a pull request on the [GitHub repository](https://github.com/android-sms-gateway/example-webhooks-fastapi).

## ⚖️ License

Apache-2.0. See [LICENSE](LICENSE).

<!-- Reference-style badge URLs: style=for-the-badge is mandatory -->
[contributors-shield]: https://img.shields.io/github/contributors/android-sms-gateway/example-webhooks-fastapi?style=for-the-badge
[contributors-url]: https://github.com/android-sms-gateway/example-webhooks-fastapi/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/android-sms-gateway/example-webhooks-fastapi?style=for-the-badge
[forks-url]: https://github.com/android-sms-gateway/example-webhooks-fastapi/network/members
[stars-shield]: https://img.shields.io/github/stars/android-sms-gateway/example-webhooks-fastapi?style=for-the-badge
[stars-url]: https://github.com/android-sms-gateway/example-webhooks-fastapi/stargazers
[issues-shield]: https://img.shields.io/github/issues/android-sms-gateway/example-webhooks-fastapi?style=for-the-badge
[issues-url]: https://github.com/android-sms-gateway/example-webhooks-fastapi/issues
[license-shield]: https://img.shields.io/github/license/android-sms-gateway/example-webhooks-fastapi?style=for-the-badge
[license-url]: https://github.com/android-sms-gateway/example-webhooks-fastapi/blob/master/LICENSE
