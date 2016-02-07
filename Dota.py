# coding: utf-8

import discord
import requests
import urllib2
import sys
from bs4 import BeautifulSoup
from tabulate import tabulate

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

def addDotaPlayer(player, playerID, dota_players):
    f = open('dota_players.txt', 'a')
    f.write(player+',')
    f.write(playerID+'\n')
    dota_players.extend([player, playerID])
    f.close()
    return dota_players

def dotastats(player, dota_players):
    finalResponse = ''
    baseURL = 'http://www.dotabuff.com'
    index = dota_players.index(player)
    playerID = dota_players[index+1]
    addURL = '/players/' + str(playerID)
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'User-Agent' : user_agent }
    req = urllib2.Request(baseURL+addURL, None, headers)
    response = urllib2.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    #index = html.find('<div class="header-content-secondary">')
    records = soup.find_all('span')
    test2 = 'Overall Record: '
    for record in records:
        attribs = record.attrs
        if 'class' in attribs:
            if attribs['class'] == ['game-record']:
                for child in record.children:
                    sys.stdout.write(child.string)
                    test2 += child.string
                sys.stdout.write('\n')
                test2 += '\n'
                finalResposne = test2
    statGroup = soup.find('article')
    heroes = statGroup.find_all('a')
    table = list()
    info = list()
    for hero in heroes:
        attribs = hero.attrs
        if 'href' in attribs:
            if str(playerID) in attribs['href']:
                info.append(hero.text)
            else:
                continue
        divs = statGroup.find_all('div')
        for div in divs:
            if div['class'] == ['r-row']:
                children = div.children
                break
        for child in children:
            if 'r-20' in child['class']:
                moreChildren = child.children
                for otherChild in moreChildren:
                    if otherChild['class'] == ['r-body']:
                        if otherChild.text == None:
                            continue
                        #print otherChild.text
                        info.append(otherChild.text)
        #print info
        wins = str(int(round(float(info[1]) * float((float(info[2][:-1])/100)))))
        losses = str(int(info[1]) - int(wins))
        info.insert(2, wins+'-'+losses)
        table.append(info)
        div = div.next_sibling
        info = list()

        while div is not None:
            children = div.children
            hero = div.div.div.next_sibling.div.next_sibling.a
            info.append(hero.text)
            for child in children:
                if 'r-20' in child['class']:
                    moreChildren = child.children
                    for otherChild in moreChildren:
                        if otherChild['class'] == ['r-body']:
                            if otherChild.text == None:
                                continue
                            #print otherChild.text
                            info.append(otherChild.text)
            #print info
            wins = str(int(round(float(info[1]) * float((float(info[2][:-1])/100)))))
            losses = str(int(info[1]) - int(wins))
            info.insert(2, wins+'-'+losses)
            table.append(info)
            div = div.next_sibling
            info = list()
        break
    print tabulate(table, headers=['Hero','Matches Played','Win-Loss','Win Rate','KDA Ratio'])
    #            tabbed = max(len(word) for row in table for word in row) + 2
    #            test = ""
    #            for row in table:
    #                test += "".join(word.ljust(tabbed) for word in row)
    #                test += '\r\n'
    counter = 0
    for i in table:
        counter += 1
        finalResponse += str(ordinal(counter)) + ': ' + str(i[0]) + '\n'
        finalResponse += "Matches Played: {0:3}  |  Win-Loss: {1:7}  |  Win Rate: {2:6}  |  KDA: {3:5}\n\n".format(i[1],i[2],i[3],i[4])
    return finalResponse

def dotaCounter(hero):
    url = 'http://www.dotabuff.com/heroes/' + hero + '/matchups'
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'User-Agent' : user_agent }
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    records = soup.find_all('article')
    textResponse = ""
    significantValues = []
    counter = 0
    for record in records:
        tbody = record.find('tbody')
        for child in tbody.children:
            counter += 1
            first = True
            second = False
            tempValues = []
            for td in child.children:
                if first == True:
                    first = False
                    second = True
                elif second == True:
                    second = False
                    continue
                attribs = td.attrs
                tempValues.append(attribs['data-value'])
            significantValues.append(tempValues)
            if counter == 10:
                break
    finalResponse = ""
    if '-' in hero:
        hero = hero.replace('-', ' ')
    counter = 0
    for value in significantValues:
        counter += 1
        finalResponse += str(ordinal(counter)) + ': ' + str(value[0]) + '\n'
        finalResponse += "Advantage: {0:7}%  |  {1} Win Percentage: {2:7}%  |  Matches Played: {3:7}\n\n".format(value[1],hero.capitalize(),value[2],value[3])
    print tabulate(significantValues, headers=['Hero','Advantage','Win Percentage','Matches Played'])
    return finalResponse
