# Scenario 00 - Token Sweep (`cold` vs `cache_hit`)

This scenario demonstrates a token-length sweep for long-document chat.

- For each token target, run exactly one `cold` then one `cache_hit`.

Expected behavior: `cache_hit` TTFT should stay below `cold` TTFT across increasing token sizes, with overall median improvement above the configured threshold.

## Files

- `scenario_00_long_document_chat.ipynb`: scenario notebook.
- `src/config.py`: environment loading and client setup.
- `src/utils/metrics.py`: streaming timing capture.
- `src/utils/reporting.py`: token-sweep table, assertion summary, and required plots.

## Required env vars

- `OPENAI_BASE_URL`
- `OPENAI_API_KEY`
- `TENSORMESH_USER_ID`
- `OPENAI_MODEL`

## Optional tuning env vars

- `SCENARIO_TOKEN_TARGETS` (default `4000,8000,12000,16000,20000,24000,28000,32000,36000,40000`)
- `MANUAL_SECTIONS` (default `1200`)
- `MAX_TOKENS` (default `64`)
- `TEMPERATURE` (default `0.0`)
- `TTFT_MIN_REDUCTION_FRACTION` (default `0.10`)
- `SCENARIO_ISOLATION_ID` (default auto-generated per execution)

The notebook injects unique run markers derived from `SCENARIO_ISOLATION_ID` across each document, so point `i` does not reuse cache from point `j < i`.
An unmeasured warmup request runs before the sweep, and measured `cold`/`cache_hit` use the same question for fair comparison.

## Run

From repo root:

```bash
python3 -m jupyter notebook scenarios/00_long_document_chat/scenario_00_long_document_chat.ipynb
```

Headless:

```bash
python3 -m nbconvert --to notebook --execute --inplace scenarios/00_long_document_chat/scenario_00_long_document_chat.ipynb --ExecutePreprocessor.timeout=1800
```
