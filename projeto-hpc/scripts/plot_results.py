"""Gera plot de speedup a partir de results/timings.csv

Uso: python scripts/plot_results.py
"""
import csv
import os
from collections import defaultdict
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSV = os.path.join(ROOT, 'results', 'timings.csv')

if not os.path.exists(CSV):
    print('Nenhum arquivo de resultados encontrado:', CSV)
    raise SystemExit(1)

data = defaultdict(list)
with open(CSV, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        p = int(row['procs'])
        t = float(row['total_time'])
        data[p].append(t)

procs = sorted(data.keys())
avg = [sum(data[p]) / len(data[p]) for p in procs]

# speedup em relação a p=1
if 1 not in data:
    print('Não há corrida com 1 processo para baseline')
    raise SystemExit(1)
baseline = sum(data[1]) / len(data[1])
speedup = [baseline / t for t in avg]

plt.figure()
plt.plot(procs, speedup, marker='o')
plt.xlabel('processos')
plt.ylabel('speedup (baseline p=1)')
plt.title('Speedup')
plt.grid(True)
out = os.path.join(ROOT, 'results', 'speedup.png')
plt.savefig(out)
print('Plota salvo em', out)
