def compute_initial_risk(likelihood, impact):
    """
    Compute risk formula before applying any controls.
    risk = likelihood x impact.
    """
    return likelihood * impact


def compute_residual_risk(likelihood, impact, controls):
    """
    Compute risk after applying the controls.
    We sum all reductions from the controls, then apply them together.
    """
    
    total_likelihood_reduction = sum(c["likelihood_reduction"] for c in controls)
    total_impact_reduction = sum(c["impact_reduction"] for c in controls)

    #apply reductions(not less than 1)
    residual_likelihood = max(1, likelihood - total_likelihood_reduction)
    residual_impact = max(1, impact - total_impact_reduction)

    #final residual risk
    residual_risk = residual_likelihood * residual_impact

    return residual_likelihood, residual_impact, residual_risk