# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 20:33:21 2020

@author: framo
"""

gameslist = ["Dark souls","Nier automata","God of war","Red Dead Redemption 2",
         "Red dead Redemption","Assassins creed 2","Assassins creed 3", 
         "Assassins creed origins","Last of us","Last of us 2","the legend of Zelda twilight princess",
         "the legend of Zelda skyward sword","Massive effect 3" ,"Tomb raider","Shadow of Tomb Raider",
         "Rise of Tomb Raider","Uncharted","Destiny","Destiny 2", "The division 2",
         "Hellblade","Horizons zero dawn","Far cry 3", "control","Batman: Arkham Asylum",
         "Batman Arkham Knight","Batman Arkham City", "Nino kuni","The Witcher 3",
         "Persona 5","star wars Knights of old republic","Gris","Spider Man","Dead Cells","Minecraft",
         "Children of morta","Gears of war","Shadows tactics","Metro redux","Metro redux last light"]

psExclusive = [0,0,1,1,2,0,0,0,1,1,4,4,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0]
psExclusive = ["pc" if i == 0 else i for i in psExclusive]
psExclusive = ["ps4" if i == 1 else i for i in psExclusive]
psExclusive = ["wii" if i == 4 else i for i in psExclusive]
psExclusive = ["ps3" if i == 2 else i for i in psExclusive]

# tres pasos:
#   buscar en how long to beat
#   buscar en metacritic
#   crear lista


from bs4 import BeautifulSoup
import requests


# how long to beat
        
from howlongtobeatpy import HowLongToBeat

def howlongExtractor(game):
    results_list = HowLongToBeat().search(game)
    if results_list is not None and len(results_list) > 0:
        best_element = max(results_list, key=lambda element: element.similarity)
        return best_element
    else:
        return "not found"

timeToBeat = []
for i in gameslist:
    print(i)
    dt = howlongExtractor(i)
    if isinstance(dt, str):
        timeToBeat.append("not found")
    else:
        timeToBeat.append(dt.gameplay_main)

# Metacritic

url = "https://www.metacritic.com/game/"
headers = {'User-Agent': 'Mozilla/5.0'}

criticScore = []
publicScore = []

for j in range(0,len(gameslist)):
    print(gameslist[j])
    jtx = gameslist[j].replace(" ","-").lower()
    furl = url + psExclusive[j] + "/" +jtx
    response = requests.get(furl, headers=headers)
    if response.status_code == 404:
        print("error 404")
        jtx = gameslist[j].replace(" ","%20")
        furl = 'https://www.metacritic.com/search/game/' + jtx + '/results'
        response = requests.get(furl, headers=headers)
        soup = BeautifulSoup(response, "html.parser")
        path = soup.select('h3.product_title a')[0]['href']
        furl = 'https://www.metacritic.com/' + path
        response = requests.get(furl, headers=headers)
    soup = BeautifulSoup(response, "html.parser")
    critic = soup.select('a.metascore_anchor div span')[0].get_text()
    public = soup.select('a.metascore_anchor div')[1].get_text()
    criticScore.append(critic)
    publicScore.append(public)


import pandas as pd

df = pd.DataFrame(gameslist, timeToBeat, criticScore,publicScore)
df.to_csv('games.csv', encoding='utf-8')