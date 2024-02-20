import requests
import re
import json
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


#test_url='https://steamcommunity.com/market/listings/730/London%202018%20Legends%20Autograph%20Capsule'
#test_url='https://steamcommunity.com/market/listings/730/Paris%202023%20Contenders%20Autograph%20Capsule'
#test_url='https://steamcommunity.com/market/listings/730/Rio%202022%20Challengers%20Autograph%20Capsule'
test_url='https://steamcommunity.com/market/listings/730/Rio%202022%20Contenders%20Sticker%20Capsule'
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
df.to_csv('Item_data', index=False)




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
            #print(month.text.strip(), avg_players.text.strip())
            row=(month.text.strip(), avg_players.text.strip())
            steamcharts_list.append(row)

    df = pd.DataFrame(steamcharts_list, columns=['Month', 'Players'])
    df['Players'] = df['Players'].astype(float)
    df['Players'] = (df['Players'] / 1000).round(2)
    df = df.tail(-1)
    df['Year'] = df['Month'].str.split().str[1]
    df['Month'] = df['Month'].str.split().str[0]
    df['Month'] = df['Month'].map(months_steamcharts)
    df_reversed = df.iloc[::-1].reset_index(drop=True)
    #print(df_reversed)
    return df_reversed



URL_steamcharts="https://steamcharts.com/app/730"
df=steamcharts_data(URL_steamcharts)
#print(df)
df.to_csv('Players_count', index=False)



def merging_data(item_csv, players_csv):
    item_df=pd.read_csv(item_csv)
    players_df=pd.read_csv(players_csv)

    sum_sold = sum((item_df['Quantity sold']))
    sum_sold_in_k=round(sum_sold/1000,2)
    start_month=item_df['Month'].iloc[0]
    start_year=item_df['Year'].iloc[0]
    first_index_row=players_df.loc[(players_df['Month']==start_month) & (players_df['Year']==start_year)]
    start_index = first_index_row.index[0]
    players_df = players_df.iloc[start_index:]

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('X')
    ax1.set_ylabel('Price', color=color)
    ax1.plot(item_df.index, item_df['Price'], color=color, label='Price')
    ax1.tick_params(axis='y', labelcolor=color)

    # Tworzenie drugiej osi Y
    ax2 = ax1.twinx()

    # Wykres dla ilości sprzedanych (Sell) ze skalą logarytmiczną na osi Y
    color = 'tab:blue'
    ax2.set_ylabel('Sell', color=color)
    ax2.plot(item_df.index, item_df['Quantity sold'], color=color, label='Sell')
    ax2.set_yscale('log')  # Ustawienie skali logarytmicznej na osi Y dla serii 'Sell'
    ax2.tick_params(axis='y', labelcolor=color)

    title='Sold: '+str(sum_sold_in_k)+'k'
    # Dodanie legendy
    fig.tight_layout()
    plt.legend()
    plt.suptitle(title, y=0.95)
    plt.show()

merging_data('Item_data','Players_count')
