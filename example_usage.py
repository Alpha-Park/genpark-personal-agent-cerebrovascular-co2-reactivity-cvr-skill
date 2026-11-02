"""
Example usage for Cerebrovascular CO2 Reactivity (CVR) Skill.
Demonstrates analyzing Transcranial Doppler breath-holding challenge.
"""

from client import CerebrovascularReactivityClient


def main():
    client = CerebrovascularReactivityClient()

    print("=== 1. Calculating Breath-Holding Index (30-Second Apnea Challenge) ===")
    res = client.calculate_breath_holding_index(
        baseline_cbfv_cm_s=62.0,
        hypercapnia_peak_cbfv_cm_s=91.5,
        apnea_duration_sec=30.0
    )

    print(f"Baseline CBFv: {res['baseline_cbfv_cm_s']} cm/s | Peak CBFv: {res['peak_hypercapnic_cbfv_cm_s']} cm/s")
    print(f"Velocity Surge: +{res['percentage_velocity_increase']} % in {res['apnea_duration_sec']}s")
    print(f"Breath-Holding Index (BHI): {res['breath_holding_index_pct_s']} %/s (Normative: >= 1.20 %/s)")
    print(f"Cerebrovascular Reserve Index: {res['cerebrovascular_reserve_index']} / 100")
    print(f"Classification: {res['classification']}")
    print(f"Interpretation: {res['physiological_interpretation']}")
    print(f"Guidance: {res['actionable_guidance']}")


if __name__ == "__main__":
    main()
