# -*- coding: utf-8 -*-
"""Dynamic Blood Biomarker & Longevity Protocol Optimizer Skill for GenPark Personal Health Agents."""
import json
from typing import Dict, Any, List

def audit_blood_biomarker_panel(apob_mg_dl: float, hba1c_pct: float, hscrp_mg_l: float, chronological_age_years: int, vitamin_d_ng_ml: float = 45.0) -> Dict[str, Any]:
    risk_flags = []
    bio_age_penalty = 0.0

    # Cardiovascular Atherogenic Burden (ApoB)
    if apob_mg_dl > 90.0:
        bio_age_penalty += 2.5
        risk_flags.append({
            "biomarker": "ApoB",
            "value": apob_mg_dl,
            "target": "< 70 mg/dL",
            "status": "ELEVATED_ATHEROGENIC_PARTICLES",
            "impact": "Accelerated arterial endothelial plaque deposition."
        })
    elif apob_mg_dl > 70.0:
        bio_age_penalty += 0.8
        risk_flags.append({
            "biomarker": "ApoB",
            "value": apob_mg_dl,
            "target": "< 70 mg/dL",
            "status": "BORDERLINE_MODERATE",
            "impact": "Mild atherogenic particle elevation."
        })

    # Glycemic Dysregulation (HbA1c)
    if hba1c_pct >= 5.7:
        bio_age_penalty += 3.0
        risk_flags.append({
            "biomarker": "HbA1c",
            "value": hba1c_pct,
            "target": "< 5.4%",
            "status": "PREDIABETIC_DYSREGULATION",
            "impact": "Chronic systemic advanced glycation end-products (AGEs)."
        })
    elif hba1c_pct > 5.4:
        bio_age_penalty += 1.0

    # Systemic Low-Grade Inflammation (hs-CRP)
    if hscrp_mg_l > 2.0:
        bio_age_penalty += 2.5
        risk_flags.append({
            "biomarker": "hs-CRP",
            "value": hscrp_mg_l,
            "target": "< 0.8 mg/L",
            "status": "CHRONIC_SYSTEMIC_INFLAMMATION",
            "impact": "Elevated inflammatory cytokine cascade."
        })
    elif hscrp_mg_l > 0.8:
        bio_age_penalty += 0.5

    # Vitamin D hormone status
    if vitamin_d_ng_ml < 30.0:
        bio_age_penalty += 1.0
        risk_flags.append({
            "biomarker": "Vitamin D (25-OH)",
            "value": vitamin_d_ng_ml,
            "target": "40 - 60 ng/mL",
            "status": "INSUFFICIENT",
            "impact": "Sub-optimal immune modulation and bone turnover."
        })

    estimated_biological_age = round(chronological_age_years + bio_age_penalty, 1)

    if bio_age_penalty > 4.0:
        summary_tier = "ACCELERATED_BIOLOGICAL_AGING"
    elif bio_age_penalty > 1.5:
        summary_tier = "MILD_METABOLIC_FRICTION"
    else:
        summary_tier = "OPTIMAL_LONGEVITY_TRAJECTORY"

    return {
        "chronological_age_years": chronological_age_years,
        "estimated_biological_age_years": estimated_biological_age,
        "biological_age_delta_years": round(bio_age_penalty, 1),
        "trajectory_tier": summary_tier,
        "flagged_biomarkers_count": len(risk_flags),
        "biomarker_deviations": risk_flags,
        "longevity_sentinel": "GenPark Preventive Biomarker Telemetry"
    }

def recommend_longevity_interventions(primary_risk_factor: str, estimated_biological_age_delta: float) -> Dict[str, Any]:
    protocols = []

    if primary_risk_factor == "atherogenic_lipids":
        protocols.append({
            "domain": "Lipid Lowering & Clearance",
            "interventions": [
                "Increase viscous soluble fiber (psyllium husk, beta-glucan) by 10-15g daily to trap bile acids.",
                "Reduce saturated fat intake to < 6% of total caloric expenditure.",
                "Consult physician regarding low-dose ApoB lowering pharmacological therapy (e.g. ezetimibe/statin)."
            ]
        })
    elif primary_risk_factor == "glycemic_dysregulation":
        protocols.append({
            "domain": "Insulin Sensitivity Optimization",
            "interventions": [
                "Zone 2 aerobic endurance cardio (150-180 mins/week) to upregulate mitochondrial density.",
                "Postprandial 10-minute zone-1 brisk walking following high carbohydrate intake.",
                "Time-restricted feeding window (14:10 or 16:8) to facilitate nocturnal hepatic glycogen depletion."
            ]
        })
    elif primary_risk_factor == "systemic_inflammation":
        protocols.append({
            "domain": "Anti-Inflammatory Modulation",
            "interventions": [
                "High-potency Omega-3 EPA/DHA supplementation (2-3g daily total fatty acids).",
                "Deep restorative slow-wave sleep prioritization (> 90 minutes deep sleep per night).",
                "Polyphenol-rich Mediterranean dietary cadence (extra virgin olive oil, berries, dark leafy greens)."
            ]
        })
    else:
        protocols.append({
            "domain": "Longevity Maintenance",
            "interventions": [
                "Maintain progressive resistance strength training 3x/week for lean muscle mass preservation.",
                "Annual comprehensive blood biomarker review."
            ]
        })

    return {
        "targeted_risk_cluster": primary_risk_factor,
        "biological_reversal_goal_years": round(max(0.5, estimated_biological_age_delta), 1),
        "recommended_protocols": protocols,
        "disclaimer": "Informational health telemetry only. Consult board-certified medical physicians for diagnostic treatment."
    }
