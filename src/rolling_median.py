# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import pandas as pd
import math as m
import matplotlib as plt
import datetime
import sys

#pre-deal with the data

inputDirect = str(sys.argv[1])

data = pd.read_csv(inputDirect, 
                   sep = '{"created_time": "|", "target": "|", "actor": "|"}', 
                   names = [0, 1, 2, 3, 4])
data = data[[1, 2, 3]][:]
data.columns = ["created_time", "target", "actor"]

#Dictionary timeTable: 
# key: created time in decreasing order
# value: a list of edges [a, b] made at the created time 

timeTable = {}

#Dictionary degreeTable:
# key: the name of each nodes
# value: degree of the node
# we can get the median of the graph by calculate median of degreeTable.values()

degreeTable = {}

#Open a output file

outputDirect = str(sys.argv[2])
file = open(outputDirect, 'w')

for i in range(len(data)):
    
    #get the creat time, target and actor of current line
    
    curTime = datetime.datetime.strptime(data["created_time"][i], "%Y-%m-%dT%H:%M:%SZ")
    target = data["target"][i]
    actor = data["actor"][i]
    
    #skip the line if there is no target or actor
    
    if pd.isnull(target) or pd.isnull(actor):
        continue;
    
    #Get the length of the timeTable
    
    l = len(timeTable)
    
    #if there is nothing in the timeTable, update timeTable and degreeTable

    if l == 0:
        timeTable[curTime] = []
        timeTable[curTime].append([target, actor])
        degreeTable[target] = 1
        degreeTable[actor] = 1
    
    #Otherwise    
        
    else:
        
        #if the time of current line is more than 60s smaller then the latest time
        #do not update any table, update the median
        
        if (timeTable.keys()[0] - curTime).total_seconds() > 60.0:
            file.write("%.2f\n" % np.median(degreeTable.values()))
            continue
            
        #else if the time of current line is earlier than the latest time
        #update the timeTable and degreeTable: 
        #delete items from the end of timeTable until the last item satisfies the time
        
        elif (curTime - timeTable.keys()[0]).total_seconds() > 0:
            timeTable[curTime] = []
            timeTable[curTime].append([target, actor])
            if target in degreeTable.keys():
                degreeTable[target] = degreeTable[target] + 1
            else:
                degreeTable[target] = 1
            if actor in degreeTable.keys():
                degreeTable[actor] = degreeTable[actor] + 1
            else:
                degreeTable[actor] = 1 
            while (curTime - timeTable.keys()[l - 1]).total_seconds() > 60.0:
                for pair in timeTable[timeTable.keys()[l-1]]:
                    degreeTable[pair[0]] -= 1
                    if degreeTable[pair[0]] == 0:
                        del degreeTable[pair[0]]
                    degreeTable[pair[1]] -= 1
                    if degreeTable[pair[1]] == 0:
                        del degreeTable[pair[1]]
                del timeTable[timeTable.keys()[l - 1]]
                l = l - 1           
        
        #The time of current line is in the middle,
        #update the timeTable and degreeTable
        
        else:
            if curTime in timeTable.keys():
                timeTable[curTime].append([target, actor])
            else:
                timeTable[curTime] = []
                timeTable[curTime].append([target, actor])
            if target in degreeTable.keys():
                degreeTable[target] = degreeTable[target] + 1
            else:
                degreeTable[target] = 1
            if actor in degreeTable.keys():
                degreeTable[actor] = degreeTable[actor] + 1
            else:
                degreeTable[actor] = 1 
    file.write("%.2f\n" % np.median(degreeTable.values()))

file.close()





