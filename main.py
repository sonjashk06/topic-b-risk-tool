import argparse
import json
from pathlib import Path

<<<<<<< HEAD
from src.analysis import analyze_all
from src.output import build_output
from src.loader import load_json, build_asset_dict, build_control_dict, extract_scenarios
=======
from src.risk import analyze_risks
from src.loader import load_json
>>>>>>> 4498b2444c855c010b59620d8d9a83d26dc188e0

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input directory")
    parser.add_argument("--output", required=True, help="Output JSON file")
    return parser.parse_args()

def main():
    args = parse_args()
    input_dir = Path(args.input)

<<<<<<< HEAD
    #Load all input files
    assets = load_json(input_dir / "assets.json")
    controls = load_json(input_dir / "security_controls.json")
    scenarios = load_json(input_dir / "scenarios.json")

    assets_by_id = build_asset_dict(assets)
    controls_by_id = build_control_dict(controls)
    scenarios_list = extract_scenarios(scenarios)

    #Risk analysis on all scenarios
    results = analyze_all(assets_by_id, controls_by_id, scenarios_list)

    #Formatting and computing the summary
    final_output = build_output(results)
=======
    assets   = load_json(input_dir / "assets.json")
    controls = load_json(input_dir / "security_controls.json")
    scenarios = load_json(input_dir / "scenarios.json")

    final_output = analyze_risks(assets, scenarios, controls)
>>>>>>> 4498b2444c855c010b59620d8d9a83d26dc188e0

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    #Output results in outputs/output.json
    with output_path.open("w", encoding="utf-8") as f:
<<<<<<< HEAD
        json.dump(final_output, f, indent=2)
=======
        ordered_output = {
            "summary": final_output["summary"],
            "risk_results": [
                {
                    "scenario_id":                         s.get("scenario_id"),
                    "asset_id":                            s.get("asset_id"),
                    "asset_name":                          s.get("asset_name"),
                    "threat":                              s.get("threat"),
                    "exposure":                            s.get("exposure"),
                    "initial_risk":                        s.get("initial_risk"),
                    "deployed_controls":                   s.get("deployed_controls"),
                    "residual_risk":                       s.get("residual_risk"),
                    "acceptable_threshold":                s.get("acceptable_threshold"),
                    "status":                              s.get("status"),
                    "recommended_controls":                s.get("recommended_controls"),
                    "projected_risk_after_recommendation": s.get("projected_risk_after_recommendation"),
                    "treatment_result":                    s.get("treatment_result"),
                    "priority":                            s.get("priority"),
                }
                for s in final_output["risk_results"]
            ]
        }
        json.dump(ordered_output, f, indent=2)


>>>>>>> 4498b2444c855c010b59620d8d9a83d26dc188e0

if __name__ == "__main__":
    main()
