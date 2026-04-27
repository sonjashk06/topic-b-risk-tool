# Control Recommendation Module


def _total_reduction(control: dict) -> int:
    return control["likelihood_reduction"] + control["impact_reduction"]


def recommend_controls(
    scenario: dict,
    residual_likelihood: int,
    residual_impact: int,
    asset_threshold: int,
    controls_by_id: dict,
) -> dict:
    residual_risk = residual_likelihood * residual_impact

    # Nothing to do if already within threshold
    if residual_risk <= asset_threshold:
        return {
            "recommended_controls": [],
            "projected_risk_after_recommendation": residual_risk,
            "treatment_result": "already_acceptable",
        }

    threat = scenario["threat"]
    deployed_ids = set(scenario.get("deployed_controls", []))

    # Applicable controls that are not yet deployed for this scenario
    candidates = [
        ctrl
        for ctrl in controls_by_id.values()
        if threat in ctrl.get("applicable_threats", [])
        and ctrl["id"] not in deployed_ids
    ]

    # Greedy: highest total reduction first
    candidates.sort(key=_total_reduction, reverse=True)

    proj_likelihood = residual_likelihood
    proj_impact = residual_impact
    recommended_names = []

    for ctrl in candidates:
        proj_likelihood = max(1, proj_likelihood - ctrl["likelihood_reduction"])
        proj_impact = max(1, proj_impact - ctrl["impact_reduction"])
        recommended_names.append(ctrl["name"])

        if proj_likelihood * proj_impact <= asset_threshold:
            break

    projected_risk = proj_likelihood * proj_impact
    treatment_result = "threshold_met" if projected_risk <= asset_threshold else "threshold_not_met"

    return {
        "recommended_controls": recommended_names,
        "projected_risk_after_recommendation": projected_risk,
        "treatment_result": treatment_result,
    }
