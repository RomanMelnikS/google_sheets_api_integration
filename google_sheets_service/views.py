from django.shortcuts import render
from google_sheets_service.models import Google_Sheets_Table


def index(request):
    table = Google_Sheets_Table.objects.all()
    return render(
        request, 'index.html', {'table': table}
    )
