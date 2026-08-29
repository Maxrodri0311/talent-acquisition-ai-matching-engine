-- ============================================================================
-- TABLEAU HYPER & LOOKER STUDIO ANALYTICAL VIEWS
-- Flat denormalized semantic representations for BI visualization tools
-- ============================================================================

CREATE OR REPLACE VIEW view_tableau_talent_funnel AS
SELECT 
    a.application_id,
    a.application_date_id,
    d.full_date AS application_date,
    d.year,
    d.quarter,
    d.month_name,
    c.candidate_id,
    c.anonymous_token,
    c.education_level,
    c.total_years_experience AS candidate_experience,
    c.primary_domain,
    c.location_region,
    c.demographic_group,
    j.job_id,
    j.role_title,
    j.seniority_level,
    j.remote_modality,
    j.min_years_experience AS job_min_experience,
    j.base_salary_min,
    j.base_salary_max,
    j.target_time_to_fill_days,
    j.actual_time_to_fill_days,
    e.employer_id,
    e.employer_name,
    e.company_tier,
    e.industry,
    ch.channel_name,
    ch.channel_type,
    a.composite_match_score,
    a.hard_skills_jaccard,
    a.semantic_cosine_sim,
    a.triage_category,
    a.triage_reason,
    a.current_funnel_stage,
    a.is_adversarial_injection,
    a.is_interviewed,
    a.is_offered,
    a.is_hired,
    a.candidate_salary_expectation
FROM fact_applications a
JOIN dim_date d ON a.application_date_id = d.date_id
JOIN dim_candidates c ON a.candidate_id = c.candidate_id
JOIN fact_job_postings j ON a.job_id = j.job_id
JOIN dim_employers e ON a.employer_id = e.employer_id
JOIN dim_channels ch ON a.channel_id = ch.channel_id;
