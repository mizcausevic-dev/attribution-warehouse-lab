with journeys as (
    select * from {{ ref('fct_attribution_journeys') }}
),
touchpoints as (
    select * from {{ ref('stg_touchpoints') }}
),
weighted_credit as (
    select
        t.journey_id,
        t.channel,
        case
            when t.stage = 'first_touch' then 0.40
            when t.stage = 'last_touch' then 0.40
            else 0.20 / nullif(j.touch_count - 2, 0)
        end as credit_share,
        t.touch_cost
    from touchpoints t
    join journeys j
      on t.journey_id = j.journey_id
)
select
    'position_weighted' as model_name,
    channel,
    sum(j.pipeline_dollars * w.credit_share) as allocated_pipeline,
    sum(w.touch_cost) as allocated_cost,
    sum(j.pipeline_dollars * w.credit_share) / nullif(sum(w.touch_cost), 0) as roi_ratio
from weighted_credit w
join journeys j
  on w.journey_id = j.journey_id
group by 1, 2
