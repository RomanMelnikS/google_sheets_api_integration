from __future__ import print_function

import datetime as dt
import os
from xml.etree import ElementTree as ET

import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_sheets_service.models import Google_Sheets_Table

TABLE_ID = os.environ['TABLE_ID']

DEVELOPER_KEY = os.environ['DEVELOPER_KEY']

DATE_FORMAT = '%d.%m.%Y'

VALUTE_ID = '"R01235"'

CBR_URL = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='


def get_table():
    try:
        service = build('sheets', 'v4', developerKey=DEVELOPER_KEY)
        table = service.spreadsheets().values().get(
            spreadsheetId=TABLE_ID, range='A2:Z999'
        ).execute()
        return table
    except HttpError as err:
        print(err)


def parse_table(table):
    for order in table['values']:
        date = dt.datetime.strptime(
            order[3], DATE_FORMAT
        ).date()
        convert_date = str(order[3]).replace('.', '/')
        price = requests.get(f'{CBR_URL}{convert_date}', stream=True)
        tree = ET.fromstring(price.content)
        valute_price = tree.find(
            f'Valute[@ID={VALUTE_ID}]/Value'
        ).text.replace(',', '.')
        Google_Sheets_Table.objects.update_or_create(
            number=order[0],
            defaults={
                'number': order[0],
                'order_number': order[1],
                'dollar_price': order[2],
                'delivery_time': date,
                'rub_price': float(order[2]) * float(valute_price),
            }
        )
    print('Worked')
