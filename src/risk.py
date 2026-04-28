from typing import Any, Dict, List, Tuple


Asset = Dict[str, Any]
Scenario = Dict[str, Any]
Control = Dict[str, Any]
RiskResult = Dict[str, Any]


def unwrap_list(data: Any, key: str) -> List[Dict[str, Any]]:
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        return data.get(key, [])

    return []


def normalize_inputs(
    assets_data: Any,
    scenarios_data: Any,
    controls_data: Any
) -> Tuple[List[Asset], List[Scenario], List[Control]]:
    assets = unwrap_list(assets_data, "assets")
    scenarios = unwrap_list(scenarios_data, "scenarios")

    if isinstance(controls_data, dict):
        controls = controls_data.get("security_controls", controls_data.get("controls", []))
    else:
        controls = controls_data

    return assets, scenarios, controls


def index_by_id(items: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {
        item["id"]: item
        for item in items
        if "id" in item
    }


def control_reduction(control: Control) -> int:
    return control.get("likelihood_reduction", 0) + control.get("impact_reduction", 0)


def control_names(controls: List[Control]) -> List[str]:
    return [control.get("name", control.get("id")) for control in controls]


def calculate_risk(likelihood: int, impact: int, controls: List[Control]) -> RiskResult:
    likelihood_reduction = sum(c.get("likelihood_reduction", 0) for c in controls)
    impact_reduction = sum(c.get("impact_reduction", 0) for c in controls)

    residual_likelihood = max(1, likelihood - likelihood_reduction)
    residual_impact = max(1, impact - impact_reduction)
    residual_risk = residual_likelihood * residual_impact

    return {
        "likelihood_reduction": likelihood_reduction,
        "impact_reduction": impact_reduction,
        "residual_likelihood": residual_likelihood,
        "residual_impact": residual_impact,
        "residual_risk": residual_risk
    }


def resolve_controls(
    deployed_control_ids: List[str],
    controls_by_id: Dict[str, Control]
) -> Tuple[List[Control], List[str]]:
    valid_controls = []
    unknown_controls = []

    for control_id in deployed_control_ids:
        control = controls_by_id.get(control_id)

        if control is None:
            unknown_controls.append(control_id)
        else:
            valid_controls.append(control)

    return valid_controls, unknown_controls


def get_candidate_controls(
    scenario: Scenario,
    all_controls: List[Control],
    deployed_control_ids: List[str]
) -> List[Control]:
    threat = scenario.get("threat")
    deployed_set = set(deployed_control_ids)

    candidates = [
        control
        for control in all_controls
        if control.get("id") not in deployed_set
        and threat in control.get("applicable_threats", [])
    ]

    candidates.sort(key=control_reduction, reverse=True)

    return candidates


def recommend_controls(
    scenario: Scenario,
    all_controls: List[Control],
    deployed_control_ids: List[str],
    already_applied_controls: List[Control],
    risk_threshold: int
) -> RiskResult:
    likelihood = scenario["likelihood"]
    impact = scenario["impact"]

    projected_controls = list(already_applied_controls)
    recommended_controls = []

    projected = calculate_risk(likelihood, impact, projected_controls)

    for control in get_candidate_controls(scenario, all_controls, deployed_control_ids):
        if projected["residual_risk"] <= risk_threshold:
            break

        recommended_controls.append(control)
        projected_controls.append(control)
        projected = calculate_risk(likelihood, impact, projected_controls)

    if projected["residual_risk"] <= risk_threshold:
        treatment_result = "threshold_met"
    else:
        treatment_result = "threshold_not_met"

    return {
        "recommended_controls": control_names(recommended_controls),
        "projected_risk_after_recommendation": projected["residual_risk"],
        "treatment_result": treatment_result
    }


def analyze_scenario(
    scenario: Scenario,
    assets_by_id: Dict[str, Asset],
    controls_by_id: Dict[str, Control],
    all_controls: List[Control]
) -> RiskResult:
    scenario_id = scenario.get("id")
    asset_id = scenario.get("asset_id")
    asset = assets_by_id.get(asset_id)

    deployed_control_ids = scenario.get("deployed_controls", [])
    deployed_controls, unknown_controls = resolve_controls(deployed_control_ids, controls_by_id)

    if asset is None:
        return {
            "scenario_id": scenario_id,
            "asset_id": asset_id,
            "asset_name": None,
            "threat": scenario.get("threat"),
            "exposure": scenario.get("exposure"),
            "initial_risk": None,
            "deployed_controls": control_names(deployed_controls),
            "residual_risk": None,
            "acceptable_threshold": None,
            "status": "invalid",
            "recommended_controls": [],
            "projected_risk_after_recommendation": None,
            "treatment_result": "invalid_scenario",
            "priority": None,
            "invalid_references": {
                "unknown_asset": asset_id,
                "unknown_controls": unknown_controls
            }
        }

    likelihood = scenario["likelihood"]
    impact = scenario["impact"]
    threshold = asset["risk_threshold"]

    initial_risk = likelihood * impact
    residual = calculate_risk(likelihood, impact, deployed_controls)
    residual_risk = residual["residual_risk"]

    if residual_risk <= threshold:
        status = "acceptable"
        treatment = {
            "recommended_controls": [],
            "projected_risk_after_recommendation": residual_risk,
            "treatment_result": "already_acceptable"
        }
    else:
        status = "not_acceptable"
        treatment = recommend_controls(
            scenario=scenario,
            all_controls=all_controls,
            deployed_control_ids=deployed_control_ids,
            already_applied_controls=deployed_controls,
            risk_threshold=threshold
        )

    result = {
        "scenario_id": scenario_id,
        "asset_id": asset_id,
        "asset_name": asset.get("name"),
        "threat": scenario.get("threat"),
        "exposure": scenario.get("exposure"),
        "initial_risk": initial_risk,
        "deployed_controls": control_names(deployed_controls),
        "residual_risk": residual_risk,
        "acceptable_threshold": threshold,
        "status": status,
        "recommended_controls": treatment["recommended_controls"],
        "projected_risk_after_recommendation": treatment["projected_risk_after_recommendation"],
        "treatment_result": treatment["treatment_result"],
        "priority": None
    }

    if unknown_controls:
        result["invalid_references"] = {
            "unknown_asset": None,
            "unknown_controls": unknown_controls
        }

    return result


def sort_and_prioritize(results: List[RiskResult]) -> List[RiskResult]:
    valid = [r for r in results if r.get("status") != "invalid"]
    invalid = [r for r in results if r.get("status") == "invalid"]

    valid.sort(
        key=lambda r: (
            r["status"] == "acceptable",
            -r["residual_risk"]
        )
    )

    for priority, result in enumerate(valid, start=1):
        result["priority"] = priority

    return valid + invalid


def build_summary(results: List[RiskResult]) -> Dict[str, Any]:
    valid = [r for r in results if r.get("status") != "invalid"]
    acceptable = [r for r in valid if r.get("status") == "acceptable"]
    not_acceptable = [r for r in valid if r.get("status") == "not_acceptable"]

    residual_risks = [
        r["residual_risk"]
        for r in valid
        if r.get("residual_risk") is not None
    ]

    highest_residual_risk = max(residual_risks) if residual_risks else None

    return {
        "total_scenarios": len(results),
        "acceptable_scenarios": len(acceptable),
        "not_acceptable_scenarios": len(not_acceptable),
        "highest_residual_risk": highest_residual_risk
    }


def analyze_risks(
    assets_data: Any,
    scenarios_data: Any,
    controls_data: Any
) -> Dict[str, Any]:
    assets, scenarios, controls = normalize_inputs(
        assets_data,
        scenarios_data,
        controls_data
    )

    assets_by_id = index_by_id(assets)
    controls_by_id = index_by_id(controls)

    results = [
        analyze_scenario(scenario, assets_by_id, controls_by_id, controls)
        for scenario in scenarios
    ]

    results = sort_and_prioritize(results)

    return {
        "summary": build_summary(results),
        "risk_results": results
    }
