from django.contrib import admin

from google_sheets_service.models import Google_Sheets_Table


@admin.register(Google_Sheets_Table)
class GoogleSheetsAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'order_number',
        'dollar_price',
        'delivery_time',
        'rub_price'
    )
