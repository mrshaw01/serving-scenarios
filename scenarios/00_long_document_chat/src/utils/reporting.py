from __future__ import annotations

import math
from statistics import median
from typing import Any


def print_token_sweep_table(points: list[dict[str, Any]]) -> None:
    if not points:
        print("No token sweep results available.")
        return

    ordered = sorted(points, key=lambda row: float(row["token_axis"]))
    print(
        "Token sweep results\n"
        "target_tok  axis_tok   ttft_cold  ttft_hit  lat_cold  lat_hit  ttft_delta%  lat_delta%"
    )
    for row in ordered:
        print(f"{int(row['token_target']):>10d} "
              f"{int(row['token_axis']):>9d} "
              f"{float(row['ttft_cold_ms']):>10.1f} "
              f"{float(row['ttft_cache_hit_ms']):>9.1f} "
              f"{float(row['latency_cold_ms']):>9.1f} "
              f"{float(row['latency_cache_hit_ms']):>8.1f} "
              f"{float(row['ttft_reduction_fraction']) * 100:>11.2f} "
              f"{float(row['latency_reduction_fraction']) * 100:>10.2f}")


def summarize_assertions(
    points: list[dict[str, Any]],
    *,
    min_reduction_fraction: float = 0.10,
) -> dict[str, Any]:
    if not points:
        return {
            "median_cold_ttft_ms": None,
            "median_cache_hit_ttft_ms": None,
            "ttft_reduction_fraction": None,
            "min_reduction_fraction": min_reduction_fraction,
            "passed": None,
            "points_passed": 0,
            "points_total": 0,
        }

    cold_ttft = [float(row["ttft_cold_ms"]) for row in points]
    hit_ttft = [float(row["ttft_cache_hit_ms"]) for row in points]
    median_cold = median(cold_ttft)
    median_hit = median(hit_ttft)
    reduction = None
    if median_cold > 0:
        reduction = 1.0 - (median_hit / median_cold)

    points_passed = 0
    for row in points:
        if (float(row["ttft_cache_hit_ms"]) < float(row["ttft_cold_ms"])
                and float(
                    row["ttft_reduction_fraction"]) >= min_reduction_fraction):
            points_passed += 1

    passed = (reduction is not None and reduction >= min_reduction_fraction
              and points_passed >= math.ceil(len(points) * 0.6))

    return {
        "median_cold_ttft_ms": median_cold,
        "median_cache_hit_ttft_ms": median_hit,
        "ttft_reduction_fraction": reduction,
        "min_reduction_fraction": min_reduction_fraction,
        "passed": passed,
        "points_passed": points_passed,
        "points_total": len(points),
    }


def _require_pyplot():
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        raise RuntimeError(
            "matplotlib is required for Scenario 00 plotting.") from exc
    return plt


def plot_token_sweep(points: list[dict[str, Any]]) -> None:
    if not points:
        raise ValueError("No token sweep points available to plot.")
    plt = _require_pyplot()
    ordered = sorted(points, key=lambda row: float(row["token_axis"]))

    x_values = [float(row["token_axis"]) for row in ordered]
    ttft_cold = [float(row["ttft_cold_ms"]) for row in ordered]
    ttft_hit = [float(row["ttft_cache_hit_ms"]) for row in ordered]
    latency_cold = [float(row["latency_cold_ms"]) for row in ordered]
    latency_hit = [float(row["latency_cache_hit_ms"]) for row in ordered]
    ttft_reduction_pct = [
        float(row["ttft_reduction_fraction"]) * 100.0 for row in ordered
    ]

    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    axes[0].plot(x_values, ttft_cold, marker="o", label="cold")
    axes[0].plot(x_values, ttft_hit, marker="o", label="cache_hit")
    axes[0].set_ylabel("TTFT (ms)")
    axes[0].set_title("TTFT vs Prompt Tokens")
    axes[0].grid(axis="both", linestyle="--", alpha=0.3)
    axes[0].legend()

    axes[1].plot(x_values, latency_cold, marker="o", label="cold")
    axes[1].plot(x_values, latency_hit, marker="o", label="cache_hit")
    axes[1].set_ylabel("Latency (ms)")
    axes[1].set_title("Latency vs Prompt Tokens")
    axes[1].grid(axis="both", linestyle="--", alpha=0.3)
    axes[1].legend()

    axes[2].plot(x_values, ttft_reduction_pct, marker="o", color="#4f9d69")
    axes[2].axhline(0.0, color="black", linewidth=1)
    axes[2].set_ylabel("TTFT reduction (%)")
    axes[2].set_xlabel("Prompt tokens (axis)")
    axes[2].set_title("TTFT Reduction vs Prompt Tokens")
    axes[2].grid(axis="both", linestyle="--", alpha=0.3)

    fig.tight_layout()
    plt.show()
