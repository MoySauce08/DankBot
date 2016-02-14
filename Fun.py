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
import random

reload(sys)
sys.setdefaultencoding('utf-8')

def wikiSearch(searchWord):
    try:
        summary = wikipedia.summary(searchWord)
        summary = summary[:2000]
        summary = summary.encode('utf-8')
    except DisambiguationError as e:
        summary = e
    except PageError:
        summary = "No wikipedia page exists"
    return summary

def urbanSearch(define):
    r = requests.Session()
    URL = 'http://api.urbandictionary.com/v0/define?term={0}'.format(define)
    response = r.get(URL)
    data = json.loads(response.text)
    if data['result_type'] == 'no_results':
        definition = '"' + define +'" is not defined'
    else:
        definition = data['list'][0]['definition']
        definition = define +': ' + definition
    return definition

def roll(n=None):
    if not n:
        n = 100
    else:
        n = int(n)
    return random.randint(0,n)

def cummies():
    x = "Just me and my 💕daddy💕, hanging out I got pretty hungry🍆 so I started to pout 😞 He asked if I was down ⬇for something yummy 😍🍆 and I asked what and he said he'd give me his 💦cummies!💦 Yeah! Yeah!💕💦 I drink them!💦 I slurp them!💦 I swallow them whole💦 😍 It makes 💘daddy💘 😊happy😊 so it's my only goal... 💕💦😫Harder daddy! Harder daddy! 😫💦💕 1 cummy💦, 2 cummy💦💦, 3 cummy💦💦💦, 4💦💦💦💦 I'm 💘daddy's💘 👑princess 👑but I'm also a whore! 💟 He makes me feel squishy💗!He makes me feel good💜! 💘💘💘He makes me feel everything a little should!~ 💘💘💘 👑💦💘Wa-What!💘💦👑".encode('utf-8')
    return x

def daddy():
    x = "IM DELETING YOU, DADDY!😭👋 ██]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]] 10% complete..... ████]]]]]]]]]]]]]]]]]]]]]]]]]]] 35% complete.... ███████]]]]]]]]]]]]]]]] 60% complete.... ███████████] 99% complete..... 🚫ERROR!🚫 💯True💯 Daddies are irreplaceable 💖I could never delete you Daddy!💖 Send this to ten other 👪Daddies👪 who give you 💦cummies💦 Or never get called ☁️squishy☁️ again❌❌😬😬❌❌ If you get 0 Back: no cummies for you 🚫🚫👿 3 back: you're squishy☁️💦 5 back: you're daddy's kitten😽👼💦".encode('utf-8')
    x = x.encode('utf-8')
    return x

def checkem():
    checkemPics = ["http://i.imgur.com/rRaG8in.png"]
    #output = ['',' Dubs!',' Trips!!',' QUADS!!!',' HOLY SHIT!!!!',' CHECKEM!! CHECKEM!! CHECKEM!!',' ASDFGHJKL WOOOOOOO! WOOOOOOOO! WOOOOOOO! WOOOOOO! RIC FLAIR, "WOOOOOOOOO!"']
    #outputNumber = ''
    #checkemList = [None] * 7
    #for i in range(0,7):
    #    if i == 0:
    #        checkemList[i] = random.randint(1,9)
    #    else:
    #        checkemList[i] = random.randint(0,9)
    #    outputNumber += str(checkemList[i])
    outputNumber = random.randint(1000000, 9999999)
    checkemList = map(int, str(outputNumber))
    counter = 0
    for i in range(6,-1,-1):
        first = checkemList[i]
        second = checkemList[i-1]
        if first == second:
            counter += 1
        else:
            break
    if counter > 0:
        return checkemPics[0]+'                                      '+str(outputNumber)
    else:
        return str(outputNumber)

def rps(firstPlayer, secondPlayer):
    
