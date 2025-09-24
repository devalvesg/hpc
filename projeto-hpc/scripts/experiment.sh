#!/usr/bin/env bash
set -e

# Runner de experimentos simples
# Ajuste NUMPROCS e REPETITIONS conforme necessidade
NUMPROCS=(1 2 4 8)
REPETITIONS=3

ROOT=$(cd "$(dirname "$0")/.." && pwd)
CSV="$ROOT/results/timings.csv"
rm -f "$CSV"

for p in "${NUMPROCS[@]}"; do
  for r in $(seq 1 $REPETITIONS); do
    echo "Run procs=$p repetition=$r"
    if command -v mpirun >/dev/null 2>&1; then
      mpirun -np "$p" python3 src/main.py --n 200000
    elif command -v mpiexec >/dev/null 2>&1; then
      mpiexec -n "$p" python src/main.py --n 200000
    else
      # fallback serial
      python src/main.py --n 200000
      break
    fi
  done
done

echo "Experimentos concluídos. Resultados em $CSV"
