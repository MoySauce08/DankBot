# coding: utf-8

import discord
import json
import requests
import urllib2
import sys
import csv
from bs4 import BeautifulSoup
from tabulate import tabulate
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError

#user imports
import Dota
import Fun

client = discord.Client()
client.login('moybot@hotmail.com', 'password')
steamKey = '6CBA26B8D032A74753AFDC81584E3245'
session = requests.Session()
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

dota_players = []

f = open("dota_players.txt", 'r')
for line in f:
    player = line.split(',')
    counter = 0
    for value in player:
        value = value.replace("\n", "")
        player[counter] = value.lower()
        counter += 1
    dota_players.extend(player)
f.close()

"""
    To use DotaBuff as an API, request the webpage and parse through the raw HTML.
    Use https://github.com/Gravestorm/Gravebot/blob/master/lib/dota2.js as a resource.
    Ctrl+F class="sortable" for best lane heroes
    My Match History: https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?account_id=76561198044120256&format=xml&key=6CBA26B8D032A74753AFDC81584E3245
    Specific Match Details: https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?match_id=2079182171&format=xml&key=6CBA26B8D032A74753AFDC81584E3245
    I can probably get the above two things through dotabuff, and that's what I'll probably do.
"""

@client.event
def on_message(message):
    global dota_players

    # Everyone's commands
    words = message.content.lower()
    if (words.startswith('!')):
        print words
    	word = words.split()
    	if word[0] == '!lenny':
            client.send_message(message.channel, '( ͡° ͜ʖ ͡°)')

        elif word[0] == '!dickbutt':
            client.send_message(message.channel, '░░░░░░░░░░░░░░░░░░░░░\n░░░░░░░░░░░░▄▀▀▀▀▄░░░\n░░░░░░░░░░▄▀░░▄░▄░█░░\n░▄▄░░░░░▄▀░░░░▄▄▄▄█░░\n█░░▀▄░▄▀░░░░░░░░░░█░░\n░▀▄░░▀▄░░░░█░░░░░░█░░\n░░░▀▄░░▀░░░█░░░░░░█░░\n░░░▄▀░░░░░░█░░░░▄▀░░░\n░░░▀▄▀▄▄▀░░█▀░▄▀░░░░░\n░░░░░░░░█▀▀█▀▀░░░░░░░\n░░░░░░░░▀▀░▀▀░░░░░░░░')

        elif word[0] == '!dota':
            if word[1] == 'stats':
                player = ''
                if len(word) > 3:
                    for i in range(2, len(word)):
                        player += word[i]
                        if i != len(word)-1:
                            player += ' '
                else:
                    player = word[2]
                response = Dota.dotastats(player, dota_players)
            elif word[1] == 'counter':
                hero = ''
                if len(word) > 3:
                    for i in range(2, len(word)):
                        hero += word[i]
                        if i != len(word)-1:
                            hero += '-'
                else:
                    hero = word[2]
                hero = hero.lower()
                response = Dota.dotaCounter(hero)
            client.send_message(message.channel, response)

        elif word[0] == '!add':
            if word[1] == 'dotaplayer':
                if len(word) == 4:
                    dota_players = Dota.addDotaPlayer(word[2], word[3], dota_players)
                else:
                    client.send_message(message.channel, "ERROR: Incorrect usage.\n\t!add dotaplayer $playername $dotabuff_player_ID")

        elif word[0] == '!help':
            counter = 0
            players = ''
            for player in dota_players:
                if counter % 2 == 0:
                    players += player + '\n\t'
                counter += 1
            client.send_message(message.channel, """Current commands:\n\t- !lenny\n\t- !dickbutt\n\t- !dota stats $player\n\t- !dota counter $hero\n\t- !add dotaplayer $username $dotabuff_player_ID\n\t- !wiki $wikiSearchWord(s)
\t- !urban $word(s)\n\t- !report @user
Dota players included:""" + '\n\t' + players)

        elif word[0] == '!wiki':
            searchWord = ''
            if len(word) > 2:
                for i in range(1, len(word)):
                    searchWord += word[i]
                    if i != len(word)-1:
                        searchWord += '_'
            else:
                searchWord = word[1]
            client.send_message(message.channel, Fun.wikiSearch(searchWord))

        elif word[0] == '!urban':
            define = ''
            if len(word) > 2:
                for i in range(1, len(word)):
                    define += word[i]
                    if i != len(word)-1:
                        define += ' '
            else:
                define = word[1]
            client.send_message(message.channel, Fun.urbanSearch(define).encode('utf-8'))

        elif word[0] == '!report':
            reported = ''
            if len(word) > 2:
                for i in range(1, len(word)):
                    reported += word[i]
            else:
                reported = word[1]
            reportedAlt = reported[2:len(reported)-1]

            f = open(message.server.name + ' reports.txt', 'r')
            user_array = {}

            for line in f:
                line = line.decode('utf-8')
                line = line.split(',')
                user_array[line[1]] = [line[0],line[2].rstrip('\n')]
            f.close()
            #print 'Reported: ' + user_array[reportedAlt][0]
            if reportedAlt in user_array:
                user_array[reportedAlt][1] = int(user_array[reportedAlt][1]) + 1
                f = open(message.server.name + ' reports.txt', 'wb')
                for key, value in user_array.items():
                    f.write(value[0].encode('utf-8') + ',' + key.encode('utf-8') + ',' + str(value[1]) + '\n')
                client.send_message(message.channel, 'Reported ' + user_array[reportedAlt][0].encode('utf-8') + '. Current Reports: ' + str(user_array[reportedAlt][1]))
                f.close()
            else:
                client.send_message(message.channel, reported + ' does not exist as a user in this server.')

    	#baseURL = https://api.steampowered.com/IDOTA2Match_570/
    	# Calum's commands
    	#if message.author.name == '1nsayn':
    	# Steam ID: 76561198066749272

    	# Tibor's commands
    	#if message.author.name == 'robit':
    	# Steam ID: 76561197996963851

    	# Michael's commands
    	#if message.author.name == 'Lekcian':
    	# Steam ID: 76561197991432811

    	if message.author.name == 'MoySauce':
    		if message.content == '!logout':
    			client.send_message(message.channel, 'Bot has logged out')
    			client.logout()

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for server in client.servers:
        user_array = {}
        members = server.members
        f = open(server.name + ' reports.txt', 'a+')
        for line in f:
            line = line.split(',')
            user_array[line[1]] = [line[0],line[2].rstrip('\n')]
        for user in members:
            if user.id not in user_array:
                uni = user.name + ',' + user.id + ',0\n'
                f.write(uni.encode('utf-8'))
                user_array[user.id] = [user.name, 0]
        f.close()
        print server.name

#			for channel in server.channels:
#				message_log_in(channel)
#				break

def message_log_in(channel):
    client.send_message(channel, 'The Bot has logged in')

client.run()
