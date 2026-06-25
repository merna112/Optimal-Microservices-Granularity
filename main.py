"""Granulify CLI simulation entrypoint."""

from __future__ import annotations

from decision.analyzer import GranularityDecisionAnalyzer
from ingestion.git_analyzer import analyze_team_boundaries
from ingestion.runtime_monitor import parse_runtime_metrics
from ingestion.static_parser import parse_source_dependencies
from scoring.engine import GranularityScoringEngine


def run_shopflow_simulation() -> None:
    """Run the built-in ShopFlow granularity optimization simulation."""

    structural_reports = parse_source_dependencies()
    runtime_reports = parse_runtime_metrics()
    service_pairs = [
        (report.source_service, report.target_service)
        for report in structural_reports
    ]
    team_reports = analyze_team_boundaries(service_pairs)

    scoring_engine = GranularityScoringEngine()
    boundary_scores = scoring_engine.compute_scores(
        structural_reports=structural_reports,
        runtime_reports=runtime_reports,
        team_reports=team_reports,
    )

    decision_analyzer = GranularityDecisionAnalyzer()
    recommendations = decision_analyzer.analyze(boundary_scores)

    print("Granulify - Granularity Optimization Decision Framework")
    print("Simulation: ShopFlow e-commerce platform")
    print("=" * 68)

    for item in recommendations:
        score = item.score
        boundary_name = f"{item.source_service} -> {item.target_service}"
        print(f"\nBoundary: {boundary_name}")
        print(f"Recommendation: {item.recommendation.value}")
        print(f"Confidence: {item.confidence:.3f}")
        print(
            "Scores: "
            f"DDD={score.ddd_alignment_score:.3f}, "
            f"Technical={score.technical_coupling_score:.3f}, "
            f"TeamAutonomy={score.team_autonomy_score:.3f}, "
            f"RVI={score.relative_variation_index:.3f}, "
            f"Elasticity={score.elasticity_score:.3f}, "
            f"Hybrid={score.hybrid_score:.3f}"
        )
        print(f"Rationale: {item.rationale}")


if __name__ == "__main__":
    run_shopflow_simulation()
