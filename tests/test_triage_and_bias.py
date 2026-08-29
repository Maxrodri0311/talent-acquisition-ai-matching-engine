"""
Unit & Integration Tests: 3-Tier Triage Classifier & Algorithmic Bias Auditor
"""

import pytest
import pandas as pd
from src.matching.triage_classifier import TriageClassifier
from src.matching.bias_auditor import AlgorithmicBiasAuditor


@pytest.fixture
def triage_classifier():
    return TriageClassifier()


@pytest.fixture
def bias_auditor():
    return AlgorithmicBiasAuditor()


def test_triage_direct_applicable(triage_classifier):
    cat, reason = triage_classifier.classify_application(
        match_score=88.5,
        candidate_exp=5,
        req_exp=4,
        salary_exp=4000,
        salary_max=5000,
        is_security_flagged=0
    )
    assert cat == "DIRECT_APPLICABLE"


def test_triage_security_flag_routes_to_human_review(triage_classifier):
    cat, reason = triage_classifier.classify_application(
        match_score=95.0,
        candidate_exp=6,
        req_exp=4,
        salary_exp=4500,
        salary_max=5000,
        is_security_flagged=1  # Prompt injection flagged
    )
    assert cat == "HUMAN_REVIEW_FLAGGED"
    assert "SECURITY_ALERT" in reason


def test_triage_overqualified_routes_to_human_review(triage_classifier):
    cat, reason = triage_classifier.classify_application(
        match_score=85.0,
        candidate_exp=15,
        req_exp=2,
        salary_exp=3000,
        salary_max=3500,
        is_security_flagged=0
    )
    assert cat == "HUMAN_REVIEW_FLAGGED"
    assert "OVERQUALIFIED" in reason


def test_triage_auto_reject(triage_classifier):
    cat, reason = triage_classifier.classify_application(
        match_score=42.0,
        candidate_exp=1,
        req_exp=5,
        salary_exp=4000,
        salary_max=5000,
        is_security_flagged=0
    )
    assert cat == "AUTO_REJECT"


def test_bias_auditor_four_fifths_rule(bias_auditor):
    df_apps = pd.DataFrame([
        {"candidate_id": "C1", "is_interviewed": 1},
        {"candidate_id": "C2", "is_interviewed": 1},
        {"candidate_id": "C3", "is_interviewed": 0},
        {"candidate_id": "C4", "is_interviewed": 1},
        {"candidate_id": "C5", "is_interviewed": 0},
    ])
    df_cands = pd.DataFrame([
        {"candidate_id": "C1", "demographic_group": "Group_A", "location_region": "Reg_1"},
        {"candidate_id": "C2", "demographic_group": "Group_A", "location_region": "Reg_1"},
        {"candidate_id": "C3", "demographic_group": "Group_A", "location_region": "Reg_1"},
        {"candidate_id": "C4", "demographic_group": "Group_B", "location_region": "Reg_2"},
        {"candidate_id": "C5", "demographic_group": "Group_B", "location_region": "Reg_2"},
    ])
    report = bias_auditor.evaluate_fairness(df_apps, df_cands)
    assert "is_fairness_certified" in report
    assert len(report["detailed_parity_table"]) == 2
