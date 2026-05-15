with touchpoints as (
    select * from {{ ref('stg_touchpoints') }}
),
journey_rollup as (
    select
        journey_id,
        any_value(account_name) as account_name,
        any_value(segment) as segment,
        min(touch_timestamp) as first_touch_at,
        max(touch_timestamp) as last_touch_at,
        count(*) as touch_count
    from touchpoints
    group by 1
)
select
    j.journey_id,
    j.account_name,
    j.segment,
    j.first_touch_at,
    j.last_touch_at,
    j.touch_count,
    c.conversion_type,
    c.pipeline_dollars,
    datediff(day, j.first_touch_at, c.converted_at) as days_to_convert
from journey_rollup j
join {{ source('revenue', 'conversions') }} c
  on j.journey_id = c.journey_id
