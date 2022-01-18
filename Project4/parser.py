import pandas as pd
import requests
from bs4 import (BeautifulSoup)

URL = 'https://code.s3.yandex.net/learning-materials/data-analyst/festival_news/index.html'
req = requests.get(URL)
soup = BeautifulSoup(req.text, 'lxml')
name_festivals = []
for row in soup.find_all(
    'tr'
):
    name_festivals.append(row.text)

name_festivals.pop(0)
size = len(name_festivals)
res = []
for i in range(size):
    z = name_festivals[i]
    z = z.split('\n')
    for j in z:
        if j == '':
            z.remove(j)
    res.append(z)
name = []
city = []
date = []
for i in range(len(res)):
    name.append(res[i][0])
    city.append(res[i][1])
    date.append(res[i][2])   
col = ['Название фестиваля', 'Место проведения', 'Дата проведения']
festivals = pd.DataFrame(columns=col)
festivals['Название фестиваля'] = name
festivals['Место проведения'] = city
festivals['Дата проведения'] = date
print(festivals)
