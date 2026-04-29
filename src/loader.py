import json
from pathlib import Path
from typing import Any, Dict


def load_json(path: Path) -> Any:
    """
    Open and load the content of the input files. 
    (assests.json, scenarios.json, controls.json)
    """
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_asset_dict(assets_data: Dict) -> Dict:
    #Convert the list of assests into a dictionary
    return {a["id"]: a for a in assets_data.get("assets", [])}


def build_control_dict(controls_data: Dict) -> Dict:
    #Converts the list of controls into a dictionary
    return {c["id"]: c for c in controls_data.get("security_controls", [])}


def extract_scenarios(scenarios_data: Dict):
    #get the list of scenarios from the JSON
    return scenarios_data.get("scenarios", [])