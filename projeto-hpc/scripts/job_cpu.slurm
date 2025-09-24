#!/bin/bash
#SBATCH --job-name=proj_cpu
#SBATCH --output=results/%x_%j.out
#SBATCH --error=results/%x_%j.err
#SBATCH --time=00:20:00
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G

module load mpi python/3.10  # ajuste no SD

echo "Iniciando em $(date)"
srun python3 src/main.py
