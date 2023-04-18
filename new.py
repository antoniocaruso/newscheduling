# Please add last date of edit or add to github repo
# Antonio - 18/04/2023

import numpy as np
import math
from collections import namedtuple

Task = namedtuple("Task","cost quality")

K = 24
MAX_TASK_QL = 10

B_INIT = 190
BMIN = 10
BMAX = 200


def print_info(Tasks):
    print("K = ",K," B = ",(BMIN,B_INIT,BMAX))
    print("-"*20)
    for i,t in enumerate(Tasks):
        print(i,"\t",t.cost,"\t",t.quality)
    print("-"*20)


def create_tasks(N = 10):
    c_i = [  1, 10, 15, 20, 25, 100, 105,110, 115,120]
    q_i = np.array([  0,  1, 2, 3, 4,  5,  6,  7,  8, 9 ])+1
    Tasks = []
    for x in zip(c_i,q_i):
        Tasks.append(Task(*x))
    return Tasks

# max_task_ql quality level

B = np.zeros((2,K*MAX_TASK_QL+1))
S = np.zeros((K,K*MAX_TASK_QL+1))


def check(K,S,Bstart,Bmin,Bmax,E,Tasks,debug=False):
    b = Bstart
    q = 0
    for i in range(K):
        bnew = min(b+E[i]-Tasks[S[i]].cost,Bmax)
        q += Tasks[S[i]].quality
        if debug: print("%2d :  %4d - %3d + %3d = %4d : %4d" %
        (S[i],b,Tasks[S[i]].cost,E[i],bnew,q))
        b = bnew
        if (b < Bmin): return 0
    if (b < Bstart):
        return 0
    return sum(Tasks[s].quality for s in S)

def ScheduleClassic(slots,Bstart,Bmin,Bmax,Eprod,Tasks):
    """
    slots = K = number of slots in a day
    Battery: Bmin < Bstart < Bmax 
    PanelProducton:  Eprod | len(Eprod) == slots
    Tasks: ordered from lowest cost,quality to greatest
    """
    # basic checks
    assert(len(Eprod) == slots)
    assert(Bmin < Bstart < Bmax)    
    M = np.zeros( (slots,Bmax+1), dtype=int)
    I = np.zeros( (slots,Bmax+1), dtype=int)
    for i in range(slots-1,-1,-1):
        for B in range(0,Bmax+1):
            qmax = -100
            idmax = 0
            if (i == slots-1):
                for t,task in enumerate(Tasks):
                    if (B-task.cost+Eprod[i] >= Bstart and task.quality > qmax):
                        qmax = task.quality
                        idmax = t+1
            else:
                for t,task in enumerate(Tasks):
                    Bprime = min(B-task.cost+Eprod[i],Bmax)
                    if (Bprime >= Bmin):
                        q = M[i+1][Bprime]
                        if (q == 0): continue
                        if (q + task.quality > qmax):
                            qmax = q + task.quality
                            idmax = t+1
            M[i][B] =  qmax if qmax != -100 else 0
            I[i][B] = idmax
    S = [0]*K
    B = Bstart
    for i in range(K):
        S[i] = I[i][B]-1
        if (S[i] < 0): return (S,0)
        B = min(B + Eprod[i] - Tasks[ S[i] ].cost,Bmax)
        assert(B >= Bmin)
    assert(B >= Bstart)
    return(S,sum(Tasks[s].quality for s in S))



def solution(tasks,upperbound):
    print("upperbound = ",upperbound)
    print(B[(K-1)%2][:])
    while upperbound >= 0 and (B[(K-1)%2][upperbound] < B_INIT or B[(K-1)%2][upperbound] == 0):
        print(B[(K-1)%2][upperbound])
        upperbound -= 1
    print("upperbound = ",upperbound)
    if upperbound < 0:
        return -1
    t = upperbound
    # note schedule use integers from 0 to 255
    schedule = np.zeros(K,dtype=np.int8)
    for s in range(K-1,-1,-1):
        schedule[s] = int(S[s][t])
        t -= tasks[ schedule[s]-1 ].quality
    print(schedule-1)
    return schedule

def ScheduleCarfagna(max_tax_ql,tasks,E) -> int:
    maxquality_previousslot = 0
    maxquality_currentslot = 0

    for k in range(K):
        print("."*40 + str(k) + "."*40)
        maxquality_currentslot = -1
        if (k == 0):
            print("iterations = ",max_tax_ql)
            for level in range(max_tax_ql):
                #print("level = ",level,end=", ")
                currentBmax = 0
                idMax = 0
                for index,t in enumerate(tasks):
                    Br = B_INIT + E[0] - t.cost;
                    if  t.quality == level and Br >= BMIN and Br >= currentBmax:
                        currentBmax = Br
                        idMax = index+1
                        maxquality_currentslot = level
                B[0][level] = min(currentBmax,BMAX)
                S[0][level] = idMax
                #print(B[0][level],", ",int(S[0][level]))
        else:
            print("iterations = ",maxquality_previousslot+max_tax_ql+1)
            for level in range(maxquality_previousslot+max_tax_ql+1):
                #print(level)
                currentBmax = 0
                idMax = 0
                for index,t in enumerate(tasks):
                     Bprec = B[(k-1)%2][level-t.quality]
                     Br = Bprec + E[k] - t.cost
                     if level >= t.quality and level - t.quality <= maxquality_previousslot and \
                        Bprec != 0 and Br >= BMIN and Br > currentBmax:
                        currentBmax = Br;
                        idMax = index+1;
                        maxquality_currentslot = level
                B[k%2][level] = min(currentBmax,BMAX);
                S[k][level] = idMax;
                #print(B[k%2][level],", ",int(S[k][level]))
        maxquality_previousslot = maxquality_currentslot
        if maxquality_previousslot == -1:
            return -1
    return maxquality_currentslot


if __name__ == "__main__":
    tasks = create_tasks()
    E = np.array([ 0, 0,0,0,0, 0,0,3,45,133,215,285,327,339,322,255,60,66,63, 23,9,0,0,0])
    E = E * 0.9
    E = E.astype(int)
    print_info(tasks)
    print("E = ",','.join(str(e) for e in E))

    maxq = ScheduleCarfagna(MAX_TASK_QL,tasks,E)
    ScheduleCarfagna = solution(tasks,maxq)
    check(K,ScheduleCarfagna-1,B_INIT,BMIN,BMAX,E,tasks,True)

    (s,q) = ScheduleClassic(K,B_INIT,BMIN,BMAX,E,tasks)
    print(s,q)
    check(K,s,B_INIT,BMIN,BMAX,E,tasks,True)


