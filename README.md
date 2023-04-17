# newscheduling
New Scheduler for Energy Harvesting Nodes.

The file common.h contains all algorithms, compile with -DCARFAGNA to obtain the Carfagna version.
Take the code from here to build the Arduino code just by copy past from common.h don't change
the Arduino code.

when compiled, with g++ main.cc -o main use main > output.txt to save the output, and
run 

python3 analyze.py output.txt

to check the output. see the main in analyze.py to see the different options.

