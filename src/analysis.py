from src.risk import compute_initial_risk, compute_residual_risk
from src.controls import recommend_controls


def analyze_scenario(s, assets_by_id, controls_by_id):
    """
    Analyze one scenario step by step:
    - find the asset
    - compute risk
    - check if it's acceptable
    - suggest fixes if needed
    """

    # find the asset linked to this scenario
    asset = assets_by_id.get(s["asset_id"])

    # if the asset doesn't exist, we cannot analyse that scenario
    if not asset:
        return {
            "scenario_id": s["id"],
            "asset_id": s["asset_id"],
            "asset_name": None,
            "threat": s["threat"],
            "exposure": s["exposure"],
            "initial_risk": None,
            "deployed_controls": [],
            "residual_risk": None,
            "acceptable_threshold": None,
            "status": "invalid",
            "recommended_controls": [],
            "projected_risk_after_recommendation": None,
            "treatment_result": "invalid_scenario",
            "priority": None,
        }

    # get the list of control IDs already applied
    deployed_ids = s.get("deployed_controls", [])
    deployed_controls = [
        controls_by_id[c] for c in deployed_ids if c in controls_by_id
    ]

    # track unknown control references to report them
    unknown_controls = [c for c in deployed_ids if c not in controls_by_id]

    # basic risk before applying any controls
    initial_risk = compute_initial_risk(s["likelihood"], s["impact"])

    # risk after applying the deployed controls
    rl, ri, residual_risk = compute_residual_risk(
        s["likelihood"], s["impact"], deployed_controls
    )

    # each asset defines how much risk is acceptable
    threshold = asset["risk_threshold"]

    if residual_risk <= threshold:
        status = "acceptable"
        recommendation = {
            "recommended_controls": [],
            "projected_risk_after_recommendation": residual_risk,
            "treatment_result": "already_acceptable",
        }
    else:
        status = "not_acceptable"
        # updated call: removed the dead rl, ri arguments
        recommendation = recommend_controls(s, threshold, controls_by_id)

    # final result for this scenario
    result = {
        "scenario_id": s["id"],
        "asset_id": asset["id"],
        "asset_name": asset["name"],
        "threat": s["threat"],
        "exposure": s["exposure"],
        "initial_risk": initial_risk,
        "deployed_controls": [c["name"] for c in deployed_controls],
        "residual_risk": residual_risk,
        "acceptable_threshold": threshold,
        "status": status,
        **recommendation,
    }

    # include unknown controls if there are any
    if unknown_controls:
        result["invalid_references"] = unknown_controls

    return result


def analyze_all(assets_by_id, controls_by_id, scenarios):
    """
    Run the analysis for all scenarios in the file.
    """
    return [
        analyze_scenario(s, assets_by_id, controls_by_id) for s in scenarios
    ]