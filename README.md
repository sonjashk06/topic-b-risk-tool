# Cybersecurity and National Defence -- Technical Project

## Topic B -- Cyber Risk Prioritization and Treatment Tool

---

## Group Members

- Sonja Shkembi -- s320526
- Eleonora Accatino -- s
- Thomas Sabena -- s
- Helya Pourkarim Kashki -- s320871

---

## Project Description
This project implements a simple cyber risk prioritization and treatment tool.
The program reads input data describing assets, threat scenarios, and security controls.
For each scenario, it computes the initial risk and the residual risk after applying the deployed controls.
If the residual risk exceeds the acceptable threshold defined for the asset, the program recommends additional controls using a greedy strategy.

The program produces a JSON output containing:
- risk evaluation for each scenario
- recommended controls (if needed)
- a summary of the overall analysis

---

## Project Structure
- `main.py`: main program that executes the analysis
- `src/`: Python modules used by the program
    - `src/loader.py`: Python modules used by the program
- `input/`: input JSON files
    - `src/assets.json`
    - `src/scenarios.json`
    - `src/security_controls.json`
- `output/`: generated output JSON file
- `requirements.txt`: list of required Python libraries

---

## Python Version
Python 3.13

---

## Required Libraries
This project uses only the Python standard library.


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
