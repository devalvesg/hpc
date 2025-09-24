#!/bin/bash
#SBATCH --job-name=proj_gpu
#SBATCH --output=results/%x_%j.out
#SBATCH --error=results/%x_%j.err
#SBATCH --time=00:30:00
#SBATCH --gpus=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G

module load cuda python/3.10 pytorch  # ajuste no SD

python3 src/main_gpu.py
