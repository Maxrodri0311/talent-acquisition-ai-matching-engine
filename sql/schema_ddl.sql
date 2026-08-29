-- ============================================================================
-- TALENT ACQUISITION & FUNNEL INTELLIGENCE PLATFORM (KIMBALL STAR SCHEMA DDL)
-- Target Database: DuckDB OLAP Columnar Engine
-- Author: Maximiliano Rodriguez (Staff Data Architect)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. DIMENSION TABLES
-- ----------------------------------------------------------------------------

-- Date Dimension (Time Intelligence)
CREATE OR REPLACE TABLE dim_date AS
SELECT 
    date_id,
    full_date,
    year,
    quarter,
    month,
    month_name,
    week_of_year,
    day_of_month,
    day_of_week,
    day_name,
    is_weekend
FROM read_parquet('data/raw/dim_date.parquet');

-- Employers Dimension
CREATE OR REPLACE TABLE dim_employers AS
SELECT 
    employer_id,
    employer_name,
    tier AS company_tier,
    industry,
    size_bucket AS company_size_bucket
FROM read_parquet('data/raw/dim_employers.parquet');

-- Recruitment Sourcing Channels Dimension
CREATE OR REPLACE TABLE dim_channels AS
SELECT 
    channel_id,
    channel_name,
    channel_type,
    cost_per_posting
FROM read_parquet('data/raw/dim_channels.parquet');

-- Candidate Dimension (Sanitized & Tokenized)
CREATE OR REPLACE TABLE dim_candidates AS
SELECT 
    candidate_id,
    anonymous_token,
    education_level,
    total_years_experience,
    primary_domain,
    skills_list,
    location_region,
    demographic_group
FROM read_parquet('data/raw/dim_candidates.parquet');


-- ----------------------------------------------------------------------------
-- 2. FACT TABLES
-- ----------------------------------------------------------------------------

-- Fact Job Postings (Requisition Lifecycle)
CREATE OR REPLACE TABLE fact_job_postings AS
SELECT 
    job_id,
    employer_id,
    posted_date_id,
    role_title,
    seniority_level,
    industry_category,
    remote_modality,
    required_skills,
    min_years_experience,
    base_salary_min,
    base_salary_max,
    target_time_to_fill_days,
    actual_time_to_fill_days,
    is_closed
FROM read_parquet('data/raw/fact_job_postings.parquet');

-- Fact Applications (Enriched with Vectorized Matching & 3-Band Triage)
CREATE OR REPLACE TABLE fact_applications AS
SELECT 
    application_id,
    candidate_id,
    job_id,
    employer_id,
    channel_id,
    application_date_id,
    candidate_skills,
    job_required_skills,
    candidate_experience_years,
    job_min_experience_years,
    candidate_salary_expectation,
    job_salary_max,
    is_adversarial_injection,
    hard_skills_jaccard,
    semantic_cosine_sim,
    experience_penalty,
    composite_match_score,
    triage_category,
    triage_reason,
    current_funnel_stage,
    is_interviewed,
    is_offered,
    is_hired
FROM read_parquet('data/processed/fact_applications.parquet');
