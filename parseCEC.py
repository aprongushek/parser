import requests
from bs4 import BeautifulSoup
import fake_useragent
import json
import csv
import time

request='http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ikTree&region=78&vrn=27820002070792'

session = requests.Session()
user = fake_useragent.UserAgent().random
header = {'user-agent': user}

page = session.get(request, headers=header, params='') 
json_ticks=page.json()[0]
children=json_ticks['children']

records = 0;
n = 1;
start = time.time()
print ('start writing data into EC.csv')
with open('EC.csv', 'w', newline='') as csvfile:
    fieldnames = ['ТИК №', 'УИК №', 'ФИО', 'Статус', 'Кем предложен в состав комиссии']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
    writer.writeheader() 
    for item in children:
        # print(item['text'])
        r=session.get(f"http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ikTree&region=78&vrn={item['id']}&onlyChildren=true", headers=header, params='')
        json_uiks=r.json()
        for uik in json_uiks:
            # print(uik['text'])
            page_uik=session.get(f"http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ik&vrn={uik['id']}", headers=header).content
            soup=BeautifulSoup(page_uik, 'lxml')
            table = soup.select_one(".table.margtab table")
            rows = table.find_all("tr")
            for i in [1, len(rows)-1]:
                tik_n = item['text'][item['text'].find('№')+2:]
                uik_n = uik['text'][uik['text'].find('№')+1:]
                fio = rows[i].select_one("td > nobr").text
                status = rows[i].select_one("td:nth-of-type(3)").text
                party = rows[i].select_one("td:nth-of-type(4)").text
                # print (tik_n + '|' + uik_n + '|' + fio + '|' + status + '|' + party)
                writer.writerow({'ТИК №': tik_n, 'УИК №': uik_n, 'ФИО': fio, 'Статус': status, 'Кем предложен в состав комиссии': party})
                records += 1
                if time.time()-start > 60*n:
                    n += 1
                    print ('---------------------------------------------')
                    print ('time spent: ' + str(time.time() - start) + 's')              
                    print ('records writed: ' + str(records))

print ('---------------------------------------------')
print ('wrighting data in EC.csv finished successfully')
print ('total time spent: ' + str(time.time() - start) + 's') 
print ('total records writed: ' + str(records))


