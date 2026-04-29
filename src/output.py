def sort_and_prioritize(valid_results: list) -> list:
    """
    Sorts scenarios such that:
    - not_acceptable ones come first
    - higher residual risk comes before lower residual risk
    - each scenario gets a priority number (1 = most urgent)
    """

    def sort_key(s):
        # not_acceptable = 0, acceptable = 1 → not_acceptable sorts first
        acceptability_rank = 0 if s.get("status") == "not_acceptable" else 1
        # negate so higher risk sorts first
        residual_risk = -s.get("residual_risk", 0)
        return (acceptability_rank, residual_risk)

    sorted_results = sorted(valid_results, key=sort_key)

    # assign priority based on position (1 = most urgent)
    for rank, scenario in enumerate(sorted_results, start=1):
        scenario["priority"] = rank

    return sorted_results


def compute_summary(all_scenarios: list) -> dict:
    """
    Builds a summary of the analysis.

    Fix: total_scenarios now counts ALL scenarios (including invalid),
    matching the spec example where total = 7 even with invalid entries.
    """

    total = len(all_scenarios)  # all scenarios, not just valid ones

    acceptable_count = sum(
        1 for s in all_scenarios if s.get("status") == "acceptable"
    )
    not_acceptable_count = sum(
        1 for s in all_scenarios if s.get("status") == "not_acceptable"
    )

    # highest residual risk only among valid scenarios (invalid have None)
    valid_risks = [
        s["residual_risk"]
        for s in all_scenarios
        if s.get("residual_risk") is not None
    ]
    highest = max(valid_risks) if valid_risks else 0

    return {
        "total_scenarios": total,
        "acceptable_scenarios": acceptable_count,
        "not_acceptable_scenarios": not_acceptable_count,
        "highest_residual_risk": highest,
    }


def build_output(scenario_results: list) -> dict:
    """
    Builds the final output.
    Separates valid and invalid scenarios.
    Sorts valid ones by priority.
    Appends invalid ones at the end (no priority assigned).
    Computes summary over all scenarios.
    """

    valid_scenarios = []
    invalid_scenarios = []

    for s in scenario_results:
        if s.get("status") == "invalid":
            invalid_scenarios.append(s)
        else:
            valid_scenarios.append(s)

    # sort only valid scenarios (invalid ones stay at the end)
    sorted_valid = sort_and_prioritize(valid_scenarios)

    # invalid scenarios get no priority
    for s in invalid_scenarios:
        s["priority"] = None

    all_scenarios = sorted_valid + invalid_scenarios

    # summary is computed over everything
    summary = compute_summary(all_scenarios)

    return {
        "summary": summary,
        "risk_results": all_scenarios,
    }