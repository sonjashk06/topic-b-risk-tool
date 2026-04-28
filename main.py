import argparse
import json
from pathlib import Path

from output import build_output
from src.Risk_controls import compute_risk 
from Risk_controls import recommend_controls
from src.risk import analyze_risks
from src.loader import load_json 

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input directory")
    parser.add_argument("--output", required=True, help="Output JSON file")
    return parser.parse_args()


def main():
    args = parse_args()
    input_dir = Path(args.input)

    assets = load_json(input_dir / "assets.json")
    controls = load_json(input_dir / "security_controls.json")
    scenarios = load_json(input_dir / "scenarios.json")

    #risk results:
    result = analyze_risks(
        assets,
        scenarios,
        controls
    )
    from loader import load_json, build_asset_dict, build_control_dict, extract_scenarios

    assets_by_id   = build_asset_dict(assets)
    controls_by_id = build_control_dict(controls)
    scenarios_list = extract_scenarios(scenarios)
    scenario_results = []

    for scenario in scenarios_list:
        asset_id = scenario.get("asset_id")
        asset = assets_by_id.get(asset_id)

        result = compute_risk(scenario, asset, controls_by_id) 

        if result.get("status") == "not_acceptable": 
            recommendation = recommend_controls(
            scenario,
            result["residual_likelihood"],
            result["residual_impact"],
            result["acceptable_threshold"],
            controls_by_id,
        )
            
        result.update(recommendation)
        scenario_results.append(result)
    
    final_output = build_output(scenario_results)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        ordered_output = {
            "summary": final_output["summary"],
            "risk_results": [
                {
                    "scenario_id":                       s.get("scenario_id"),
                    "asset_id":                          s.get("asset_id"),
                    "asset_name":                        s.get("asset_name"),
                    "threat":                            s.get("threat"),
                    "exposure":                          s.get("exposure"),
                    "initial_risk":                      s.get("initial_risk"),
                    "deployed_controls":                 s.get("deployed_controls"),
                    "residual_risk":                     s.get("residual_risk"),
                    "acceptable_threshold":              s.get("acceptable_threshold"),
                    "status":                            s.get("status"),
                    "recommended_controls":              s.get("recommended_controls"),
                    "projected_risk_after_recommendation": s.get("projected_risk_after_recommendation"),
                    "treatment_result":                  s.get("treatment_result"),
                    "priority":                          s.get("priority"),
                }
                for s in final_output["risk_results"]
            ]
        }
        json.dump(ordered_output, f, indent=2)



if __name__ == "__main__":
    main()
