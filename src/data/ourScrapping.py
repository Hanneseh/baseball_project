#webscrape for honkbalsite 

import requests
from bs4 import BeautifulSoup 

url = 'https://www.honkbalsite.com/profhonkballers/'

headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers = headers)

#response status should be 200
response.status_code

soup = BeautifulSoup(response.content, 'html.parser')

stat_table = soup.find_all('table', class_ = 'tablepress tablepress-id-1')
#Checks how many table we found, should be 1
len(stat_table)

stat_table = stat_table[0]

for row in stat_table.find_all('tr'):
    for cell in row.find_all('td'):
        print(cell.text)

with open ('baseball_stats.txt', 'w') as r:
    for row in stat_table.find_all('tr'):
        for cell in row.find_all('td'):
            r.write(cell.text.ljust(25))
        r.write('\n')

1

#####koden####################Q#3#######################################################################################################
#OzzieA

import requests
from bs4 import BeautifulSoup 

url = 'https://www.baseball-reference.com/register/player.fcgi?id=albies000ozh'

headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers = headers)

#response status should be 200
response.status_code

soup = BeautifulSoup(response.content, 'html.parser')

stat_table = soup.find_all('table', class_ = 'sortable stats_table')
#Checks how many table we found, should be 1
len(stat_table)
print(stat_table)

stat_table = stat_table[0]

for row in stat_table.find_all('tr'):
    for cell in row.find_all('td'):
        print(cell.text)





with open ('baseball_stats.txt', 'w') as r:
    for row in stat_table.find_all('tr'):
        for cell in row.find_all('td'):
            r.write(cell.text.ljust(3))
        r.write('\n')




#Xander
import requests
from bs4 import BeautifulSoup 

url = 'https://www.baseball-reference.com/register/player.fcgi?id=bogaer001xan'

headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers = headers)

#response status should be 200
response.status_code

soup = BeautifulSoup(response.content, 'html.parser')

stat_tablex = soup.find_all('table', class_ = 'sortable stats_table')
#Checks how many table we found, should be 1
len(stat_tablex)
print(stat_tablex)

stat_tablex = stat_tablex[0]

for row in stat_tablex.find_all('tr'):
    for cell in row.find_all('td'):
        print(cell.text)



with open ('baseball_stats.txt', 'w') as r:
    for row in stat_tablex.find_all('tr'):
        for cell in row.find_all('td'):
            r.write(cell.text.ljust(25))
        r.write('\n')





#####koden####################Q#3#######################################################################################################


#year
import requests
from bs4 import BeautifulSoup 

url = 'https://www.baseball-reference.com/register/player.fcgi?id=albies000ozh'

headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers = headers)

#response status should be 200
response.status_code

soup = BeautifulSoup(response.content, 'html.parser')

stat_tableyear = soup.find_all('th')
#Checks how many table we found, should be 1
len(stat_tableyear)
print(stat_tableyear)

stat_tableyear = stat_tableyear[0]

for row in stat_tableyear.find_all('th'):
    for cell in row.find_all('data-stat'):
        print(cell.text)





with open ('baseball_stats.txt', 'w') as r:
    for row in stat_table.find_all('tr'):
        for cell in row.find_all('td'):
            r.write(cell.text.ljust(25))
        r.write('\n')



#####

#S script trying 


import requests
from bs4 import BeautifulSoup 

url = 'http://www.milb.com/player/index.jsp?sid=milb&player_id=642720#/career/R/hitting/2019/ALL'

headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers = headers)

#response status should be 200
response.status_code

soup = BeautifulSoup(response.content, 'html.parser')

stat_table = soup.find_all('table', class_ = "responsive-datatable")
#Checks how many table we found, should be 1
len(stat_table)

stat_table = stat_table[0]

for row in stat_table.find_all('tr'):
    for cell in row.find_all('td'):
        print(cell.text)

with open ('baseball_stats_ray.txt', 'w') as r:
    for row in stat_table.find_all('tr'):
        for cell in row.find_all('td'):
            r.write(cell.text.ljust(25))
        r.write('\n')


#webscrape for honkbalsite 

import requests
from bs4 import BeautifulSoup 

url = 'https://www.baseball-reference.com/register/player.fcgi?id=wiel--000zan'

headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers = headers)

#response status should be 200
response.status_code

soup = BeautifulSoup(response.content, 'html.parser')

stat_table = soup.find_all('table', class_ = 'overthrow table_container')
#Checks how many table we found, should be 1
len(stat_table)

stat_table = stat_table[0]

for row in stat_table.find_all('tr'):
    for cell in row.find_all('td'):
        print(cell.text)

with open ('baseball_stats.txt', 'w') as r:
    for row in stat_table.find_all('tr'):
        for cell in row.find_all('td'):
            r.write(cell.text.ljust(25))
        r.write('\n')


