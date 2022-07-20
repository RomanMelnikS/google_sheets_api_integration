from django.shortcuts import render
from google_sheets_service.models import Google_Sheets_Table
from google_sheets_service.tasks import update_table_task


def index(request):
    update_table_task.delay()
    table = Google_Sheets_Table.objects.all()
    return render(
        request, 'index.html', {'table': table}
    )
