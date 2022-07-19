from django.db import models

class Google_Sheets_Table(models.Model):
    number = models.IntegerField(primary_key=True)
    order_number = models.IntegerField()
    dollar_price = models.IntegerField()
    delivery_time = models.DateField()
    rub_price = models.IntegerField()

    def __str__(self):
        return f'Заказы'
