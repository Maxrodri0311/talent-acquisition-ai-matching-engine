-- ============================================================================
-- TALENT ACQUISITION FUNNEL ANALYTICS & RECRUITER INTELLIGENCE (ADVANCED SQL)
-- Demonstrates CTEs, Window Functions, Funnel Stage Drop-offs & Yield Ratios
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. EXECUTIVE APPLICATION FUNNEL STAGE CONVERSION (WITH DROP-OFF RATES)
-- ----------------------------------------------------------------------------
WITH FunnelStageCounts AS (
    SELECT 
        COUNT(*) AS total_applications,
        SUM(CASE WHEN triage_category IN ('DIRECT_APPLICABLE', 'HUMAN_REVIEW_FLAGGED') THEN 1 ELSE 0 END) AS passed_initial_triage,
        SUM(is_interviewed) AS total_interviews,
        SUM(is_offered) AS total_offers,
        SUM(is_hired) AS total_hires
    FROM fact_applications
)
SELECT 
    '1. Total Applications' AS stage_name,
    total_applications AS candidate_volume,
    100.0 AS stage_conversion_pct,
    0.0 AS drop_off_pct
FROM FunnelStageCounts

UNION ALL

SELECT 
    '2. Qualified for Review (Triage Passed)',
    passed_initial_triage,
    ROUND((passed_initial_triage * 100.0) / NULLIF(total_applications, 0), 2),
    ROUND(((total_applications - passed_initial_triage) * 100.0) / NULLIF(total_applications, 0), 2)
FROM FunnelStageCounts

UNION ALL

SELECT 
    '3. Technical Interviews Conducted',
    total_interviews,
    ROUND((total_interviews * 100.0) / NULLIF(passed_initial_triage, 0), 2),
    ROUND(((passed_initial_triage - total_interviews) * 100.0) / NULLIF(passed_initial_triage, 0), 2)
FROM FunnelStageCounts

UNION ALL

SELECT 
    '4. Job Offers Extended',
    total_offers,
    ROUND((total_offers * 100.0) / NULLIF(total_interviews, 0), 2),
    ROUND(((total_interviews - total_offers) * 100.0) / NULLIF(total_interviews, 0), 2)
FROM FunnelStageCounts

UNION ALL

SELECT 
    '5. Placements / Final Hires',
    total_hires,
    ROUND((total_hires * 100.0) / NULLIF(total_offers, 0), 2),
    ROUND(((total_offers - total_hires) * 100.0) / NULLIF(total_offers, 0), 2)
FROM FunnelStageCounts;


-- ----------------------------------------------------------------------------
-- 2. RECRUITMENT SOURCING CHANNEL EFFICIENCY & COST-PER-HIRE
-- ----------------------------------------------------------------------------
SELECT 
    c.channel_name,
    c.channel_type,
    COUNT(a.application_id) AS total_candidates,
    SUM(a.is_interviewed) AS interview_count,
    SUM(a.is_hired) AS hire_count,
    ROUND(AVG(a.composite_match_score), 2) AS avg_match_score,
    ROUND((SUM(a.is_hired) * 100.0) / NULLIF(COUNT(a.application_id), 0), 2) AS channel_hire_yield_pct,
    ROUND(SUM(c.cost_per_posting) / NULLIF(SUM(a.is_hired), 0), 2) AS estimated_cost_per_hire_usd,
    DENSE_RANK() OVER (ORDER BY SUM(a.is_hired) DESC) AS channel_rank_by_volume
FROM fact_applications a
JOIN dim_channels c ON a.channel_id = c.channel_id
GROUP BY c.channel_name, c.channel_type
ORDER BY hire_count DESC;


-- ----------------------------------------------------------------------------
-- 3. EMPLOYER HIRING VELOCITY & TIME-TO-FILL (TTF) PERFORMANCE
-- ----------------------------------------------------------------------------
SELECT 
    e.employer_name,
    e.company_tier,
    e.industry,
    COUNT(j.job_id) AS total_requisitions,
    ROUND(AVG(j.target_time_to_fill_days), 1) AS target_ttf_avg_days,
    ROUND(AVG(j.actual_time_to_fill_days), 1) AS actual_ttf_avg_days,
    ROUND(AVG(j.actual_time_to_fill_days - j.target_time_to_fill_days), 1) AS ttf_variance_days,
    ROUND(AVG(j.base_salary_max), 2) AS avg_offered_salary_usd
FROM fact_job_postings j
JOIN dim_employers e ON j.employer_id = e.employer_id
GROUP BY e.employer_name, e.company_tier, e.industry
ORDER BY total_requisitions DESC;
