# 📱 Example SMS Webhook Processor (FastAPI)

[![Example](https://img.shields.io/badge/Type-Example%20Project-orange.svg)](https://github.com/yourusername/sms-webhook-processor)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-%2300C7B7.svg)](https://fastapi.tiangolo.com/)

> **⚠️ Example Project Notice**  
> Not intended for production use without proper security review and modifications.

## 📋 Table of Contents
- [📱 Example SMS Webhook Processor (FastAPI)](#-example-sms-webhook-processor-fastapi)
  - [📋 Table of Contents](#-table-of-contents)
  - [✨ About The Project](#-about-the-project)
    - [🛠️ Built With](#️-built-with)
    - [⚠️ Important Notes](#️-important-notes)
  - [🚀 Getting Started](#-getting-started)
    - [📦 Prerequisites](#-prerequisites)
    - [⚡ Installation](#-installation)
  - [⚙️ Configuration](#️-configuration)
  - [🖥️ Usage](#️-usage)
  - [📚 API Reference](#-api-reference)
    - [`POST /webhook/sms-received`](#post-webhooksms-received)
  - [🤝 Contributing](#-contributing)
  - [📜 License](#-license)

## ✨ About The Project

**Example Project Features**:
- 🧩 Demonstrates webhook registration/deregistration lifecycle
- 🔐 Example HMAC signature validation implementation
- 📝 Sample payload validation using Pydantic models

### 🛠️ Built With

- 🚀 [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- ✔️ [Pydantic](https://pydantic.dev/) - Data validation and settings management
- 🌐 [HTTPX](https://www.python-httpx.org/) - Async HTTP client
- ⚡ [UVicorn](https://www.uvicorn.org/) - ASGI server

### ⚠️ Important Notes

**This example intentionally omits**:

- Production-grade error handling
- Rate limiting
- Persistent storage integration
- Advanced security features

**Recommended for**:

- 🧪 Testing SMS Gate webhook integration
- 🎓 Learning FastAPI webhook implementations

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.9+ (development environment)
- Valid SSL certificate ([project's CA](https://docs.sms-gate.app/services/ca/) available) or reverse proxy (like [ngrok](https://ngrok.com/))
- SMS Gate credentials

### ⚡ Installation

1. Clone the example repository:
    ```bash
    git clone https://github.com/android-sms-gateway/example-webhooks-fastapi.git
    cd example-webhooks-fastapi
    ```

2. Install development dependencies:
    ```bash
    pip install -r requirements.txt
    # or
    pipenv install
    ```

3. Create example environment file:
    ```bash
    cp .env.example .env
    ```

## ⚙️ Configuration

**Example `.env` configuration**:
```ini
# 🔑 Example SMS Gate API Credentials
SMS_GATE_API_URL="https://api.sms-gate.app/3rdparty/v1" # API root endpoint (optional)
SMS_GATE_API_USERNAME="test_user"                       # API username
SMS_GATE_API_PASSWORD="test_password"                   # API password

# 🔒 Example Webhook Security
WEBHOOK_SECRET="your_test_secret_here"                      # signing key (optional)
WEBHOOK_URL="https://localhost:8443/webhook/sms-received"   # current server endpoint

# 🛡️ SSL Configuration
SSL_CERT_PATH="./certs/server.crt"  # SSL certificate (optional)
SSL_KEY_PATH="./certs/server.key"   # SSL private key (optional)
```

## 🖥️ Usage

**Run the example server**:
```bash
python main.py
```

**Expected output**:
```plaintext
INFO:     Started server process [42516]
INFO:     Waiting for application startup.
Registered webhook with ID: mIv93KBZgaFNGrhl_ivk9
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
Received SMS:
SIM: 1
From: 6505551212
Message: Android is always a sweet treat!
Received at: 2025-04-15 12:28:01+07:00
INFO:     169.150.246.92:0 - "POST /webhook/sms-received HTTP/1.1" 200 OK
^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
Unregistered webhook ID: mIv93KBZgaFNGrhl_ivk9
INFO:     Application shutdown complete.
INFO:     Finished server process [42516]
```

## 📚 API Reference

### `POST /webhook/sms-received`

**Example Request**:
```bash
curl -X POST https://localhost:8443/webhook/sms-received \
  -H "X-Signature: abc123..." \
  -H "X-Timestamp: 1690123456" \
  -d @sample_payload.json
```

**Example Response**:
```json
{
  "status": "ok"
}
```

## 🤝 Contributing

This example project welcomes contributions to:

- Improve documentation
- Demonstrate additional features
- Enhance example security implementations

## 📜 License

This example code is released under [Apache License 2.0](LICENSE).
