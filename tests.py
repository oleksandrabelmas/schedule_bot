from bs4 import BeautifulSoup
import requests


link = 'https://docs.google.com/spreadsheets/d/1dYQlz8wP3he67hDlhjqk5KVDBuUTmKkXuSSvK6wx7XU/edit#gid=508591041'


def parser_func(sheet_link):
    r = requests.get(sheet_link)
    src = r.text

    soup = BeautifulSoup(src, 'lxml')

    sheet_name = soup.find('div', {'class': 'docs-sheet-tab-caption'}).text

    sheet_id = sheet_link.split('/')[5]

    print(sheet_name, sheet_id)


if __name__ == '__main__':
    parser_func(link)
