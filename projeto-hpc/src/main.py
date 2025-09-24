"""MPI example with detailed timing, fallback to serial if MPI not available.

Produces a CSV line in `results/` with: procs,compute_time,comm_time,total_time,result
"""
import time
import math
import os
import csv

try:
    from mpi4py import MPI
    mpi_available = True
except Exception:
    MPI = None
    mpi_available = False


def trabalho(x):
    # exemplo de computação pesada por item
    return math.sqrt(x)


def run(n=100000):
    # garante diretório de resultados
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    results_dir = os.path.join(root, 'results')
    os.makedirs(results_dir, exist_ok=True)

    if mpi_available:
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()
    else:
        rank = 0
        size = 1

    # divisão de trabalho
    chunk = n // size
    start = rank * chunk
    end = n if rank == size - 1 else (rank + 1) * chunk

    t0 = time.time()

    # medição de computação local
    comp_t0 = time.time()
    local = sum(trabalho(i) for i in range(start, end))
    comp_t1 = time.time()

    # sincronização / redução
    comm_t0 = time.time()
    if mpi_available:
        total = comm.reduce(local, op=MPI.SUM, root=0)
    else:
        total = local
    comm_t1 = time.time()
    t1 = time.time()

    compute_time = comp_t1 - comp_t0
    comm_time = comm_t1 - comm_t0
    total_time = t1 - t0

    if rank == 0:
        # salvar em CSV para experimentos
        csv_path = os.path.join(results_dir, 'timings.csv')
        header = ['procs', 'compute_time', 'comm_time', 'total_time', 'result']
        write_header = not os.path.exists(csv_path)
        with open(csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(header)
            writer.writerow([size, f"{compute_time:.6f}", f"{comm_time:.6f}", f"{total_time:.6f}", f"{total:.6f}"])

        print(f"resultado={total:.4f} tempo_total={total_time:.3f}s comp={compute_time:.3f}s comm={comm_time:.3f}s procs={size}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=100000, help='tamanho do trabalho (n)')
    args = parser.parse_args()
    run(n=args.n)
