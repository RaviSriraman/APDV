import dagster as dg
from dagster import ScheduleDefinition

from .jobs import all_jobs, enterprises_etl_job

# update_all_schedule = dg.ScheduleDefinition(
#     job=all_jobs,
#     cron_schedule="* * * * *"
# )

enterprises_etl_job_schedule = ScheduleDefinition(
    job= enterprises_etl_job,
    cron_schedule="* * * * *"
)
