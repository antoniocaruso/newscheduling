
# Please add here the date of last change, or add to a git repo.
# Antonio / 27/04/2023


import sys
import numpy as np
from scheduling import Task,iot_schedule_exact,carfagna_schedule

# def iterated_test():
#     K: int = 24
#     Bmin: int = 10
#     Bmax: int = 220
#     Bstart = 180
#     Panel = [0,0,0,0,0,1,3,5,20,50,70,120,120,70,50,20,5,3,1,0,0,0,0,0]
#     Tasks = []
#     for x in zip([2,10,20,32,50],[1,2,3,4,5]):
#         Tasks.append(Task(*x))
#     (S,Q) = ScheduleClassic(K,Bstart,Bmin,Bmax,Panel,Tasks)
#     print("Q = ",Q)
#     print("S = ",S)
#     qsum = 0
#     Bend = Bstart
#     S = []
#     for i in range(K):
#     #print("run with",(K-i,Bstart))
#         (Q,task) = ScheduleNoMem(K-i,Bstart,Bmin,Bmax,Panel[i:],Tasks,Bend)
#     qsum += Tasks[task-1].quality
#     print("Q = ",Q," t = ",task-1, "qsum = ", qsum);
#     Bstart = min( Bstart - Tasks[task-1].cost + Panel[i], Bmax )
#     S += [task-1]
#     print("S' =",S)
#     print("TotalEnergy = ",sum(Panel)," ",sum(Panel)/K)
#     sys.exit();

#### main program

def parse_input(lines):
    iterations = []
    i = 0
    while "it,Energy" not in lines[i]: i += 1
    if i == 0:
        print("Error in input file.")
        sys.exit(0)
    # parse all variabile in input
    com = ""
    inside = False
    for l in lines[0:i]:
        if not inside and '[' in l and ']' not in l:
           com += l 
           inside = True
        else:
            if inside and ']' not in l:
                com += l
            elif inside and ']' in l:
                com += l + "\n"
            else:
                com += l + "\n"
    # parse iteration data
    it: int = 0
    Energy: int = 0
    Q: int = 0
    Time: int = 0
    E,S = [],[]
    print(f"start parsing {len(lines)} lines:")
    inside = True
    while True:
        j = i+1
        ldict = {}
        while j<len(lines) and "it,Energy" not in lines[j]: 
            j += 1
        if j-i<5:
           break 
        exec("\n".join(lines[i:j]),globals(),ldict)
        iterations.append({ 'it': ldict['it'], 
                       'Energy': ldict['Energy'], 
                       'Q': ldict['Q'], 
                       'E': np.array(ldict['E']), 
                       'S': np.array(ldict['S']) })
        i = j
    return i,com,iterations



if __name__ == "__main__":
    # analyze.py console_output.txt option
    # console_output.txt -> output from Ardino serial, start with #------
    # option:
    # none -> parse input, run schedule exact, compare with schedule Arduino
    # 1.   -> parse input, just ouput the Arduino 'input' for scheduling
    # 2.   -> parse input, run ScheduleClassic, output result (no comparison)
    # 3.   -> parse input, run ScheduleCalssic and schedule, compare.
    # 4.   -> parse input, check if quality is correct

    K,N,BMIN,BMAX,BINIT,BSAMPLING,MAX_QUALITY_LVL = [0]*7
    c_i: list[int] = []
    q_i: list[int] = []
    l_i: list[int] = []
    e_i: list[int] = []
    it: int = 0
    Energy, Q, Time, E, S = 0,0,0,[],[]
    
    if len(sys.argv) == 1:
        print("analyze [serialdump]")
        sys.exit()
#   option = int(sys.argv[2]) if len(sys.argv) == 3 else 0
    
    # read input
    f = open(sys.argv[1],encoding="utf8")
    lines = f.read().split("\n")
    i,com,iterations = parse_input(lines)
    exec(com)
    #--print header
    print("-"*20)
    print(K,N)
    print(BMIN,BMAX,BINIT,BSAMPLING)
    print(MAX_QUALITY_LVL)
    print(c_i)
    print(q_i)
    print(l_i)
    Tasks = []
    if len(l_i) == 0:
        l_i = [0]*K
        alg_input = "IoT"
    else:
        alg_input = "Carfagna"
    for x in zip(c_i, q_i, l_i):
        Tasks.append(Task(*x))
    print("-"*20)

    #-- start analysis
    for data in iterations:
        it = data['it']
        Q = data['Q']
        Energy = data['Energy']
        E = data['E']
        S = data['S']
        print(f"iteration: {it}, E = {E}")
        (s1,quality1) = iot_schedule_exact(K,BINIT,BMIN,BMAX,E,Tasks)
        (s2,quality2) = carfagna_schedule(K,BINIT,BMIN,BMAX,MAX_QUALITY_LVL,E,Tasks)
        print(f"quality input {alg_input}    =  {Q}")
        print("quality python exact      = ",quality1)
        print("quality python carfagna   = ",quality2)
        print(f"S input {alg_input} = {S}")
        print(f"S python exact    = {np.array(s1)+1}")
        print(f"S python carfagna = {np.array(s2)+1}")


        # do not use for now..
        # if option == 1:
        #     print("%2d" % (it),"\t",E)
        # elif option == 2:
        #     print("%2d" % (it),"\t",E)
        #     (s,q) = ScheduleClassic(K,BINIT,BMIN,BMAX,E,Tasks)
        #     print(" ",q,end=" - ")
        #     print(f"S = {s}" if q!=0 else "")
        # elif option == 3:
        #     print("%2d" % (it),"\t",E)
        #     (s,q) = ScheduleClassic(K,BINIT,BMIN,BMAX,E,Tasks)
        #     print(" ",q,end=" - ")
        #     print(f"S = {s}" if q!=0 else "")
        #     (s,q) = schedule(K,BINIT,BMIN,BMAX,E,Tasks)
        #     print(" ",q,end=" - ")
        #     print(f"S = {s}" if q!=0 else "")
        # elif option == 0:   
        #     print("%2d " % (it),Energy,Time,end=" - \n")
        #     (Sn,q) = schedule(K,BINIT,BMIN,BMAX,E,Tasks)
        #     print("\t",E)
        #     print("\tS Esatta   ",Sn,q)
        #     print("\tS Arduino  ",S,Q,"%.1f%%" % (100*Q/q))
        # elif option == 4:
        #     print("%2d" % (it)," ",E)
        #     (s,q) = ScheduleClassic(K,BINIT,BMIN,BMAX,E,Tasks)
        #     print("    ",S,Q,check(K,S,BINIT,BMIN,BMAX,E,Tasks),q)