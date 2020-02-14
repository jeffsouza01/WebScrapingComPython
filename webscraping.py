from lib2to3.pgen2 import driver

import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

    # Pegando conteúdo HTML a partir da URL
url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"
top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'}
}


def buildrank(type):

    field = rankings[type]['field']
    label = rankings[type]['label']

    driver.find_element_by_xpath(f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()

    element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")

    html_content = element.get_attribute('outerHTML')

    # Tratando o conteudo HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # Estruturar conteudo em um DataFrame - Pandas
    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['pos', 'Player', 'Team', 'Total']

    # Transformando os dados em um Dicionãrio de dados Próprio
    return df.to_dict('records')



option = Options()
option.headless = True
driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver')

driver.get(url)
driver.implicitly_wait(10)

for k in rankings:
    top10ranking[k] = buildrank(k)

driver.quit()


#Convertendo e salvando em um arquivo JSON
with open('ranking.json', 'w', encoding='utf-8') as jp:
    json = json.dumps(top10ranking, indent=4)
    jp.write(json)
