import pandas as pd # pip install pandas
import requests # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4


def scrape(requested_date):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    }

    url = 'https://www.marketwatch.com/tools/earnings-calendar?requestedDate='+requested_date+'&partial=true'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    earning_tables = soup.select(".j-tabPanes > .element")

    dfs = {}
    xlsxwriter = pd.ExcelWriter('Earning Calendar ({0}).xlsx'.format(requested_date))

    for earning_table in earning_tables:
        if 'Sorry, this date currently does not have any earnings announcements scheduled' not in earning_table.text:
            earning_date = earning_table['data-tab-pane'].replace("/", "-")
            dfs[earning_date] = pd.read_html(str(earning_table.table))[0]
            dfs[earning_date].to_excel(xlsxwriter, sheet_name=earning_date, index=False)

    xlsxwriter.save()
    print('earning tables {0} Excel file exported'.format(requested_date))


if __name__ == '__main__':
    scrape('2022-08-01')
    scrape('2022-08-08')
    scrape('2022-08-15')
    scrape('2022-08-22')
