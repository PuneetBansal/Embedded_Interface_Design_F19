#!/bin/bash

node nodejsServer.js &
P1=$!
python3 proj1.py &
P2=$!
wait $P1 $P2
