# SCENARIO_00: Token Sweep (Cold vs Cache Hit)

## 1. Objective

Demonstrate prefix-KV reuse behavior for long-document chat by sweeping prompt length and comparing:

- `cold`
- `cache_hit`

For each token length point, run exactly one `cold` request and one `cache_hit` request.

## 2. Scope

- In scope: remote serving behavior (TTFT/latency) vs prompt token length.
- Out of scope: local GPU performance and model quality benchmarking.

## 3. Required Inputs

From `.env` (required):

- `OPENAI_BASE_URL` (must include `/v1`)
- `OPENAI_API_KEY`
- `TENSORMESH_USER_ID`
- `OPENAI_MODEL`

Optional tuning:

- `REQUEST_TIMEOUT_S` (default `300`)
- `SCENARIO_TOKEN_TARGETS` (default `4000,8000,12000,16000,20000,24000,28000,32000,36000,40000`)
- `MAX_TOKENS` (default `64`)
- `TEMPERATURE` (default `0.0`)
- `MANUAL_SEED` (default `17`)
- `MANUAL_SECTIONS` (default `1200`)
- `TTFT_MIN_REDUCTION_FRACTION` (default `0.10`)
- `SCENARIO_ISOLATION_ID` (default auto-generated per execution)

Optional KV metric source:

- `KV_METRIC_RESPONSE_FIELD`

## 4. Scenario Design

For each token target:

1. Build an isolated long document up to target length.
2. Inject a run-specific marker across document content and `SESSION_PREFIX_HASH`.
3. Run one `cold` request.
4. Run one `cache_hit` request using the same document for that target.

Isolation rule:

- Point `i` must not reuse cache from any previous point `j < i`.

## 5. Procedure

1. Load settings from `.env`.
2. Iterate through token targets in ascending order.
3. Run one unmeasured warmup request before collecting results.
4. For each target, execute `cold -> cache_hit` once using the same question text.
5. Collect:
   - `ttft_ms` and `latency_ms` for both `cold` and `cache_hit`
   - prompt token counts
6. Build a token-sweep results table.
7. Plot:
   - TTFT vs prompt tokens (`cold` and `cache_hit`)
   - Latency vs prompt tokens (`cold` and `cache_hit`)
   - TTFT reduction (%) vs prompt tokens
8. Evaluate assertion on median TTFT reduction.

## 6. Success Criteria

Primary checks:

1. Median `TTFT(cache_hit) < TTFT(cold)`
2. Median TTFT reduction >= `TTFT_MIN_REDUCTION_FRACTION` (default 10%)

## 7. Outputs and Artifacts

- Per-target token sweep table (target tokens, axis tokens, cold/hit TTFT, cold/hit latency, deltas).
- Assertion summary (median cold/hit TTFT, reduction %, pass/fail).
- 3 charts:
  - TTFT vs tokens
  - Latency vs tokens
  - TTFT reduction vs tokens

## 8. Source of Truth

- Notebook: `scenarios/00_long_document_chat/scenario_00_long_document_chat.ipynb`
- Config: `scenarios/00_long_document_chat/src/config.py`
- Metrics: `scenarios/00_long_document_chat/src/utils/metrics.py`
- Reporting: `scenarios/00_long_document_chat/src/utils/reporting.py`

## 9. Execution

Interactive:

```bash
python3 -m jupyter notebook scenarios/00_long_document_chat/scenario_00_long_document_chat.ipynb
```

Headless:

```bash
python3 -m nbconvert --to notebook --execute --inplace scenarios/00_long_document_chat/scenario_00_long_document_chat.ipynb --ExecutePreprocessor.timeout=2400
```
