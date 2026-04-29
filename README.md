# Cybersecurity and National Defence -- Technical Project

## Topic B -- Cyber Risk Prioritization and Treatment Tool

---

## Group Members

- Sonja Shkembi -- s320526
- Eleonora Accatino -- s323779
- Thomas Sabena -- s324196
- Helya Pourkarim Kashki -- s320871

---

## Project Description
This project implements a simple cyber risk analysis tool.

The program takes as input:
- a list of assets
- a list of threat scenarios
- a catalog of security controls

For each scenario, the tool:
1. computes the initial risk (likelihood × impact)
2. applies the deployed controls to compute the residual risk
3. checks if the risk is acceptable based on the asset threshold
4. if not acceptable, suggests additional controls using a greedy strategy

The program produces a JSON output containing:
- risk evaluation for each scenario
- recommended controls (if needed)
- a summary of the overall analysis

---

## Project Structure
- `main.py`: main program that executes the analysis
- `src/`: Python modules used by the program
    - `src/loader.py`: loads and prepares input data
    - `src/risk.py`: risk computation logic
    - `src/controls.py`: reccomends controls if needed
    - `src/analysis.py`: analysis of all scenarios
    - `src/output.py`: formatting and summary of the result
- `input/`: input JSON files
    - `src/assets.json`
    - `src/scenarios.json`
    - `src/security_controls.json`
- `output/`: generated output JSON file
- `requirements.txt`: list of required Python libraries (In our project this file is empty, since no external Python libraries are used)

---

## Work distribution
The work was divided among the group members as follows:
- Helya - Risk computation logic
- Sonja - Data loading + scenario analysis
- Thomas - Control recommendation logic
- Eleonora - Main logic and output formatting

We all worked together on refining the code structure, improving readability, and ensuring there was no duplicated logic or unnecessary code.

---
## Notes
- Check output.json correctness
- Invalid scenarios(unknown assets or controls) are handled and reported
- Empty control lists handled correctly.
- Risk values do not go below 1.

---

## Python Version
Python 3.13

---

## Required Libraries
This project uses only the Python standard library. No external dependencies are required.


## Creating a Virtual Environment
A virtual environment is recommended in order to install the project libraries in an isolated way.

### Linux / macOS
```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```
