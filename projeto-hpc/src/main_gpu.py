"""Placeholder for GPU-enabled main. Replace with GPU implementation (PyTorch/CUDA) if needed."""
import time

def main():
    t0 = time.time()
    s = sum(i**0.5 for i in range(1000000))
    t1 = time.time()
    print(f"resultado={s:.4f} tempo={t1-t0:.3f}s")

if __name__ == '__main__':
    main()
