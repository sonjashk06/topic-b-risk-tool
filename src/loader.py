import json
from pathlib import Path
from typing import Any, Dict


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
    

def build_asset_dict(assets_data: Dict) -> Dict:
    # Converts assets JSON into dictionary: id -> asset
    assets = assets_data.get("assets", [])
    return {asset["id"]: asset for asset in assets}


def build_control_dict(controls_data: Dict) -> Dict:
    #converts controls JSON into dictionary: id -> control
    controls = controls_data.get("security_controls", [])
    return {control["id"]: control for control in controls}


def extract_scenarios(scenarios_data: Dict):
    # extracts the list of scenarios
    return scenarios_data.get("scenarios", [])