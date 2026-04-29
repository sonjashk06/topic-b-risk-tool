import argparse
import json
from pathlib import Path

from src.analysis import analyze_all
from src.output import build_output
from src.loader import load_json, build_asset_dict, build_control_dict, extract_scenarios

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input directory")
    parser.add_argument("--output", required=True, help="Output JSON file")
    return parser.parse_args()

def main():
    args = parse_args()
    input_dir = Path(args.input)

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

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    #Output results in outputs/output.json
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2)

if __name__ == "__main__":
    main()
