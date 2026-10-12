import azure.functions as func
import os
import json
import time
import requests

# ============================================
# CONFIGURATION - Set these in Azure Function App Settings
# ============================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
OPENAI_TIMEOUT = int(os.getenv("OPENAI_TIMEOUT", "30"))

# Optional comma-separated allowlist of models clients may request.
# When empty, any model name is accepted (the default is always allowed).
OPENAI_ALLOWED_MODELS = [
    m.strip() for m in os.getenv("OPENAI_ALLOWED_MODELS", "").split(",") if m.strip()
]

# Simple in-memory rate limiter (best-effort, per instance).
# Key: client IP -> timestamp of last accepted request.
_LAST_REQUEST = {}
_RATE_LIMIT_SECONDS = int(os.getenv("OPENAI_RATE_LIMIT_SECONDS", "30"))

VALID_ROLES = {"system", "user", "assistant"}
MAX_MESSAGES = 50
MAX_TOTAL_CHARS = 24000
MAX_TEMPERATURE = 2.0
MAX_TOKENS_LIMIT = 4096


def _error_response(message: str, status: int = 400) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"success": False, "message": message}),
        status_code=status,
        mimetype="application/json"
    )


def _success_response(reply: str, model: str) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"success": True, "reply": reply, "model": model}),
        status_code=200,
        mimetype="application/json"
    )


def _validate_config() -> func.HttpResponse | None:
    if not OPENAI_API_KEY:
        return _error_response(
            "Server configuration incomplete. Contact administrator.",
            status=500
        )
    return None


def _client_ip(req: func.HttpRequest) -> str:
    """Best-effort client IP from SWA/Functions forwarded headers."""
    forwarded = req.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return req.headers.get("x-client-ip") or "unknown"


def _rate_limited(ip: str) -> bool:
    now = time.time()
    last = _LAST_REQUEST.get(ip, 0)
    if now - last < _RATE_LIMIT_SECONDS:
        return True
    _LAST_REQUEST[ip] = now
    return False


def _validate_messages(messages: object) -> tuple[bool, str, list[dict]]:
    """Validate and normalize the incoming chat messages."""
    if not isinstance(messages, list) or not messages:
        return False, "Field 'messages' must be a non-empty array", []
    if len(messages) > MAX_MESSAGES:
        return False, f"Too many messages (max {MAX_MESSAGES})", []

    normalized: list[dict] = []
    total_chars = 0
    for message in messages:
        if not isinstance(message, dict):
            return False, "Each message must be an object with 'role' and 'content'", []
        role = message.get("role")
        content = message.get("content")
        if role not in VALID_ROLES:
            return False, f"Invalid role '{role}'. Expected one of: {', '.join(sorted(VALID_ROLES))}", []
        if not isinstance(content, str) or not content.strip():
            return False, "Each message 'content' must be a non-empty string", []
        total_chars += len(content)
        if total_chars > MAX_TOTAL_CHARS:
            return False, "Conversation is too long", []
        normalized.append({"role": role, "content": content})

    return True, "", normalized


def _resolve_model(requested: object) -> tuple[bool, str, str]:
    """Pick the model to use, enforcing the optional allowlist."""
    if requested is None:
        return True, "", OPENAI_MODEL
    if not isinstance(requested, str) or not requested.strip():
        return False, "Field 'model' must be a non-empty string", ""
    model = requested.strip()
    if model == OPENAI_MODEL or model in OPENAI_ALLOWED_MODELS:
        return True, "", model
    return False, "Requested model is not allowed", ""


def _call_openai(payload: dict) -> tuple[bool, str, str, int]:
    """Call the OpenAI chat completions API.

    Returns (success, reply_or_message, model, status_code).
    """
    try:
        response = requests.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=OPENAI_TIMEOUT,
        )
    except requests.Timeout:
        return False, "The AI service timed out. Please try again.", "", 504
    except requests.RequestException:
        return False, "Could not reach the AI service. Please try again.", "", 502

    if response.status_code == 429:
        return False, "The AI service is rate limited. Please try again shortly.", "", 429
    if response.status_code >= 400:
        return False, "The AI service returned an error.", "", 502

    try:
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        return False, "Received an unexpected response from the AI service.", "", 502

    if not isinstance(reply, str) or not reply.strip():
        return False, "The AI service returned an empty response.", "", 502

    model = data.get("model") or payload.get("model", OPENAI_MODEL)
    return True, reply, model, 200


def main(req: func.HttpRequest) -> func.HttpResponse:
    config_error = _validate_config()
    if config_error:
        return config_error

    if _rate_limited(_client_ip(req)):
        return _error_response("Too many requests. Please wait a moment.", status=429)

    try:
        req_body = req.get_json()
    except ValueError:
        return _error_response("Invalid request body")

    if not isinstance(req_body, dict):
        return _error_response("Invalid request body")

    ok, message, messages = _validate_messages(req_body.get("messages"))
    if not ok:
        return _error_response(message)

    ok, message, model = _resolve_model(req_body.get("model"))
    if not ok:
        return _error_response(message)

    payload: dict = {"model": model, "messages": messages}

    temperature = req_body.get("temperature")
    if temperature is not None:
        if not isinstance(temperature, (int, float)) or isinstance(temperature, bool):
            return _error_response("Field 'temperature' must be a number")
        if not 0 <= float(temperature) <= MAX_TEMPERATURE:
            return _error_response(f"Field 'temperature' must be between 0 and {MAX_TEMPERATURE}")
        payload["temperature"] = float(temperature)

    max_tokens = req_body.get("max_tokens")
    if max_tokens is not None:
        if not isinstance(max_tokens, int) or isinstance(max_tokens, bool):
            return _error_response("Field 'max_tokens' must be an integer")
        if max_tokens <= 0 or max_tokens > MAX_TOKENS_LIMIT:
            return _error_response(f"Field 'max_tokens' must be between 1 and {MAX_TOKENS_LIMIT}")
        payload["max_tokens"] = max_tokens

    ok, reply, response_model, status = _call_openai(payload)
    if not ok:
        return _error_response(reply, status=status)

    return _success_response(reply, response_model)
