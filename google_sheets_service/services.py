from __future__ import print_function

import datetime as dt
import logging
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
    """Получает таблицу из Google Sheets.

    Returns:
        table (dict): Таблица из из Google Sheets.
    """
    try:
        service = build('sheets', 'v4', developerKey=DEVELOPER_KEY)
        table = service.spreadsheets().values().get(
            spreadsheetId=TABLE_ID,
            range='A2:Z999'
        ).execute()
        return table
    except HttpError as err:
        logging.error(err, exc_info=True)


def get_valute_rate(current_date):
    """Парсер курса валюты с сайта ценробанка России.

    Args:
        current_date (str): Актуальная дата заказа.

    Vars:
        convert_date (str): Преобразованная в нужный вид дата.
        price_list (Response): Ответ с сайта центробанка с курсами валют.
        tree (Element): Обработанный price_list.
        valute_price (str): Курс указанной валюты, в данном случае рубля.

    Returns:
        valute_price (str): Актуальный курс на указанную дату.
    """
    try:
        convert_date = current_date.replace('.', '/')
        price_list = requests.get(f'{CBR_URL}{convert_date}', stream=True)
        tree = ET.fromstring(price_list.content)
        valute_price = tree.find(
            f'Valute[@ID={VALUTE_ID}]/Value'
        ).text.replace(',', '.')
        return valute_price
    except Exception as err:
        logging.error(err, exc_info=True)


def parse_table(table):
    """Разбирает полученную таблицу.
    Сравнивает данные из таблицы с базой данных, если данные есть в БД,
    но их нет в таблице, удаляет их из базы,
    иначе создаёт или обновляет объекты в базе данных.
    """
    orders = []
    for obj_id in Google_Sheets_Table.objects.values_list('number', flat=True):
        if obj_id not in table['values']:
            obj = Google_Sheets_Table.objects.get(number=obj_id)
            obj.delete()
    for order in table['values']:
        try:
            orders.append(
                Google_Sheets_Table(
                    number=int(order[0]),
                    order_number=int(order[1]),
                    dollar_price=int(order[2]),
                    delivery_time=dt.datetime.strptime(order[3], DATE_FORMAT).date(),
                    rub_price=float(order[2]) * float(get_valute_rate(order[3])),
                )
            )
        except Exception as err:
            logging.error(err, exc_info=True)
    Google_Sheets_Table.objects.bulk_create(orders, ignore_conflicts=True)
