import azure.functions as func
import os
import json
import re
import requests
from requests.auth import HTTPBasicAuth

# ============================================
# CONFIGURATION - Set these in Azure Function App Settings
# ============================================
# Unified OpenAI-compatible MLflow gateway endpoint.
# e.g. https://sandbox-mlflow.gilmanuel.com/gateway/mlflow/v1
MLFLOW_GATEWAY_URL = os.getenv("MLFLOW_GATEWAY_URL", "").rstrip("/")
MLFLOW_GATEWAY_USER = os.getenv("MLFLOW_GATEWAY_USER")
MLFLOW_GATEWAY_PASSWORD = os.getenv("MLFLOW_GATEWAY_PASSWORD")
MLFLOW_GATEWAY_DEFAULT_MODEL = os.getenv("MLFLOW_GATEWAY_DEFAULT_MODEL", "gpt-4o-mini")
MLFLOW_GATEWAY_TIMEOUT = int(os.getenv("MLFLOW_GATEWAY_TIMEOUT", "30"))

# Optional comma-separated allowlist of gateway endpoint names clients may
# request. When empty, any endpoint name is accepted (the default is always
# allowed).
MLFLOW_GATEWAY_ALLOWED_MODELS = [
    m.strip() for m in os.getenv("MLFLOW_GATEWAY_ALLOWED_MODELS", "").split(",") if m.strip()
]

VALID_ROLES = {"system", "user", "assistant"}
MAX_MESSAGES = 50
MAX_TOTAL_CHARS = 24000
MAX_TEMPERATURE = 2.0
MAX_TOKENS_LIMIT = 4096


def _error_response(message: str, status: int = 400, code: str | None = None) -> func.HttpResponse:
    body = {"success": False, "message": message}
    if code:
        body["code"] = code
    return func.HttpResponse(
        json.dumps(body),
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
    if not MLFLOW_GATEWAY_URL or not MLFLOW_GATEWAY_USER or not MLFLOW_GATEWAY_PASSWORD:
        return _error_response(
            "Server configuration incomplete. Contact administrator.",
            status=500
        )
    return None


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
    """Pick the gateway endpoint name to use, enforcing the optional allowlist."""
    if requested is None:
        return True, "", MLFLOW_GATEWAY_DEFAULT_MODEL
    if not isinstance(requested, str) or not requested.strip():
        return False, "Field 'model' must be a non-empty string", ""
    model = requested.strip()
    if model == MLFLOW_GATEWAY_DEFAULT_MODEL or model in MLFLOW_GATEWAY_ALLOWED_MODELS:
        return True, "", model
    return False, "Requested model is not allowed", ""


GUARDRAIL_RE = re.compile(r"guardrail ['\"]?([^'\"]+)['\"]? blocked", re.IGNORECASE)


def _guardrail_violation(response: requests.Response) -> str | None:
    """Return the guardrail name when the gateway blocked the request, else None.

    MLflow's gateway raises ``GuardrailViolation`` as ``{"detail": "Guardrail
    '<name>' blocked: <rationale>"}``. We detect it from the body so the exact
    upstream status code (400/500) doesn't matter.
    """
    try:
        body = response.json()
    except ValueError:
        body = None

    text = ""
    if isinstance(body, dict):
        for key in ("detail", "message", "error"):
            value = body.get(key)
            if isinstance(value, str) and value:
                text = value
                break
    if not text:
        text = response.text or ""

    lowered = text.lower()
    if "guardrail" not in lowered or "blocked" not in lowered:
        return None
    match = GUARDRAIL_RE.search(text)
    return match.group(1).strip() if match else "guardrail"


def _call_gateway(payload: dict) -> tuple[bool, str, str, int, str]:
    """Call the MLflow gateway OpenAI-compatible chat completions endpoint.

    Returns (success, reply_or_message, model, status_code, code).
    """
    try:
        response = requests.post(
            f"{MLFLOW_GATEWAY_URL}/chat/completions",
            auth=HTTPBasicAuth(MLFLOW_GATEWAY_USER, MLFLOW_GATEWAY_PASSWORD),
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=MLFLOW_GATEWAY_TIMEOUT,
        )
    except requests.Timeout:
        return False, "The AI service timed out. Please try again.", "", 504, "timeout"
    except requests.RequestException:
        return False, "Could not reach the AI service. Please try again.", "", 502, "network"

    if response.status_code == 429:
        return False, "The AI service is rate limited. Please try again shortly.", "", 429, "rate_limited"
    if response.status_code in (401, 403):
        return False, "The AI service rejected the request.", "", 502, "auth"
    if response.status_code >= 400:
        if _guardrail_violation(response) is not None:
            return False, "Blocked by the safety filter.", "", 400, "guardrail"
        return False, "The AI service returned an error.", "", 502, "upstream"

    try:
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        return False, "Received an unexpected response from the AI service.", "", 502, "invalid_response"

    if not isinstance(reply, str) or not reply.strip():
        return False, "The AI service returned an empty response.", "", 502, "empty_response"

    model = data.get("model") or payload.get("model", MLFLOW_GATEWAY_DEFAULT_MODEL)
    return True, reply, model, 200, ""


def main(req: func.HttpRequest) -> func.HttpResponse:
    config_error = _validate_config()
    if config_error:
        return config_error

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

    ok, reply, response_model, status, code = _call_gateway(payload)
    if not ok:
        return _error_response(reply, status=status, code=code)

    return _success_response(reply, response_model)
