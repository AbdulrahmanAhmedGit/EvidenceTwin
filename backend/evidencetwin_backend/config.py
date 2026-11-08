"""Server-only runtime configuration. Never serialize credentials to the browser."""
import os
from typing import Any
from urllib.parse import urlsplit

def _positive_integer(name: str, default: int) -> int:
    value = int(os.environ.get(name, str(default)))
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value

def load_config() -> dict[str, Any]:
    origins = [value.strip() for value in os.environ.get("EVIDENCETWIN_CORS_ORIGINS", "").split(",") if value.strip()]
    provider = os.getenv("EVIDENCETWIN_PROVIDER", "ollama").lower()
    if provider not in {"ollama", "openai", "google", "anthropic", "openrouter", "deepseek"}:
        raise ValueError("Unsupported EVIDENCETWIN_PROVIDER")
    host = os.getenv("OLLAMA_HOST", "https://ollama.com").rstrip("/")
    parsed = urlsplit(host)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password or parsed.path or parsed.query or parsed.fragment:
        raise ValueError("OLLAMA_HOST must be an HTTP(S) origin without credentials or a path")
    if parsed.scheme == "http" and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("Remote Ollama endpoints require HTTPS")
    key = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "") if provider == "google" else os.getenv(provider.upper()+"_API_KEY", "")
    return {
        "RUNTIME_ENABLED": os.getenv("EVIDENCETWIN_RUNTIME", "1").lower() not in {"0", "false"},
        "DATA_DIRECTORY": os.getenv("EVIDENCETWIN_DATA_DIRECTORY", str(__import__("pathlib").Path(__file__).resolve().parents[1]/"instance")),
        "WORKERS": _positive_integer("EVIDENCETWIN_WORKERS", 2),
        "QUEUE_LIMIT": _positive_integer("EVIDENCETWIN_QUEUE_LIMIT", 16),
        "AI_PROVIDER_KEYS": {name: (os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")) if name == "google" else os.getenv(name.upper()+"_API_KEY", "") for name in ("ollama", "openai", "google", "anthropic", "openrouter", "deepseek")},
        "AI_PROVIDER": provider,
        "AI_MODEL": os.getenv("EVIDENCETWIN_MODEL", ""),
        "AI_API_KEY": key,
        "OLLAMA_HOST": host,
        "OLLAMA_API_KEY": os.getenv("OLLAMA_API_KEY", ""),
        "OLLAMA_MODEL": os.getenv("EVIDENCETWIN_MODEL", ""),
        "OLLAMA_SCHEMA_MODE": os.getenv("OLLAMA_SCHEMA_MODE", "0" if parsed.hostname == "ollama.com" else "1").lower() not in {"0", "false"},
        "OLLAMA_TIMEOUT": _positive_integer("EVIDENCETWIN_PROVIDER_TIMEOUT", 180),
        "MAX_CONTENT_LENGTH": _positive_integer("EVIDENCETWIN_MAX_CONTENT_LENGTH", 64 * 1024 * 1024),
        "MAX_FORM_MEMORY_SIZE": _positive_integer("EVIDENCETWIN_MAX_FORM_MEMORY_SIZE", 512 * 1024),
        "MAX_FORM_PARTS": _positive_integer("EVIDENCETWIN_MAX_FORM_PARTS", 32),
        "CORS_ALLOWED_ORIGINS": origins,
        "LIBRETRANSLATE_URL": os.getenv("EVIDENCETWIN_LIBRETRANSLATE_URL", "http://127.0.0.1:5002"),
        "LIBRETRANSLATE_API_KEY": os.getenv("EVIDENCETWIN_LIBRETRANSLATE_API_KEY", ""),
        # Owner hook: authenticate/authorize or raise Unauthorized/Forbidden.
        # No token parser, principal, login route or session is fabricated.
        "AUTHENTICATE_REQUEST": None,
        "ACCOUNTS_ENABLED": os.getenv("EVIDENCETWIN_ACCOUNTS", "0") == "1",
        "SECRET_KEY": os.getenv("EVIDENCETWIN_SESSION_SECRET"),
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_NAME": "evidencetwin_session",
        "SESSION_COOKIE_PATH": "/api",
        "SESSION_COOKIE_SAMESITE": "Strict",
        "SESSION_COOKIE_SECURE": os.getenv("EVIDENCETWIN_SECURE_COOKIES", "0") == "1",
    }

def validate_origins(origins: list[str]) -> None:
    if not isinstance(origins, list):
        raise ValueError("CORS_ALLOWED_ORIGINS must be a list of exact HTTP(S) origins")
    for origin in origins:
        if not isinstance(origin, str):
            raise ValueError("Each CORS origin must be a string")
        parsed = urlsplit(origin)
        # Accessing .port validates malformed and out-of-range ports.
        _ = parsed.port
        if (parsed.scheme not in {"http", "https"} or not parsed.netloc or not parsed.hostname or parsed.username
                or parsed.password or parsed.path or parsed.query or parsed.fragment or "*" in origin or any(c.isspace() for c in origin)):
            raise ValueError("CORS origins must be exact HTTP(S) origins without paths, wildcards or credentials")
