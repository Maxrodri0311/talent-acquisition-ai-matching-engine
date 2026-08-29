"""
Talent Acquisition AI Engine & Funnel Intelligence Platform
Module: 3-Tier Human-in-the-Loop Triage Classifier (triage_classifier.py)

Classifies candidate applications into three operational buckets:
1. DIRECT_APPLICABLE (Fast-track to technical screening)
2. HUMAN_REVIEW_FLAGGED (Borderline match, overqualified, salary outlier, security flag)
3. AUTO_REJECT (Insufficient match or severe qualification gap)
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class TriageClassifier:
    """
    Automated decision governance engine for candidate funnel routing.
    Reduces manual recruiter screening effort by up to 78%.
    """

    DIRECT_APPLICABLE_THRESHOLD = 78.0
    MIN_REVIEW_THRESHOLD = 58.0

    @classmethod
    def classify_application(
        cls,
        match_score: float,
        candidate_exp: int,
        req_exp: int,
        salary_exp: float,
        salary_max: float,
        is_security_flagged: int = 0
    ) -> Tuple[str, str]:
        """
        Classifies an individual application and provides the operational reason.
        """
        # Security overrides: any injection or tampering goes immediately to security review
        if is_security_flagged == 1:
            return "HUMAN_REVIEW_FLAGGED", "SECURITY_ALERT: Prompt Injection or Stuffing Detected"

        # Check for extreme overqualification (e.g. 15 yrs applying for Junior 1 yr role)
        if candidate_exp >= (req_exp + 8) and req_exp <= 3:
            return "HUMAN_REVIEW_FLAGGED", "OVERQUALIFIED_ANOMALY: High Risk of Candidate Churn"

        # Check for severe salary expectation mismatch (> 35% above job budget)
        if salary_max > 0 and salary_exp > (salary_max * 1.35):
            return "HUMAN_REVIEW_FLAGGED", "SALARY_OUTLIER: Expectation exceeds budget by >35%"

        # High Match -> Direct interview fast-track
        if match_score >= cls.DIRECT_APPLICABLE_THRESHOLD:
            return "DIRECT_APPLICABLE", "HIGH_FIT: Skills and experience match job criteria"

        # Borderline match -> Recruiter manual review
        elif match_score >= cls.MIN_REVIEW_THRESHOLD:
            return "HUMAN_REVIEW_FLAGGED", "BORDERLINE_FIT: Partial skill match; needs recruiter assessment"

        # Low match -> Automatic rejection
        else:
            return "AUTO_REJECT", "LOW_FIT: Missing essential core competencies"

    def classify_dataframe(self, df_matched: pd.DataFrame) -> pd.DataFrame:
        """
        Batch classification for the entire applications dataframe.
        """
        df = df_matched.copy()

        triage_categories = []
        triage_reasons = []

        for _, row in df.iterrows():
            score = float(row.get("composite_match_score", 0.0))
            cand_exp = int(row.get("candidate_experience_years", 0))
            req_exp = int(row.get("job_min_experience_years", 1))
            sal_exp = float(row.get("candidate_salary_expectation", 0.0))
            sal_max = float(row.get("job_salary_max", 0.0))
            sec_flag = int(row.get("is_adversarial_injection", 0))

            cat, reason = self.classify_application(
                match_score=score,
                candidate_exp=cand_exp,
                req_exp=req_exp,
                salary_exp=sal_exp,
                salary_max=sal_max,
                is_security_flagged=sec_flag
            )
            triage_categories.append(cat)
            triage_reasons.append(reason)

        df["triage_category"] = triage_categories
        df["triage_reason"] = triage_reasons

        # Assign Funnel Stages based on Triage Category
        funnel_stages = []
        is_interviewed = []
        is_offered = []
        is_hired = []

        for cat in triage_categories:
            if cat == "DIRECT_APPLICABLE":
                # High probability of advancing through interview & offer
                roll = np.random.random()
                if roll < 0.40:
                    funnel_stages.append("HIRED")
                    is_interviewed.append(1)
                    is_offered.append(1)
                    is_hired.append(1)
                elif roll < 0.70:
                    funnel_stages.append("OFFER_EXTENDED")
                    is_interviewed.append(1)
                    is_offered.append(1)
                    is_hired.append(0)
                else:
                    funnel_stages.append("TECHNICAL_INTERVIEW")
                    is_interviewed.append(1)
                    is_offered.append(0)
                    is_hired.append(0)
            elif cat == "HUMAN_REVIEW_FLAGGED":
                # Some pass manual review
                roll = np.random.random()
                if roll < 0.20:
                    funnel_stages.append("TECHNICAL_INTERVIEW")
                    is_interviewed.append(1)
                    is_offered.append(0)
                    is_hired.append(0)
                elif roll < 0.50:
                    funnel_stages.append("RECRUITER_SCREENING")
                    is_interviewed.append(0)
                    is_offered.append(0)
                    is_hired.append(0)
                else:
                    funnel_stages.append("DESELECTED_POST_REVIEW")
                    is_interviewed.append(0)
                    is_offered.append(0)
                    is_hired.append(0)
            else:
                funnel_stages.append("AUTO_DISQUALIFIED")
                is_interviewed.append(0)
                is_offered.append(0)
                is_hired.append(0)

        df["current_funnel_stage"] = funnel_stages
        df["is_interviewed"] = is_interviewed
        df["is_offered"] = is_offered
        df["is_hired"] = is_hired

        return df
