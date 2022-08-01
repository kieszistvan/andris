import datetime
import pandas as pd # pip install pandas
import requests # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4


def scrape():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    }
    url = 'https://www.marketwatch.com/tools/earningscalendar'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    earning_tables = soup.select(".j-tabPanes > .element")

    dfs = {}
    current_datetime = datetime.datetime.now().strftime('%d-%m-%y-%H-%M-%S')
    xlsxwriter = pd.ExcelWriter('Earning Calendar ({0}).xlsx'.format(current_datetime))

    for earning_table in earning_tables:
        if not 'Sorry, this date currently does not have any earnings announcements scheduled' in earning_table.text:
            earning_date = earning_table['data-tab-pane'].replace("/", "-")
            dfs[earning_date] = pd.read_html(str(earning_table.table))[0]
            dfs[earning_date].to_excel(xlsxwriter, sheet_name=earning_date, index=False)

    xlsxwriter.save()
    print('earning tables Excel file exported')


if __name__ == '__main__':
    scrape()
