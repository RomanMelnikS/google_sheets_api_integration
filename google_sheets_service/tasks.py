from celery import shared_task

from google_sheets_service.services import get_table, parse_table


@shared_task
def update_table_task():
    parse_table(get_table())
