# serving-scenarios

Scenario-driven notebooks for validating long-context serving behavior on Tensormesh deployments using vLLM + LMCache.

## Purpose

This repository provides practical demos that send requests to a deployed Tensormesh endpoint and measure serving behavior in a reproducible way.

## Deploy a model on Tensormesh

1. Open the deployment page (staging example): `https://staging.app.tensormesh.ai/deployments/on-demand`
2. Deploy a model on the target GPU profile (for example, `openai/gpt-oss-120b` on 1x H200).
3. Collect the runtime credentials and endpoint details from the deployment:
   - `OPENAI_BASE_URL` (should include `/v1`, for example `https://external.nebius.tensormesh.ai/v1`)
   - `OPENAI_API_KEY` (Bearer token)
   - `TENSORMESH_USER_ID` (sent as `X-User-Id`)
   - `OPENAI_MODEL` (deployed model ID)

## Environment setup

1. Copy `.env.example` to `.env`.
2. Fill the four required values listed above.

Repository rule: all notebooks in this repo, including future notebooks, must read these runtime values directly from `.env`.

## Repository structure rules

1. `smoke_test.ipynb` must stay at the repository root as the quick endpoint liveness check.
2. All future development must be organized under `scenarios/` in numbered folders:
   - `scenarios/00_<name>/`
   - `scenarios/01_<name>/`
   - `scenarios/02_<name>/`
3. Each scenario folder must be self-contained and include all required assets for that scenario (notebooks, scripts, and supporting code).

## Smoke test notebook

- Interactive run:
  - `python3 -m notebook smoke_test.ipynb`
- Headless run:
  - `python3 -m nbconvert --to notebook --execute --inplace smoke_test.ipynb --ExecutePreprocessor.timeout=600`

## Runtime notes

- No local GPU is required.
- Local `vllm`/`lmcache` installs are not required.
- The notebook runs locally and calls a Tensormesh-hosted OpenAI-compatible endpoint.
