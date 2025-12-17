from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "AP-PowerSupply.csv"
MODEL_DIR = BASE_DIR / "models"
ARTIFACT_DIR = BASE_DIR / "artifacts"
MODEL_PATH = MODEL_DIR / "xgboost_energy_requirement.joblib"
REPORT_PATH = ARTIFACT_DIR / "training_report.json"

COLUMN_RENAMES = {
    "Energy Required (MU)": "energy_required_mu",
    "Energy Met (MU)": "energy_met_mu",
    "Energy +/- (MU)": "energy_delta_mu",
    "Genco Thermal": "genco_thermal",
    "Genco Hydel": "genco_hydel",
    "Genco Total": "genco_total",
    "CGS and Purchases": "cgs_and_purchases",
    "IPPS (GAS)": "ipps_gas",
    "NCEs & Others": "nces_others",
    "AP Share of TGISTS": "ap_share_tgists",
    "Grand Total": "grand_total",
    "Reversible Pump Consumption": "reversible_pump_consumption",
    "Unrestricted Peak Demand (MW)": "unrestricted_peak_demand_mw",
    "Deficit/Surplus (MW)": "deficit_surplus_mw",
}

USER_INPUT_FEATURES = [
    {
        "key": "energy_met_mu",
        "label": "Energy Met (MU)",
        "description": "Actual energy served to the state grid on the planning day.",
    },
    {
        "key": "energy_delta_mu",
        "label": "Energy +/- (MU)",
        "description": "Energy surplus (+) or shortfall (-) carried into the day.",
    },
    {
        "key": "genco_thermal",
        "label": "GENCO Thermal (MU)",
        "description": "Projected supply from APGENCO thermal assets.",
    },
    {
        "key": "genco_hydel",
        "label": "GENCO Hydel (MU)",
        "description": "Projected supply from hydel generation.",
    },
    {
        "key": "genco_total",
        "label": "GENCO Total (MU)",
        "description": "Total state GENCO generation available.",
    },
    {
        "key": "cgs_and_purchases",
        "label": "CGS + Purchases (MU)",
        "description": "Central generating stations and open-market purchases.",
    },
    {
        "key": "ipps_gas",
        "label": "IPPs (Gas) (MU)",
        "description": "Independent power producers on gas contracts.",
    },
    {
        "key": "nces_others",
        "label": "NCEs & Others (MU)",
        "description": "Non-conventional energy (solar/wind/etc.).",
    },
    {
        "key": "ap_share_tgists",
        "label": "AP Share of TSGENCO (MU)",
        "description": "Imported share from Telangana generating stations.",
    },
    {
        "key": "grand_total",
        "label": "Grand Total Availability (MU)",
        "description": "All supply sources combined for the day.",
    },
    {
        "key": "reversible_pump_consumption",
        "label": "Reversible Pump Consumption (MU)",
        "description": "Storage pumping obligations.",
    },
    {
        "key": "unrestricted_peak_demand_mw",
        "label": "Unrestricted Peak Demand (MW)",
        "description": "Peak demand expected without load shedding.",
    },
    {
        "key": "deficit_surplus_mw",
        "label": "Deficit / Surplus (MW)",
        "description": "Instantaneous MW level shortfall (-) or surplus (+).",
    },
]
