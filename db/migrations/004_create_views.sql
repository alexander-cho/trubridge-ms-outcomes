CREATE MATERIALIZED VIEW tract_health_outcomes
AS
(
SELECT census_tract_id,
       MAX(county_name)                                                                       AS county_name,
       MAX(CASE
               WHEN measure = 'Frequent mental distress among adults'
                   THEN data_value / 100 END)                                                 AS frequent_mental_distress,
       MAX(CASE
               WHEN measure = 'Frequent physical distress among adults'
                   THEN data_value / 100 END)                                                 AS frequent_physical_distress,
       MAX(CASE
               WHEN measure = 'Visits to doctor for routine checkup within the past year among adults'
                   THEN (1 - data_value / 100) END)                                           AS no_doctor_visit_routine_checkup_past_year,
       MAX(CASE WHEN measure = 'Mobility disability among adults' THEN data_value / 100 END)  AS mobility_disability,
       MAX(CASE WHEN measure = 'Cognitive disability among adults' THEN data_value / 100 END) AS cognitive_disability,
       MAX(CASE WHEN measure = 'Diagnosed diabetes among adults' THEN data_value / 100 END)   AS diabetes,
       MAX(CASE
               WHEN measure = 'Food insecurity in the past 12 months among adults'
                   THEN data_value / 100 END)                                                 AS food_insecurity_past_year,
       MAX(CASE WHEN measure = 'Depression among adults' THEN data_value / 100 END)           AS depression
FROM public.health_outcomes
WHERE state_abbr = 'MS'
GROUP BY census_tract_id
    )
WITH NO DATA;



CREATE MATERIALIZED VIEW tract_analytics
AS
(
SELECT t1.*,
       t2.tract_name,
       (t2.total_population_uninsured::float / NULLIF(t2.total_population::float, 0))           AS uninsured,
       (t3.total_households_no_internet_access::float / NULLIF(t3.total_households::float, 0))  AS no_internet_access,
       (t4.total_population_below_poverty_level::float / NULLIF(t4.total_population::float, 0)) AS below_poverty,
       (t5.total_households_no_vehicle::float / NULLIF(t5.total_households::float, 0))          AS no_vehicle
FROM public.tract_health_outcomes t1
         JOIN public.health_insurance t2 ON t1.census_tract_id = t2.tract_id
         JOIN public.internet_subscriptions t3 ON t1.census_tract_id = t3.tract_id
         JOIN public.poverty t4 ON t1.census_tract_id = t4.tract_id
         JOIN public.vehicles_available t5 ON t1.census_tract_id = t5.tract_id
    )
WITH NO DATA;