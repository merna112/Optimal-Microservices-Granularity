"""Decision optimizer for service-boundary recommendations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from scoring.engine import BoundaryScore


class Recommendation(str, Enum):
    """Supported architectural boundary recommendations."""

    SPLIT = "SPLIT"
    MERGE = "MERGE"
    MAINTAIN = "MAINTAIN"


@dataclass(frozen=True)
class ArchitecturalRecommendation:
    """Formal recommendation for one service boundary."""

    source_service: str
    target_service: str
    recommendation: Recommendation
    confidence: float
    rationale: str
    score: BoundaryScore


class GranularityDecisionAnalyzer:
    """Runs the optimization loop and emits architecture recommendations."""

    def analyze(
        self,
        boundary_scores: list[BoundaryScore],
    ) -> list[ArchitecturalRecommendation]:
        """Convert GODF scores into SPLIT, MERGE, or MAINTAIN decisions.

        Args:
            boundary_scores: Aggregated boundary scores from the scoring engine.

        Returns:
            Ranked architectural recommendations.
        """

        recommendations = [
            self._recommend_for_boundary(score) for score in boundary_scores
        ]
        return sorted(
            recommendations,
            key=lambda item: item.confidence,
            reverse=True,
        )

    def _recommend_for_boundary(
        self,
        score: BoundaryScore,
    ) -> ArchitecturalRecommendation:
        """Create a recommendation from one boundary score."""

        if self._should_merge(score):
            recommendation = Recommendation.MERGE
            rationale = (
                "High domain alignment, high technical coupling, and overlapping "
                "ownership suggest the services behave as one capability."
            )
        elif self._should_split(score):
            recommendation = Recommendation.SPLIT
            rationale = (
                "Signal variation and low domain/team alignment suggest the "
                "boundary should be decomposed or reassigned."
            )
        else:
            recommendation = Recommendation.MAINTAIN
            rationale = (
                "Signals are within acceptable operating thresholds for the "
                "current boundary."
            )

        return ArchitecturalRecommendation(
            source_service=score.source_service,
            target_service=score.target_service,
            recommendation=recommendation,
            confidence=self._calculate_confidence(score, recommendation),
            rationale=rationale,
            score=score,
        )

    @staticmethod
    def _should_merge(score: BoundaryScore) -> bool:
        """Return whether two services are strong merge candidates."""

        return (
            score.ddd_alignment_score >= 0.80
            and score.technical_coupling_score >= 0.65
            and score.team_autonomy_score <= 0.35
        )

    @staticmethod
    def _should_split(score: BoundaryScore) -> bool:
        """Return whether a service boundary is a split candidate."""

        return (
            score.relative_variation_index >= 0.38
            and score.ddd_alignment_score <= 0.60
        ) or (
            score.hybrid_score >= 0.72
            and score.elasticity_score <= 0.50
        )

    @staticmethod
    def _calculate_confidence(
        score: BoundaryScore,
        recommendation: Recommendation,
    ) -> float:
        """Estimate confidence for a generated recommendation."""

        if recommendation == Recommendation.MERGE:
            confidence = (
                0.40 * score.ddd_alignment_score
                + 0.40 * score.technical_coupling_score
                + 0.20 * (1.0 - score.team_autonomy_score)
            )
        elif recommendation == Recommendation.SPLIT:
            confidence = (
                0.45 * score.relative_variation_index
                + 0.30 * (1.0 - score.ddd_alignment_score)
                + 0.25 * score.team_autonomy_score
            )
        else:
            confidence = 1.0 - abs(score.hybrid_score - 0.50)

        return round(max(0.0, min(confidence, 1.0)), 3)
