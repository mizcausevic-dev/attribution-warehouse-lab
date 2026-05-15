select
    journey_id,
    touch_timestamp,
    account_name,
    segment,
    channel,
    campaign,
    stage,
    touch_cost
from {{ source('marketing', 'touchpoints') }}
where touch_timestamp >= dateadd(day, -120, current_timestamp)
