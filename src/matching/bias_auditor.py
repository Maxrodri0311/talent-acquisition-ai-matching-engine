"""
Talent Acquisition AI Engine & Funnel Intelligence Platform
Module: Algorithmic Fairness & Bias Audit Engine (bias_auditor.py)

Audits model decisions for compliance with international AI ethics & hiring laws
(NYC Local Law 144 on Automated Employment Decision Tools - AEDT & EU AI Act).
Calculates Disparate Impact Ratio (DIR) and demographic selection parity.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any


class AlgorithmicBiasAuditor:
    """
    Evaluates algorithmic selection parity across demographic groups and geographic regions.
    Enforces the Four-Fifths Rule (80% Rule):
    Disparate Impact Ratio (DIR) = Selection_Rate_Protected / Selection_Rate_Reference >= 0.80
    """

    FOUR_FIFTHS_THRESHOLD = 0.80

    def evaluate_fairness(
        self,
        df_applications: pd.DataFrame,
        df_candidates: pd.DataFrame,
        demographic_column: str = "demographic_group",
        target_stage_column: str = "is_interviewed"
    ) -> Dict[str, Any]:
        """
        Calculates selection rates and Disparate Impact Ratios across demographic segments.
        """
        # Join applications with candidate demographic metadata
        df_merged = df_applications.merge(
            df_candidates[["candidate_id", demographic_column, "location_region"]],
            on="candidate_id",
            how="left"
        )

        group_stats = []
        unique_groups = df_merged[demographic_column].dropna().unique()

        # Calculate selection rate for each group
        for grp in unique_groups:
            grp_subset = df_merged[df_merged[demographic_column] == grp]
            total_apps = len(grp_subset)
            selected_apps = grp_subset[target_stage_column].sum()
            selection_rate = (selected_apps / total_apps) if total_apps > 0 else 0.0

            group_stats.append({
                "group": grp,
                "total_applicants": total_apps,
                "selected_count": int(selected_apps),
                "selection_rate": round(selection_rate, 4)
            })

        df_stats = pd.DataFrame(group_stats)
        if df_stats.empty:
            return {"status": "NO_DATA", "report": []}

        # Reference group is the group with the highest selection rate
        max_rate = df_stats["selection_rate"].max()
        ref_group = df_stats.loc[df_stats["selection_rate"] == max_rate, "group"].values[0]

        # Calculate DIR for each group relative to the reference group
        df_stats["disparate_impact_ratio"] = df_stats["selection_rate"].apply(
            lambda r: round(r / max_rate, 4) if max_rate > 0 else 1.0
        )
        df_stats["is_compliant_80_rule"] = df_stats["disparate_impact_ratio"].apply(
            lambda dir_val: 1 if dir_val >= self.FOUR_FIFTHS_THRESHOLD else 0
        )

        overall_compliant = bool(df_stats["is_compliant_80_rule"].min() == 1)

        return {
            "is_fairness_certified": overall_compliant,
            "reference_group": ref_group,
            "max_selection_rate": max_rate,
            "four_fifths_threshold": self.FOUR_FIFTHS_THRESHOLD,
            "detailed_parity_table": df_stats.to_dict(orient="records"),
        }
