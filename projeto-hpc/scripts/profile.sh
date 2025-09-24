#!/usr/bin/env bash
set -e
time mpirun -np 4 python3 src/main.py
