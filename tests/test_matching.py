"""
Unit & Integration Tests: Composite Matching Engine & Vector Sim
"""

import pytest
import pandas as pd
from src.matching.matching_engine import CompositeMatchingEngine


@pytest.fixture
def matching_engine():
    return CompositeMatchingEngine()


def test_jaccard_similarity(matching_engine):
    cand = "Python; SQL; DuckDB; Docker"
    job = "Python; SQL; DuckDB; Kubernetes"
    # Intersect: Python, SQL, DuckDB (3)
    # Union: Python, SQL, DuckDB, Docker, Kubernetes (5)
    # Expected: 3/5 = 0.60
    jaccard = matching_engine.calculate_jaccard_similarity(cand, job)
    assert round(jaccard, 2) == 0.60


def test_experience_penalty_bounds(matching_engine):
    assert matching_engine.calculate_experience_penalty(5, 5) == 1.0
    assert matching_engine.calculate_experience_penalty(10, 5) == 1.0
    assert matching_engine.calculate_experience_penalty(2, 4) == 0.50
    assert matching_engine.calculate_experience_penalty(0, 5) == 0.0


def test_batch_matching_execution(matching_engine):
    df = pd.DataFrame([
        {
            "candidate_skills": "Python; SQL; Scikit-Learn; DuckDB",
            "job_required_skills": "Python; SQL; Scikit-Learn; DuckDB",
            "candidate_experience_years": 6,
            "job_min_experience_years": 5
        },
        {
            "candidate_skills": "Tableau; Excel",
            "job_required_skills": "Python; PyTorch; Kubernetes",
            "candidate_experience_years": 1,
            "job_min_experience_years": 8
        }
    ])
    df_res = matching_engine.calculate_batch_matching(df)

    assert len(df_res) == 2
    assert "composite_match_score" in df_res.columns
    # First row should have high score (>90%)
    assert df_res.iloc[0]["composite_match_score"] >= 90.0
    # Second row should have low score (<25%)
    assert df_res.iloc[1]["composite_match_score"] < 25.0
