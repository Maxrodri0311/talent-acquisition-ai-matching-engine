"""
End-to-End Integration Tests: Dimensional Model, DuckDB OLAP & Excel Builder
"""

import os
import pytest
import duckdb
import pandas as pd
from src.dimensional_model import DimensionalModelPipeline
from src.excel_builder import ExecutiveExcelBuilder


@pytest.fixture(scope="module")
def pipeline_results():
    pipeline = DimensionalModelPipeline()
    return pipeline.run_pipeline()


def test_processed_fact_applications_exists():
    path = "data/processed/fact_applications.parquet"
    assert os.path.exists(path)
    df = pd.read_parquet(path)
    assert len(df) > 0
    assert "composite_match_score" in df.columns
    assert "triage_category" in df.columns


def test_duckdb_star_schema_integrity():
    con = duckdb.connect("data/talent_analytics.duckdb")
    tables = con.execute("SHOW TABLES").fetchdf()["name"].tolist()
    
    expected_tables = ["dim_date", "dim_employers", "dim_channels", "dim_candidates", "fact_job_postings", "fact_applications"]
    for t in expected_tables:
        assert t in tables

    # Check that there are no orphan candidate IDs
    orphans = con.execute("""
        SELECT COUNT(*) as orphan_count
        FROM fact_applications f
        LEFT JOIN dim_candidates c ON f.candidate_id = c.candidate_id
        WHERE c.candidate_id IS NULL
    """).fetchdf()["orphan_count"].iloc[0]
    assert orphans == 0


def test_excel_dashboard_generation(pipeline_results):
    output_excel = "dist/Talent_Acquisition_Executive_Dashboard.xlsx"
    builder = ExecutiveExcelBuilder(output_path=output_excel)
    path = builder.build_dashboard(
        df_funnel=pipeline_results["funnel_summary"],
        df_channels=pipeline_results["channel_summary"],
        df_employers=pipeline_results["employer_summary"]
    )
    assert os.path.exists(path)
    assert os.path.getsize(path) > 3000
