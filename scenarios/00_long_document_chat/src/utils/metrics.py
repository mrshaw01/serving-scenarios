from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from time import perf_counter
from typing import Any, Iterable, Mapping

from src.config import Settings


@dataclass
class StreamingResult:
    ttft_ms: float | None
    latency_ms: float
    text: str
    usage: dict[str, Any] | None
    response_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class KVReuseMetric:
    label: str
    method: str
    value: float | None
    available: bool
    details: dict[str, Any] = field(default_factory=dict)


def _to_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "to_dict"):
        return value.to_dict()
    try:
        return dict(value)
    except Exception:
        return {}


def _extract_delta_text(chunk: Mapping[str, Any]) -> str:
    choices = chunk.get("choices")
    if not isinstance(choices, list):
        return ""

    text_parts: list[str] = []
    for choice in choices:
        if not isinstance(choice, dict):
            continue
        delta = choice.get("delta")
        if not isinstance(delta, dict):
            continue
        content = delta.get("content")
        if isinstance(content, str):
            text_parts.append(content)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str):
                        text_parts.append(text)
    return "".join(text_parts)


def stream_chat_completion(
    client: Any,
    *,
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    max_tokens: int,
) -> StreamingResult:
    started = perf_counter()
    first_token_at: float | None = None
    text_parts: list[str] = []
    usage: dict[str, Any] | None = None
    response_metadata: dict[str, Any] = {}

    params: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True,
    }
    try:
        params["stream_options"] = {"include_usage": True}
        stream = client.chat.completions.create(**params)
    except TypeError:
        params.pop("stream_options", None)
        stream = client.chat.completions.create(**params)

    for event in stream:
        event_dict = _to_dict(event)
        if first_token_at is None:
            choices = event_dict.get("choices")
            if isinstance(choices, list) and choices:
                first_token_at = perf_counter()

        delta_text = _extract_delta_text(event_dict)
        if delta_text:
            text_parts.append(delta_text)

        usage_payload = event_dict.get("usage")
        if isinstance(usage_payload, dict):
            usage = usage_payload

        for key, value in event_dict.items():
            if key not in {
                    "id",
                    "object",
                    "created",
                    "model",
                    "choices",
                    "usage",
            }:
                response_metadata[key] = value

    ended = perf_counter()
    ttft_ms = None if first_token_at is None else (first_token_at -
                                                   started) * 1000.0
    return StreamingResult(
        ttft_ms=ttft_ms,
        latency_ms=(ended - started) * 1000.0,
        text="".join(text_parts),
        usage=usage,
        response_metadata=response_metadata,
    )


def _iter_key_values(payload: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield key, value
            yield from _iter_key_values(value)
    elif isinstance(payload, list):
        for item in payload:
            yield from _iter_key_values(item)


def _to_fraction(value: Any) -> float | None:
    if not isinstance(value, (int, float)):
        return None
    number = float(value)
    if number < 0:
        return None
    if number <= 1:
        return number
    if number <= 100:
        return number / 100.0
    return None


def _extract_by_path(payload: Mapping[str, Any], path: str) -> Any:
    current: Any = payload
    for part in path.split("."):
        if not isinstance(current, Mapping):
            return None
        if part not in current:
            return None
        current = current[part]
    return current


def _metric_from_response_extensions(
    response_metadata: Mapping[str, Any] | None,
    response_field: str | None,
) -> KVReuseMetric | None:
    if not response_metadata:
        return None

    if response_field:
        value = _extract_by_path(response_metadata, response_field)
        value_fraction = _to_fraction(value)
        if value_fraction is not None:
            return KVReuseMetric(
                label="manual-prefix hit rate",
                method="response_extension",
                value=value_fraction,
                available=True,
                details={"field": response_field},
            )

    key_candidates = {
        "manual_prefix_hit_rate",
        "manual_kv_cache_hit_rate",
        "kv_cache_hit_rate",
        "prefix_hit_rate",
    }
    for key, value in _iter_key_values(response_metadata):
        if key.lower() in key_candidates:
            value_fraction = _to_fraction(value)
            if value_fraction is not None:
                return KVReuseMetric(
                    label="manual-prefix hit rate",
                    method="response_extension",
                    value=value_fraction,
                    available=True,
                    details={"field": key},
                )
    return None


def resolve_kv_reuse_metric(
    settings: Settings,
    *,
    manual_prefix: str,
    full_prompt: str,
    response_metadata: Mapping[str, Any] | None = None,
) -> KVReuseMetric:
    _ = (manual_prefix, full_prompt)
    response_metric = _metric_from_response_extensions(
        response_metadata=response_metadata,
        response_field=settings.kv_metric_response_field,
    )
    if response_metric is not None:
        return response_metric

    return KVReuseMetric(
        label="manual-prefix hit rate",
        method="not_available",
        value=None,
        available=False,
        details={
            "message":
            ("No response KV metric found. "
             "Set KV_METRIC_RESPONSE_FIELD or use latency-only comparison.")
        },
    )
