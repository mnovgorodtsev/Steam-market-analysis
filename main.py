import requests
import re
import json
from bs4 import BeautifulSoup
test_url='https://steamcommunity.com/market/listings/730/London%202018%20Legends%20Autograph%20Capsule'


r = requests.get(test_url).text
soup = BeautifulSoup(r,'html.parser')
all_scripts=soup.find_all("script",type='text/javascript')

data=str(all_scripts[len(all_scripts)-1])
#print(data)

pattern = r'var line1=\[(.*?)\];'
match = re.search(pattern, data)

found_text = match.group(1)
print(found_text)


