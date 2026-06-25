"""Static dependency ingestion for structural microservice coupling.

The current implementation ships with a deterministic mock parser for the
ShopFlow e-commerce platform. The parser shape mirrors a real static analysis
adapter so it can later be backed by AST parsing, import graph analysis, or
architecture metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class SourceDependency:
    """Represents a source-level dependency between two services."""

    source_service: str
    target_service: str
    dependency_count: int
    domain_affinity: float


@dataclass(frozen=True)
class StructuralCouplingReport:
    """Normalized structural coupling score for a service boundary."""

    source_service: str
    target_service: str
    dependency_count: int
    coupling_score: float
    domain_affinity: float


def load_mock_source_dependencies() -> list[SourceDependency]:
    """Return mock static dependency data for the ShopFlow platform."""

    return [
        SourceDependency("catalog", "pricing", 18, 0.86),
        SourceDependency("checkout", "payment", 32, 0.91),
        SourceDependency("checkout", "inventory", 21, 0.76),
        SourceDependency("orders", "shipping", 24, 0.88),
        SourceDependency("orders", "customer", 7, 0.44),
        SourceDependency("recommendations", "catalog", 9, 0.52),
        SourceDependency("support", "orders", 5, 0.38),
    ]


def parse_source_dependencies(
    dependencies: Iterable[SourceDependency] | None = None,
) -> list[StructuralCouplingReport]:
    """Convert source dependencies into normalized coupling reports.

    Args:
        dependencies: Optional dependency records. If omitted, mock ShopFlow
            dependency data is used.

    Returns:
        A list of normalized structural coupling reports.
    """

    dependency_list = list(dependencies or load_mock_source_dependencies())
    if not dependency_list:
        return []

    max_dependency_count = max(item.dependency_count for item in dependency_list)

    return [
        StructuralCouplingReport(
            source_service=item.source_service,
            target_service=item.target_service,
            dependency_count=item.dependency_count,
            coupling_score=round(item.dependency_count / max_dependency_count, 3),
            domain_affinity=item.domain_affinity,
        )
        for item in dependency_list
    ]
