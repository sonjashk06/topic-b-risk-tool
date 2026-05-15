from src.risk import compute_residual_risk

def recommend_controls(
    scenario: dict,
    asset_threshold: int,
    controls_by_id: dict,
    ) -> dict:
    """
    If the current risk is too high, try to fix it by adding controls.
    - take controls that match the threat
    - sort them from most useful to least useful
    - add them one by one until the risk is acceptable
    """

    # start from the original values
    original_likelihood = scenario["likelihood"]
    original_impact = scenario["impact"]

    # controls already deployed in this scenario
    already_deployed_control_ids = set(scenario.get("deployed_controls", []))
    active_controls = [
        controls_by_id[cid]
        for cid in scenario.get("deployed_controls", [])
        if cid in controls_by_id
    ]

    #Compute the current residual risk after deployed controls
    current_residual_risk = compute_residual_risk(
        original_likelihood, original_impact, active_controls
    )

    # if the risk is already acceptable, no need to recommend anything
    if current_residual_risk <= asset_threshold:
        return {
            "recommended_controls": [],
            "projected_risk_after_recommendation": current_residual_risk,
            "treatment_result": "already_acceptable",
        }

    threat_type = scenario["threat"]

    # Select controls that:
    # -apply to this threat
    # -are not already deployed
    candidate_controls = [
        control
        for control in controls_by_id.values()
        if threat_type in control.get("applicable_threats", [])
        and control["id"] not in already_deployed_control_ids
    ]

    # sort controls from most effective to least effective
    candidate_controls.sort(
        key=lambda c: c["likelihood_reduction"] + c["impact_reduction"],
        reverse=True,
    )

    recommended_control_names = []
    updated_risk = current_residual_risk

    #add controls one by one
    for control in candidate_controls:
        active_controls.append(control)
        recommended_control_names.append(control["name"])

        # recompute the risk with all controls applied so far
        updated_risk = compute_residual_risk(
            original_likelihood, original_impact, active_controls
        )

        # as soon as the risk becomes acceptable, we stop
        if updated_risk <= asset_threshold:
            break

    return {
        "recommended_controls": recommended_control_names,
        "projected_risk_after_recommendation": updated_risk,
        "treatment_result": (
            "threshold_met" if updated_risk <= asset_threshold else "threshold_not_met"
        ),
    }