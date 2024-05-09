#!/bin/bash

# for i in [1, 3, 10]
for i in 5 10 50 100
do 
  npm run single-start;
  venv/bin/python benchmark.py 1 $i;
  npm run single-stop;
done

for i in 5 10 50 100
do 
  ./setup-triple.sh;
  venv/bin/python benchmark.py 3 $i;
  npm run triple-stop;
done

for i in 5 10 50 100
do 
  ./setup-ten.sh;
  venv/bin/python benchmark.py 10 $i;
  npm run ten-stop;
done

venv/bin/python calculate-avg.py

