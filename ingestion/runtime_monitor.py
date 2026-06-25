"""Runtime metrics ingestion for service-to-service communication."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RuntimeTrace:
    """Represents observed runtime communication between two services."""

    source_service: str
    target_service: str
    call_frequency_per_minute: int
    p95_latency_ms: float
    error_rate: float


@dataclass(frozen=True)
class RuntimeCouplingReport:
    """Normalized runtime coupling score for a service boundary."""

    source_service: str
    target_service: str
    call_frequency_per_minute: int
    p95_latency_ms: float
    error_rate: float
    runtime_coupling_score: float


def load_mock_runtime_traces() -> list[RuntimeTrace]:
    """Return mock Prometheus/Jaeger-like traces for ShopFlow."""

    return [
        RuntimeTrace("catalog", "pricing", 260, 42.0, 0.004),
        RuntimeTrace("checkout", "payment", 420, 115.0, 0.018),
        RuntimeTrace("checkout", "inventory", 330, 88.0, 0.012),
        RuntimeTrace("orders", "shipping", 300, 71.0, 0.009),
        RuntimeTrace("orders", "customer", 65, 39.0, 0.006),
        RuntimeTrace("recommendations", "catalog", 190, 54.0, 0.005),
        RuntimeTrace("support", "orders", 45, 62.0, 0.011),
    ]


def parse_runtime_metrics(
    traces: Iterable[RuntimeTrace] | None = None,
) -> list[RuntimeCouplingReport]:
    """Normalize runtime traces into boundary-level coupling reports.

    Args:
        traces: Optional runtime trace records. If omitted, mock ShopFlow trace
            data is used.

    Returns:
        A list of runtime coupling reports.
    """

    trace_list = list(traces or load_mock_runtime_traces())
    if not trace_list:
        return []

    max_frequency = max(trace.call_frequency_per_minute for trace in trace_list)
    max_latency = max(trace.p95_latency_ms for trace in trace_list)
    max_error_rate = max(trace.error_rate for trace in trace_list)

    reports: list[RuntimeCouplingReport] = []
    for trace in trace_list:
        frequency_score = trace.call_frequency_per_minute / max_frequency
        latency_score = trace.p95_latency_ms / max_latency
        error_score = trace.error_rate / max_error_rate if max_error_rate else 0.0
        runtime_score = (
            0.55 * frequency_score
            + 0.30 * latency_score
            + 0.15 * error_score
        )

        reports.append(
            RuntimeCouplingReport(
                source_service=trace.source_service,
                target_service=trace.target_service,
                call_frequency_per_minute=trace.call_frequency_per_minute,
                p95_latency_ms=trace.p95_latency_ms,
                error_rate=trace.error_rate,
                runtime_coupling_score=round(runtime_score, 3),
            )
        )

    return reports
