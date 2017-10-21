#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 23:45:10 2017

@author: Ray
"""

from getStats import get_stats
from urlfinder import find_url
from predictor import predict_by_PER
from random import random


def main():

    print ("Welcome to Raymond Kwan's NBA game simulator!")
    print ("Pick any 5 current players on to be on each team, and see how these hypothetical teams match up in a simulated game.")

    urls = {}
    urls['team1'] = []
    urls['team2'] = []

    for t in range (1,3):
        p = 1
        while p < 6:
            player = input("(TEAM %s) Player %s: " %(t,p))
            print ("Gathering data on " + player + "...")
            url = find_url(player)
            if len(url) == 0:
                print ("Player not found (player must be current and capitalized correctly). Try again.")
            else:
                p += 1
                if t == 1:
                    urls['team1'].append(url[0])
                if t == 2:
                    urls['team2'].append(url[0])
            url.clear
    
    team1pers = []
    team2pers = []
    team1_DRtg = 0
    team2_DRtg = 0
    print ('Simulating Game...')
    for plyr in urls['team1']:
        d = get_stats(plyr, 'adv')
        print ('..')
        if 'PER' in d:
            team1pers.append( d['PER'] )
        if 'DRtg' in d:
            team1_DRtg += d['DRtg']
        d.clear
    team1_DRtg = team1_DRtg / 5
    for plyr in urls['team2']:
        d = get_stats(plyr, 'adv')
        print ('...')
        if 'PER' in d:
            team2pers.append( d['PER'] )
        if 'DRtg' in d:
            team2_DRtg += d['DRtg']
        d.clear
    team2_DRtg = team2_DRtg / 5
    # future feature: follow game action, or update quarter scores
    team1score = int(round(predict_by_PER(team1pers, team2_DRtg)))
    team2score = int(round(predict_by_PER(team2pers, team1_DRtg)))
    
    winner = 0
    if team1score > team2score:
        winner = 1
    elif team2score > team1score:
        winner = 2
    else:  # if it's a tie, by luck/random add a point to one team
        tiebreaker = random()
        if tiebreaker == 0:
            team1score += 1
            winner = 1
        else:
            team2score += 1
            winner = 2
    print ('Final Score')
    print('-------------')
    print('Team 1: {}'.format(team1score))
    print('Team 2: {}'.format(team2score))
    print('...TEAM {} WINS!'.format(winner))
    
    return 0
        

if __name__ == "__main__":
    main()
    
