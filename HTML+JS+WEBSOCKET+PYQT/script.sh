#!/bin/bash

node nodejsServer.js &
P2=$!
python3 proj1.py &
P3=$!
wait $P1 $P2
