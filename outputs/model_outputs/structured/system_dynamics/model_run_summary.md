# Structured SyD -- Model Run Summary

**Run date:** 2026-08-03
**Notebook:** notebooks/68_structured_system_dynamics.ipynb
**Blueprint:** outputs/reports/structured/structured_syd_blueprint.md

## Eligibility
- SyD-eligible (>= 4 weeks): 47/61 (77.0%)

## Backlog stock summary (eligible, N=47)
       backlog_mean  backlog_peak  backlog_trend_slope  backlog_trend_slope_trimmed
count        47.000        47.000               47.000                       47.000
mean         32.112        57.745                2.950                        2.924
std          40.997        74.292                3.714                        3.888
min           0.381         2.000                0.014                       -0.000
25%           6.062        11.500                0.469                        0.329
50%          15.750        31.000                1.719                        1.524
75%          43.246        63.000                3.200                        3.383
max         192.095       352.000               17.036                       17.202

## Right-censoring sensitivity check
Sign agreement between raw and final-week-trimmed backlog_trend_slope: 44/47 (93.6%)
-- high agreement means the positive trend is a genuine structural finding (driven by the 26.8%% of
non-censored tasks that never resolve within the window), not primarily a right-censoring artifact of
the final week alone.

## Dominant loop label distribution
dominant_loop_label
overload-trending      16
productive-trending    16
balanced               15
NaN                    14

## Feedback-loop tests (pooled, population-level; predicted sign stated in advance)
 loop_name                 X                              Y  pearson_r  pearson_r_within  p_value   n predicted_sign
productive completed_count_w            created_count_{w+1}     0.9456            0.1182      0.0 735       positive
  overload         Backlog_w            created_count_{w+1}     0.4185           -0.1794      0.0 735       negative
 balancing         Backlog_w reschedule_count_w (same week)     0.4659           -0.1083      0.0 792       positive
-- pearson_r = pooled (conflates between-participant volume differences with within-week timing)
-- pearson_r_within = person-mean-centered, isolates genuine week-to-week coupling (see notebook 10b)

## Left-censoring caveat
Backlog_w is computed from non-censored tasks only and initialized at 0 per participant's own week 0 --
likely an UNDERCOUNT of true backlog, especially early in each participant's observed window, since
60.7%% of all tasks are left-censored (pre-existed the window).
