def sort_and_prioritize(validResults: list) -> list:
    def sort_key(s):
        if s.get("status")=="acceptable": 
            acceptability_rank = 1
        else:
            acceptability_rank = 0
        residual_risk = -s.get("residual_risk", 0)  
        return (acceptability_rank, residual_risk, s["scenario_id"]) 

    sorted_results = sorted(validResults, key=sort_key)

    for rank, scenario in enumerate(sorted_results, start=1):
        scenario["priority"] = rank

    return sorted_results


def compute_summary(all_scenarios: list) -> dict:
    total = len(all_scenarios)

    count = 0
    for s in all_scenarios:
        if s.get("status") == "invalid":
            count += 1
    invalid_count = count

    count = 0
    for s in all_scenarios:
        if s.get("status")=="acceptable":
            count += 1
    acceptable_count = count

    count = 0
    for s in all_scenarios:
        if s.get("status")=="not_acceptable":
            count += 1
    not_acceptable_count = count

    valid_risks = []
    for s in all_scenarios:
        if s.get("status")!="invalid":
            valid_risks.append(s.get("residual_risk", 0))

    if len(valid_risks) > 0:
        highest = valid_risks[0]
        for risk in valid_risks:
            if risk > highest:
                highest = risk
    else:
        highest = 0

    return {
        "total_scenarios": total,
        "acceptable_scenarios": acceptable_count,
        "not_acceptable_scenarios": not_acceptable_count,
        "highest_residual_risk": highest,
    }

def build_output(scenario_results: list) -> dict:
    valid_scenarios = []
    invalid_scenarios = []
    
    for s in scenario_results:
        if s.get("status") == "invalid":
            invalid_scenarios.append(s)
        else:
            valid_scenarios.append(s)
    
    sorted_valid = sort_and_prioritize(valid_scenarios)

    for s in invalid_scenarios:
        s["priority"] = None

    all_scenarios = sorted_valid + invalid_scenarios

    summary = compute_summary(all_scenarios)

    return {
        "summary": summary,
        "risk_results": all_scenarios,
    }