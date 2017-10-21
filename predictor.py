#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 23:18:05 2017

@author: Ray
"""

#Method 1: based on average PER of starting 5
# note: gives each starter same amt of min (36)

def predict_by_PER(PERs, opp_drtg):
    # league avg PER is set to 15. league avg team ppg was 105.8 in 2016-2017
    # Average the PERs (which is calculated by per min basis)
    # multiply the average by 36 (around how many min starters usually play)
    # divide by 5.104 so that 5 league avg players would score league avg 105.8 pts
    avg = 0
    for per in PERs:
        avg = avg + per
    avg = avg / 5
    avg = avg * 36
    avg = avg / 5.104
    # score is average btwn adjusted PER avg and the Def Rating of the opponent
    # def rtg adjusted for avg 96.4 possessions per game
    avg = (avg + opp_drtg * 0.964 )/2
    return avg