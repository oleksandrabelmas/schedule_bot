import os.path
import time
import json

from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SHEET_ID = '165FEfvPuH9CfYK0qLp1Xa6o35aTW7WKdOmy5eqEvmWw'
SHEET_NAME = 'Розклад 20.02.2023 по 24.02.2023'


def get_data(sheet_id, sheet_name):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,
                                                                        scopes=SCOPES)

    SAMPLE_SPREADSHEET_ID = sheet_id
    SAMPLE_RANGE_NAME = sheet_name

    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    # Нам потрібний 4 строка і з 5 по 31
    values = result.get('values', [])

    # Розбираюсь із часом уроку
    list_hours = ['']

    for value in values[4]:
        try:
            # Тут блять пиздец індус. Відокремлюю години зі строки в читабельному форматі // Важливий лише початок уроку
            start_lesson = ':'.join(value.split(',')[2].split('-')[0].split('.')).strip()
            list_hours.append(start_lesson)
        # Сука тут вообще зайоб. Одна із назв уроку позначена не так як інші
        except:
            continue
    # збираю данні з гугл таблиці в json
    class_schedule = {}
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    for value in values[5::]:

        # вирішую проблему з бракуючими елементами
        if len(value) < 41:
            value.extend([''] * (41 - len(value)))

        c = 0
        lessons_list = []
        time_lesson = {}
        schedule_for_week = {}

        for i in range(1, len(value)):
            if i % 8 != 0:
                time_lesson[list_hours[i]] = value[i]
                lessons_list.append(time_lesson)
                time_lesson = {}
            else:
                time_lesson[list_hours[i]] = value[i]
                lessons_list.append(time_lesson)
                time_lesson = {}
                schedule_for_week[days[c]] = lessons_list
                class_schedule[value[0]] = schedule_for_week
                c += 1
                lessons_list = []

    with open('data.json', 'w') as f:
        f.write(json.dumps(class_schedule))


#def main():
#    get_data(SHEET_ID, SHEET_NAME)
#    while True:
#        remembering('data.json', '11-А')
#
#
#if __name__ == '__main__':
#    main()
