"""Hybrid scoring engine for microservice granularity decisions."""

from __future__ import annotations

from dataclasses import dataclass

from ingestion.git_analyzer import TeamBoundaryReport
from ingestion.runtime_monitor import RuntimeCouplingReport
from ingestion.static_parser import StructuralCouplingReport


@dataclass(frozen=True)
class BoundaryScore:
    """Aggregated score for one candidate microservice boundary."""

    source_service: str
    target_service: str
    ddd_alignment_score: float
    technical_coupling_score: float
    team_autonomy_score: float
    relative_variation_index: float
    elasticity_score: float
    hybrid_score: float


class GranularityScoringEngine:
    """Computes hybrid GODF scores from structural, runtime, and team signals."""

    def compute_scores(
        self,
        structural_reports: list[StructuralCouplingReport],
        runtime_reports: list[RuntimeCouplingReport],
        team_reports: list[TeamBoundaryReport],
    ) -> list[BoundaryScore]:
        """Compute boundary scores by joining all available signal reports.

        Args:
            structural_reports: Static coupling reports.
            runtime_reports: Runtime coupling reports.
            team_reports: Organizational alignment reports.

        Returns:
            A list of hybrid boundary scores.
        """

        runtime_by_boundary = {
            self._boundary_key(report.source_service, report.target_service): report
            for report in runtime_reports
        }
        team_by_boundary = {
            self._boundary_key(report.source_service, report.target_service): report
            for report in team_reports
        }

        scores: list[BoundaryScore] = []
        for structural in structural_reports:
            boundary_key = self._boundary_key(
                structural.source_service,
                structural.target_service,
            )
            runtime = runtime_by_boundary.get(boundary_key)
            team = team_by_boundary.get(boundary_key)
            if runtime is None or team is None:
                continue

            ddd_alignment_score = structural.domain_affinity
            technical_coupling_score = self._calculate_technical_coupling(
                structural.coupling_score,
                runtime.runtime_coupling_score,
            )
            team_autonomy_score = 1.0 - team.team_alignment_score
            relative_variation_index = self._calculate_relative_variation_index(
                structural.coupling_score,
                runtime.runtime_coupling_score,
                team_autonomy_score,
            )
            elasticity_score = self._calculate_elasticity(
                runtime.p95_latency_ms,
                runtime.error_rate,
                runtime.call_frequency_per_minute,
            )
            hybrid_score = self._calculate_hybrid_score(
                ddd_alignment_score,
                technical_coupling_score,
                team_autonomy_score,
                relative_variation_index,
                elasticity_score,
            )

            scores.append(
                BoundaryScore(
                    source_service=structural.source_service,
                    target_service=structural.target_service,
                    ddd_alignment_score=round(ddd_alignment_score, 3),
                    technical_coupling_score=round(technical_coupling_score, 3),
                    team_autonomy_score=round(team_autonomy_score, 3),
                    relative_variation_index=round(relative_variation_index, 3),
                    elasticity_score=round(elasticity_score, 3),
                    hybrid_score=round(hybrid_score, 3),
                )
            )

        return scores

    @staticmethod
    def _boundary_key(source_service: str, target_service: str) -> tuple[str, str]:
        """Return a stable key for a directed service boundary."""

        return source_service, target_service

    @staticmethod
    def _calculate_technical_coupling(
        structural_coupling_score: float,
        runtime_coupling_score: float,
    ) -> float:
        """Blend structural and runtime coupling into one technical score."""

        return 0.45 * structural_coupling_score + 0.55 * runtime_coupling_score

    @staticmethod
    def _calculate_relative_variation_index(
        structural_coupling_score: float,
        runtime_coupling_score: float,
        team_autonomy_score: float,
    ) -> float:
        """Placeholder Relative Variation Index calculation.

        RVI approximates instability across signals. Higher values indicate
        greater disagreement between structure, runtime behavior, and team
        ownership.
        """

        mean_score = (
            structural_coupling_score + runtime_coupling_score + team_autonomy_score
        ) / 3
        if mean_score == 0:
            return 0.0

        absolute_deviation = (
            abs(structural_coupling_score - mean_score)
            + abs(runtime_coupling_score - mean_score)
            + abs(team_autonomy_score - mean_score)
        ) / 3

        return min(absolute_deviation / mean_score, 1.0)

    @staticmethod
    def _calculate_elasticity(
        p95_latency_ms: float,
        error_rate: float,
        call_frequency_per_minute: int,
    ) -> float:
        """Placeholder elasticity calculation for runtime adaptability.

        The score estimates how stressed a boundary is under load. Higher
        elasticity means the boundary is handling runtime pressure well.
        """

        latency_penalty = min(p95_latency_ms / 250.0, 1.0)
        error_penalty = min(error_rate / 0.05, 1.0)
        load_penalty = min(call_frequency_per_minute / 600.0, 1.0)
        stress_score = (
            0.45 * latency_penalty + 0.35 * error_penalty + 0.20 * load_penalty
        )

        return max(0.0, 1.0 - stress_score)

    @staticmethod
    def _calculate_hybrid_score(
        ddd_alignment_score: float,
        technical_coupling_score: float,
        team_autonomy_score: float,
        relative_variation_index: float,
        elasticity_score: float,
    ) -> float:
        """Calculate the final GODF boundary pressure score."""

        return (
            0.30 * technical_coupling_score
            + 0.25 * ddd_alignment_score
            + 0.20 * team_autonomy_score
            + 0.15 * relative_variation_index
            + 0.10 * (1.0 - elasticity_score)
        )
