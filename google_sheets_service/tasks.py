from config.celery import app
from .script import parse_table, get_table


@app.task
def get_table_task():
    table = get_table()
    return table


@app.task
def update_table_task():
    parse_table(get_table_task())