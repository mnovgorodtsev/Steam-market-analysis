import requests
import re
import json
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


test_url='https://steamcommunity.com/market/listings/730/London%202018%20Legends%20Autograph%20Capsule'

r = requests.get(test_url).text
soup = BeautifulSoup(r,'html.parser')
all_scripts=soup.find_all("script",type='text/javascript')

data=str(all_scripts[len(all_scripts)-1])

pattern = r'var line1=\[(.*?)\];'
match = re.search(pattern, data)

text = match.group(1)

months = {
    'Jan': 1, 'Feb': 2, 'Mar': 3,
    'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9,
    'Oct': 10, 'Nov': 11, 'Dec': 12
}

months_steamcharts = {
    'January': 1, 'February': 2, 'March': 3,
    'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9,
    'October': 10, 'November': 11, 'December': 12
}

data = eval(text)
df = pd.DataFrame(data, columns=['Date', 'Price', 'Quantity sold'])
df['Month']=df['Date'].str[0:3]
df['Year']=df['Date'].str[7:11]
df['Day'] = df['Date'].str[4:6]


df['Month']=df['Month'].map(months)
df['Day'] = df['Day'].astype(int)
df=df.drop(columns='Date')
print(df)


plt.plot(df['Price'])
plt.show()


def steamcharts_data(url):
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    table=soup.find('table',class_='common-table')
    rows=table.find_all('tr')

    steamcharts_list=[]
    for single_row in rows:
        avg_players=single_row.find('td',class_="right num-f italic")
        if avg_players is None:
            avg_players=single_row.find('td',class_='right num-f')

        month=single_row.find('td',class_='month-cell left italic')
        if month is None:
            month=single_row.find('td',class_='month-cell left')

        if(month is not None and avg_players is not None):
            print(month.text.strip(), avg_players.text.strip())
            row=(month.text.strip(), avg_players.text.strip())
            steamcharts_list.append(row)

    df = pd.DataFrame(steamcharts_list, columns=['Month', 'Players'])
    return df
URL="https://steamcharts.com/app/730"

df=steamcharts_data(URL)
print(df)