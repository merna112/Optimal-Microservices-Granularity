"""Git authorship and team-boundary ingestion for organizational coupling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class GitContribution:
    """Represents ownership contribution for one service by one team."""

    service_name: str
    team_name: str
    commits: int


@dataclass(frozen=True)
class TeamBoundaryReport:
    """Organizational alignment metrics for a pair of services."""

    source_service: str
    target_service: str
    source_primary_team: str
    target_primary_team: str
    shared_team_ratio: float
    team_alignment_score: float


def load_mock_git_contributions() -> list[GitContribution]:
    """Return mock Git authorship data for ShopFlow services."""

    return [
        GitContribution("catalog", "merchandising", 145),
        GitContribution("catalog", "growth", 34),
        GitContribution("pricing", "merchandising", 118),
        GitContribution("pricing", "finance-platform", 22),
        GitContribution("checkout", "commerce-core", 164),
        GitContribution("payment", "commerce-core", 132),
        GitContribution("payment", "finance-platform", 51),
        GitContribution("inventory", "supply-chain", 126),
        GitContribution("inventory", "commerce-core", 49),
        GitContribution("orders", "fulfillment", 139),
        GitContribution("shipping", "fulfillment", 122),
        GitContribution("customer", "identity", 101),
        GitContribution("recommendations", "growth", 98),
        GitContribution("support", "customer-success", 77),
    ]


def analyze_team_boundaries(
    service_pairs: Iterable[tuple[str, str]],
    contributions: Iterable[GitContribution] | None = None,
) -> list[TeamBoundaryReport]:
    """Map service boundaries to authorship and team-alignment signals.

    Args:
        service_pairs: Service boundaries to analyze.
        contributions: Optional Git contribution records. If omitted, mock
            ShopFlow authorship data is used.

    Returns:
        A list of team-boundary reports.
    """

    contribution_list = list(contributions or load_mock_git_contributions())
    ownership = _build_ownership_index(contribution_list)

    reports: list[TeamBoundaryReport] = []
    for source_service, target_service in service_pairs:
        source_teams = ownership.get(source_service, {})
        target_teams = ownership.get(target_service, {})
        source_primary_team = _primary_team(source_teams)
        target_primary_team = _primary_team(target_teams)
        shared_team_ratio = _calculate_shared_team_ratio(source_teams, target_teams)

        reports.append(
            TeamBoundaryReport(
                source_service=source_service,
                target_service=target_service,
                source_primary_team=source_primary_team,
                target_primary_team=target_primary_team,
                shared_team_ratio=round(shared_team_ratio, 3),
                team_alignment_score=round(shared_team_ratio, 3),
            )
        )

    return reports


def _build_ownership_index(
    contributions: Iterable[GitContribution],
) -> dict[str, dict[str, int]]:
    """Build a service-to-team commit-count index."""

    ownership: dict[str, dict[str, int]] = {}
    for contribution in contributions:
        team_commits = ownership.setdefault(contribution.service_name, {})
        team_commits[contribution.team_name] = (
            team_commits.get(contribution.team_name, 0) + contribution.commits
        )

    return ownership


def _primary_team(team_commits: dict[str, int]) -> str:
    """Return the highest-contributing team for a service."""

    if not team_commits:
        return "unknown"

    return max(team_commits.items(), key=lambda item: item[1])[0]


def _calculate_shared_team_ratio(
    source_teams: dict[str, int],
    target_teams: dict[str, int],
) -> float:
    """Calculate ownership overlap between two services."""

    if not source_teams or not target_teams:
        return 0.0

    source_total = sum(source_teams.values())
    target_total = sum(target_teams.values())
    shared_ratio = 0.0

    for team_name in set(source_teams) & set(target_teams):
        source_ratio = source_teams[team_name] / source_total
        target_ratio = target_teams[team_name] / target_total
        shared_ratio += min(source_ratio, target_ratio)

    return min(shared_ratio, 1.0)
