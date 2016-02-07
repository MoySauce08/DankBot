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
