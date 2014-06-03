# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 11:43:47 2014

@author: Will McFadden (wmcfadden)
"""

import json
import numpy as np
import random as rand
import time
import datetime
import re
from copy import deepcopy as dc

import matplotlib.pyplot as plt

# this takes the 8 important offensive statistics and turns it directly into the baseline 
# probabilities of the standard game model
#def simple(p):
#    dt = 40./(p[1]+p[3]+p[8]+p[9]+p[11]+p[13]+p[18]+p[19])
#    p2 = p[1]/(p[1]+p[3]+p[8]+p[9])
#    p2m = p[0]/p[1]
#    p3 = p[3]/(p[3]+p[8]+p[9])
#    p3m = p[2]/p[3]
#    pf = p[9]/(p[8]+p[9])
#    pft = 0.475*p[5]/p[9]    
#    pftm = p[4]/p[5]
#    pr = p[6]/(p[1]-p[0]+p[3]-p[2]+0.525*(p[5]-p[4]))
#    return [dt, p2, p2m, p3, p3m, pf, pft, pftm, pr]
#
## this simulates each possession based on a set of probabilities passed in p
## it currently assumes no adjustment to score differential or time
#def pos(p, t, s):
#    dt = p[0]
#    p2 = p[1]
#    p2m = p[2]
#    p3 = p[3]
#    p3m = p[4]
#    pf = p[5]
#    pft = p[6]
#    pftm = p[7]
#    pr = p[8]
#    if rand.random() < p2:
#        if rand.random() < p2m:
#            return np.array([dt, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
#        elif rand.random() < pr:
#            return np.array([dt, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0])
#        else:
#            return np.array([dt, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0])
#    elif rand.random() < p3:
#        if rand.random() < p3m:
#            return np.array([dt, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
#        elif rand.random() < pr:
#            return np.array([dt, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0])
#        else:
#            return np.array([dt, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0])
#    elif rand.random() < pf:
#        if rand.random()<pft:
#            inc = 0
#            if rand.random() < pftm:        
#                inc = 1
#            if rand.random() < pftm:
#                return np.array([dt, 1, 0, 0, 0, 0, 1+inc, 2, 0, 0, 0, 1])
#            elif rand.random() < pr:
#                return np.array([dt, 0, 0, 0, 0, 0, inc, 2, 1, 0, 0, 1])
#            else:
#                return np.array([dt, 1, 0, 0, 0, 0, inc, 2, 0, 1, 0, 1])
#        else:
#            return np.array([dt, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
#    else:
#        return np.array([dt, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
#
## this runs a game and keeps track of stats using a pair of team offensive probabiliies
#def game(params):
#    team = 0;
#    time = 40;
#    dat = np.zeros((2,10))
#    while time>0:
#        other = int((team + 1)%2)
#        sco = dat[team,0]*2 + dat[team,2]*3 + dat[team,4] - dat[other,0]*2 - dat[other,2]*3 - dat[other,4]
#        new = pos(params[team],time,sco)
#        dat[team,:] = dat[team,:] + new[2:]
#        team = int((team + new[1])%2)
#        time = time - new[0]
#    return np.concatenate([dat[0],dat[1]])
#
#def avgstats(gm):
#    avg = np.zeros(20)
#    cnt = 0.;
#    for t2 in gm:
#        for agm in gm[t2]:
#            cnt = cnt + 1.
#            avg = avg + agm
#    return avg/cnt
#
#basefileD1 = "/Users/will/Desktop/tutorial/outputD1.json"
#basefileD2 = "/Users/will/Desktop/tutorial/outputD2.json"
#basefileD3 = "/Users/will/Desktop/tutorial/outputD3.json"
#basefileB = "/Users/will/Desktop/tutorial/bra.json"
#json_data=open(basefileD1)
#data1 = json.load(json_data)
#json_data.close()
#json_data=open(basefileD2)
#data2 = json.load(json_data)
#json_data.close()
#json_data=open(basefileD3)
#data3 = json.load(json_data)
#json_data.close()
#json_data=open(basefileB)
#dataB = json.load(json_data)
#json_data.close()
#names = {};
#idns = {};
#gms = {};
#games = {};
#data = data1+data2+data3
#for d in data:
#    s = d["value"]
#    if s:
#        nm = s[0][1]
#        idn = int(s[0][2].split("id=")[1])
#        if idn in names:
#            if nm not in names[idn]:
#                names[idn].append(nm);
#        else:
#            names[idn] = [nm]
#        if nm in idns:
#            if idn not in idns[nm]:
#                idns[nm].append(idn);
#        else:
#            idns[nm] = [idn]
#        
#        for i in range(1,len(s)):
#            g = s[i]
#            dt = g[0]
#            t1 = idn
#            t2 = int(g[2].split("id=")[1])
#            sload = [];
#            for j in range(5,len(g)):
#                if unicode.isalnum(g[j]):
#                    sload.append(float(re.sub('/','',g[j])))
#                else:
#                    sload.append(0)
#            stats = [sload[0]-sload[2],sload[1]-sload[3],sload[2],sload[3],sload[4],sload[5],sload[7],sload[8],sload[11],sload[14]]
#            if t1 in gms:
#                w = gms[t1]
#                if t2 in w:
#                    x = w[t2]
#                    if dt in x:
#                        x[dt] = stats+x[dt]
#                    else:
#                        x[dt] = stats
#                else:
#                    w[t2] = {dt:stats}
#            else:
#                gms[t1] = {t2:{dt:stats}}
#            if t2 in gms:
#                w = gms[t2]
#                if t1 in w:
#                    x = w[t1]
#                    if dt in x:
#                        x[dt] = x[dt]+stats
#                    else:
#                        x[dt] = stats
#                else:
#                    w[t1] = {dt:stats}
#            else:
#                gms[t2] = {t1:{dt:stats}}
#for t1 in gms:
#    for t2 in gms[t1]:
#        for dt in gms[t1][t2]:
#            if len(gms[t1][t2][dt])==20:
#                ins = gms[t1][t2][dt]
#                tmp = ins[7]
#                ins[7] = ins[17]
#                ins[17] = ins[7]
#                tmp = ins[9]
#                ins[9] = ins[19]
#                ins[19] = ins[9]
#                if(t1 in games):
#                    if t2 in games[t1]:
#                        games[t1][t2].append(np.array(ins))
#                    else:
#                        games[t1][t2] = [np.array(ins)]
#                else:
#                    games[t1] = {t2:[np.array(ins)]}


score = {};
for t1 in games:
    avg = 0.;
    cnt = 0.;
    for t2 in games[t1]:
        for p in games[t1][t2]:
            res = p[0]*2+p[2]*2+p[4]-(p[10]*2+p[12]*2+p[14])
            val = -1
            if res>0:
                val = 1
            avg = avg + val
            cnt = cnt + 1
    score[t1] = avg/cnt
trk = []
    
scorout = []
scorout.append(zip(*score.items())[1])
for t1 in games:
    avg = 0.;
    cnt = 0.;
#    for t2 in games[t1]:
#        for p in games[t1][t2]:
#            res = p[0]*2+p[2]*2+p[4]-(p[10]*2+p[12]*2+p[14])
#            val = -1
#            if res>0:
#                val = 1
#            avg = avg + val
#            cnt = cnt + 1
    score[t1] = rand.random()*2-1
jump= 0.5
scorout.append(zip(*score.items())[1])
for i in range(2000):
    oldscore = dc(score)
    for t1 in games:
        avg = 0.;
        cnt = 0.;
        for t2 in games[t1]:
            for p in games[t1][t2]:
                res = p[0]*2+p[2]*2+p[4]-(p[10]*2+p[12]*2+p[14])
                val = -1
                if res>0:
                    val = 1
                avg = avg + val*math.pow(1.5,3*oldscore[t2]) #this is the line where you use the prior score to weight each game
                cnt = cnt + 1
        score[t1] = avg/cnt + (rand.random()*2-1)*jump
    if i==500:
        scorout.append(zip(*score.items())[1])
    if i==1000:
        scorout.append(zip(*score.items())[1])
    if i==1500:
        scorout.append(zip(*score.items())[1])
    jump = jump*jump

scorout.append(zip(*score.items())[1])    
plot([x for y, x in sorted(zip(scorout[0], scorout[0]))],'.')  #this plots the original ranking
plot([x for y, x in sorted(zip(scorout[0], scorout[1]))],'.')  #this plots the corrected ranking
plot([x for y, x in sorted(zip(scorout[0], scorout[2]))],'.')  #this plots the corrected ranking
plot([x for y, x in sorted(zip(scorout[0], scorout[3]))],'.')  #this plots the corrected ranking
plot([x for y, x in sorted(zip(scorout[0], scorout[4]))],'.')  #this plots the corrected ranking
plot([x for y, x in sorted(zip(scorout[0], scorout[5]))],'.')  #this plots the corrected ranking

def matchup(team1, team2, games, idns, rank):
    t1 = idns[team1][0]
    t2 = idns[team2][0]
    play = []
    comp = []
    for t in games[t1]:
        if(t==t2):
            for p in games[t1][t2]:
                res = p[0]*2+p[2]*2+p[4]-(p[10]*2+p[12]*2+p[14])
                if res!=0:
                    if res>0 :
                        play.append('W')
                    else:
                        play.append('L')
        elif(t in games[t2]):
            t1r = []
            t2r = []
            for p in games[t1][t]:
                t1r.append(p[0]*2+p[2]*2+p[4]-(p[10]*2+p[12]*2+p[14]))
            for p in games[t2][t]:
                t2r.append(p[0]*2+p[2]*2+p[4]-(p[10]*2+p[12]*2+p[14]))
            comp.append([t1r, t2r])
    ret = {}
    ret['rnk']=[rank[t1],rank[t2]]   #return the rank of each
    ret['h2h']=play  #return any headto head matchups
    ret['gms']=comp #return any shared games
    return ret
    
matchup('VCU','StephenF.Austin',games,idns,score)
