import dagster as dg
from dagster import ScheduleDefinition

from .jobs import apdv_etl_job

enterprises_etl_job_schedule = ScheduleDefinition(
    job= apdv_etl_job,
    cron_schedule="* * * * *"
)
