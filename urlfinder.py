#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 23:55:23 2017

@author: Ray
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def find_url(name):
    realgm = 'https://basketball.realgm.com/nba/players'
    
    page = urlopen(realgm)
    soup = BeautifulSoup(page, "lxml")
    prefix = 'https://basketball.realgm.com'
    l = []
    name = name.replace(' ', '-')
    
    link = soup.find_all(href=re.compile(name))
    if len(link)>0 and ( len(link[0]) > 0 ):
        l.append(prefix + link[0]['href'])
    
    #note: it would be more efficent to sort inputted 5 players first,
    #     search for the first player, then continue from that point to the next
    #     this would allow at most a search through the entire web page just once
    # return a list. if list is empty, player not found. 
    return l