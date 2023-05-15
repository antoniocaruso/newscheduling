DATE = $(shell date +'%d%m%H%M%S')
K?=24

all: carfagna iot

carfagna: common.h main.cc 
	g++ -O2 -DCARFAGNA -D"K=$(K)" -Wp,-w  main.cc -o main_carfagna

iot: common.h main.cc 
	g++ -O2 -D"K=$(K)" -Wp,-w main.cc -o main_iot

run: main_iot main_carfagna
	./main_iot > output/out_$(K)_$(DATE)_iot.txt
	./main_carfagna > output/out_$(K)_$(DATE)_carfagna.txt


.PHONY: clean_output
clean_output:
	-rm output/*.txt

