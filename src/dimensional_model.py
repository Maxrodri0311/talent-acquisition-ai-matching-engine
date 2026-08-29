"""
Talent Acquisition AI Engine & Funnel Intelligence Platform
Module: OLAP Star Schema & Dimensional Pipeline Engine (dimensional_model.py)

Ingests raw candidate and application events, applies security sanitization and
vectorized matching, and instantiates the Kimball Star Schema in DuckDB.
"""

import os
import duckdb
import pandas as pd
from typing import Dict, Any

try:
    from src.security.sanitizer import ZeroTrustSanitizer
    from src.matching.matching_engine import CompositeMatchingEngine
    from src.matching.triage_classifier import TriageClassifier
    from src.matching.bias_auditor import AlgorithmicBiasAuditor
except ImportError:
    from security.sanitizer import ZeroTrustSanitizer
    from matching.matching_engine import CompositeMatchingEngine
    from matching.triage_classifier import TriageClassifier
    from matching.bias_auditor import AlgorithmicBiasAuditor


class DimensionalModelPipeline:
    """
    Orchestrates the transformation from raw lakehouse files to analytical Star Schema.
    """

    def __init__(self, db_path: str = "data/talent_analytics.duckdb"):
        self.db_path = db_path
        self.sanitizer = ZeroTrustSanitizer()
        self.matcher = CompositeMatchingEngine()
        self.triage = TriageClassifier()
        self.bias_auditor = AlgorithmicBiasAuditor()

    def process_and_enrich_applications(
        self,
        raw_applications_path: str = "data/raw/raw_applications.parquet",
        output_processed_path: str = "data/processed/fact_applications.parquet"
    ) -> pd.DataFrame:
        """
        Runs the security firewall, vectorized matching, and 3-band triage on raw applications.
        """
        print("[Dimensional Pipeline] Reading raw applications...")
        df_raw = pd.read_parquet(raw_applications_path)

        # 1. Apply Security Firewall & Sanitization
        print("[Dimensional Pipeline] Running Zero-Trust Security Firewall on submissions...")
        security_flags = []
        for _, row in df_raw.iterrows():
            payload = str(row.get("adversarial_payload", "")) if row.get("is_adversarial_injection", 0) == 1 else ""
            skills_text = str(row.get("candidate_skills", ""))
            full_text = f"{skills_text} {payload}".strip()

            sec_result = self.sanitizer.sanitize_candidate_submission(full_text, row.get("candidate_id", ""))
            security_flags.append(sec_result["is_security_flagged"])

        df_raw["is_adversarial_injection"] = security_flags

        # 2. Apply Vectorized Composite Matching Engine
        print("[Dimensional Pipeline] Computing vectorized Jaccard + TF-IDF Cosine Match Scores...")
        df_matched = self.matcher.calculate_batch_matching(df_raw)

        # 3. Apply 3-Tier Human-in-the-Loop Triage Classifier
        print("[Dimensional Pipeline] Applying 3-Band Triage Classification and Funnel routing...")
        df_final = self.triage.classify_dataframe(df_matched)

        # Export to processed lakehouse
        os.makedirs(os.path.dirname(output_processed_path), exist_ok=True)
        df_final.to_parquet(output_processed_path, engine="pyarrow", compression="snappy", index=False)
        print(f"[Dimensional Pipeline] fact_applications exported: {len(df_final):,} rows -> {output_processed_path}")

        return df_final

    def build_star_schema_in_duckdb(self, ddl_script_path: str = "sql/schema_ddl.sql") -> duckdb.DuckDBPyConnection:
        """
        Executes pure ANSI SQL DDL scripts to instantiate the Kimball Star Schema in DuckDB.
        """
        print(f"[Dimensional Pipeline] Connecting to DuckDB database -> {self.db_path}")
        con = duckdb.connect(self.db_path)

        with open(ddl_script_path, "r", encoding="utf-8") as f:
            ddl_sql = f.read()

        con.execute(ddl_sql)
        print("[Dimensional Pipeline] Kimball Star Schema tables created successfully in DuckDB.")

        # Create Tableau / Looker views
        views_script = "sql/tableau_looker_views.sql"
        if os.path.exists(views_script):
            with open(views_script, "r", encoding="utf-8") as f:
                views_sql = f.read()
            con.execute(views_sql)
            print("[Dimensional Pipeline] Analytical views registered in DuckDB.")

        return con

    def run_pipeline(self) -> Dict[str, Any]:
        """
        Executes end-to-end dimensional modeling pipeline.
        """
        df_applications = self.process_and_enrich_applications()
        con = self.build_star_schema_in_duckdb()

        # Run Funnel Analytics Query from SQL file
        with open("sql/funnel_analytics.sql", "r", encoding="utf-8") as f:
            analytics_sql = f.read()

        queries = [q.strip() for q in analytics_sql.split(";") if q.strip()]
        funnel_summary_df = con.execute(queries[0]).fetchdf()
        channel_summary_df = con.execute(queries[1]).fetchdf()
        employer_summary_df = con.execute(queries[2]).fetchdf()

        # Run Bias Audit
        df_candidates = pd.read_parquet("data/raw/dim_candidates.parquet")
        bias_report = self.bias_auditor.evaluate_fairness(df_applications, df_candidates)

        return {
            "funnel_summary": funnel_summary_df,
            "channel_summary": channel_summary_df,
            "employer_summary": employer_summary_df,
            "bias_report": bias_report,
        }


def main():
    pipeline = DimensionalModelPipeline()
    results = pipeline.run_pipeline()

    print("\n" + "=" * 80)
    print(">> EXECUTIVE TALENT ACQUISITION FUNNEL SUMMARY (DUCKDB OLAP)")
    print("=" * 80)
    print(results["funnel_summary"].to_string(index=False))

    print("\n" + "=" * 80)
    print(">> SOURCING CHANNEL EFFICIENCY & COST-PER-HIRE")
    print("=" * 80)
    print(results["channel_summary"].to_string(index=False))

    print("\n" + "=" * 80)
    print(f">> AI FAIRNESS & NYC LAW 144 AUDIT: Certified Compliant = {results['bias_report']['is_fairness_certified']}")
    print("=" * 80)


if __name__ == "__main__":
    main()
