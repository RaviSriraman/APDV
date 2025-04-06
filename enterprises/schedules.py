import dagster as dg
from .jobs import all_jobs

update_all_schedule = dg.ScheduleDefinition(
    job=all_jobs,
    cron_schedule="* * * * *"
)
