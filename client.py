"""
Cerebrovascular CO2 Reactivity (CVR) & Breath-Holding Vasomotor Reserve Engine.
Provides deterministic, zero-dependency calculation of the Breath-Holding Index (BHI),
middle cerebral artery flow velocity (CBFv) percentage surge, and microvascular reserve.
"""

from typing import Dict, Any, List, Optional


class CerebrovascularReactivityClient:
    """
    Deterministic client for calculating Cerebrovascular Reactivity (CVR) and Breath-Holding Index (BHI).
    Pure Python standard library implementation based on Markus & Harrison Transcranial Doppler standards.
    """

    def __init__(self):
        pass

    def calculate_breath_holding_index(
        self,
        baseline_cbfv_cm_s: float,
        hypercapnia_peak_cbfv_cm_s: float,
        apnea_duration_sec: float = 30.0
    ) -> Dict[str, Any]:
        """
        Calculates Breath-Holding Index (BHI):
        BHI = ((Peak_CBFv - Base_CBFv) / Base_CBFv) * (100 / Apnea_Duration_sec).
        Standard apnea duration is 30 seconds.
        Normal physiological BHI is >= 1.20 %/s.
        """
        if baseline_cbfv_cm_s <= 0 or apnea_duration_sec < 10.0:
            return {"error": "Baseline CBFv must be positive and apnea duration must be at least 10 seconds"}

        delta_cbfv = max(0.0, hypercapnia_peak_cbfv_cm_s - baseline_cbfv_cm_s)
        pct_increase = round((delta_cbfv / baseline_cbfv_cm_s) * 100.0, 1)

        bhi = round(pct_increase / apnea_duration_sec, 3)

        # Cerebrovascular Vasomotor Reserve Index (CVRI, 0 - 100):
        # BHI >= 1.4 %/s -> 90+
        # BHI 1.2 - 1.4 -> 75 - 90
        # BHI 0.7 - 1.19 -> 45 - 74
        # BHI < 0.69 -> < 40 (Impaired Vasomotor Reserve)
        if bhi >= 1.40:
            cvri = min(100.0, 85.0 + (bhi - 1.40) * 25.0)
        elif bhi >= 1.20:
            cvri = 75.0 + ((bhi - 1.20) / 0.20) * 10.0
        elif bhi >= 0.70:
            cvri = 45.0 + ((bhi - 0.70) / 0.50) * 30.0
        else:
            cvri = max(5.0, (bhi / 0.70) * 45.0)

        cvri_score = round(min(100.0, max(5.0, cvri)), 1)

        is_impaired = bhi < 0.69

        if cvri_score >= 80.0:
            tier = "OPTIMAL_CEREBROVASCULAR_RESERVE"
            interpretation = f"Normal robust arteriolar vasodilation (+{pct_increase}% in {apnea_duration_sec}s; BHI {bhi}%/s); cerebral autoregulatory dilation is intact."
            recommendation = "Cerebral microvascular compliance is exceptional. Maintain regular aerobic exercise and healthy blood pressure."
        elif not is_impaired:
            tier = "BORDERLINE_VASOMOTOR_RESPONSIVENESS"
            interpretation = f"Mildly attenuated CO2 reactivity (+{pct_increase}%; BHI {bhi}%/s); modest reduction in arteriolar dilatatory capacity."
            recommendation = "Incorporate pranayama / controlled breath retention drills and verify endothelial dietary nitrate intake."
        else:
            tier = "IMPAIRED_CEREBROVASCULAR_VASOMOTOR_RESERVE"
            interpretation = f"Significantly diminished vasodilatory capacity (BHI {bhi}%/s < 0.69); microvascular cerebral compliance compromised."
            recommendation = "Compromised cerebral reserve indicates elevated hemodynamic vulnerability. Recommend clinical neurovascular consultation."

        return {
            "baseline_cbfv_cm_s": baseline_cbfv_cm_s,
            "peak_hypercapnic_cbfv_cm_s": hypercapnia_peak_cbfv_cm_s,
            "delta_velocity_cm_s": round(delta_cbfv, 2),
            "percentage_velocity_increase": pct_increase,
            "apnea_duration_sec": apnea_duration_sec,
            "breath_holding_index_pct_s": bhi,
            "cerebrovascular_reserve_index": cvri_score,
            "classification": tier,
            "physiological_interpretation": interpretation,
            "actionable_guidance": recommendation
        }
