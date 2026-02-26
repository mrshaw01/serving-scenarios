from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any


def load_dotenv(path: str | Path = ".env") -> None:
    dotenv_path = Path(path)
    if not dotenv_path.exists() and not dotenv_path.is_absolute():
        for parent in [Path.cwd(), *Path.cwd().parents]:
            candidate = parent / dotenv_path
            if candidate.exists():
                dotenv_path = candidate
                break
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _read_required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _ensure_v1_suffix(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if not normalized.endswith("/v1"):
        raise ValueError("OPENAI_BASE_URL must include '/v1' suffix.")
    return normalized


def _parse_int_list(raw: str) -> list[int]:
    values: list[int] = []
    for piece in raw.split(","):
        item = piece.strip()
        if not item:
            continue
        number = int(item)
        if number <= 0:
            raise ValueError("Token targets must be positive integers.")
        values.append(number)
    if not values:
        raise ValueError(
            "SCENARIO_TOKEN_TARGETS must contain at least one value.")
    return values


@dataclass(frozen=True)
class Settings:
    openai_base_url: str
    openai_api_key: str
    tensormesh_user_id: str
    openai_model: str
    request_timeout_s: float
    token_targets: list[int]
    max_tokens: int
    temperature: float
    manual_seed: int
    manual_sections: int
    kv_metric_response_field: str | None

    @classmethod
    def from_env(cls, load_env_file: bool = True) -> "Settings":
        if load_env_file:
            load_dotenv()

        return cls(
            openai_base_url=_ensure_v1_suffix(
                _read_required("OPENAI_BASE_URL")),
            openai_api_key=_read_required("OPENAI_API_KEY"),
            tensormesh_user_id=_read_required("TENSORMESH_USER_ID"),
            openai_model=_read_required("OPENAI_MODEL"),
            request_timeout_s=float(os.environ.get("REQUEST_TIMEOUT_S",
                                                   "300")),
            token_targets=_parse_int_list(
                os.environ.get(
                    "SCENARIO_TOKEN_TARGETS",
                    "4000,8000,12000,16000,20000,24000,28000,32000,36000,40000",
                )),
            max_tokens=int(os.environ.get("MAX_TOKENS", "64")),
            temperature=float(os.environ.get("TEMPERATURE", "0.0")),
            manual_seed=int(os.environ.get("MANUAL_SEED", "17")),
            manual_sections=int(os.environ.get("MANUAL_SECTIONS", "1200")),
            kv_metric_response_field=os.environ.get(
                "KV_METRIC_RESPONSE_FIELD"),
        )

    def openai_client_kwargs(self) -> dict[str, Any]:
        return {
            "api_key": self.openai_api_key,
            "base_url": self.openai_base_url,
            "default_headers": {
                "X-User-Id": self.tensormesh_user_id
            },
            "timeout": self.request_timeout_s,
        }


def create_openai_client(settings: Settings) -> Any:
    from openai import OpenAI

    return OpenAI(**settings.openai_client_kwargs())
