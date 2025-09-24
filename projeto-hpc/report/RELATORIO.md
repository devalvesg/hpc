# RELATÓRIO — Projeto HPC

Resumo executivo
-----------------
Este relatório descreve a implementação, experimentos e resultados de um protótipo de pipeline paralelo em Python usando MPI (via mpi4py). O objetivo é demonstrar práticas de engenharia para HPC, projetar experimentos reproduzíveis e analisar velocidade e gargalos em execução paralela.

Problema e relevância
----------------------
Problemas de computação intensiva (simulações numéricas, processamento de grandes volumes de dados, treinamento e inferência de modelos) são comuns em aplicações científicas e médicas. A paralelização permite reduzir tempo de execução e aumentar throughput. Este trabalho fornece um esqueleto reprodutível para medir speedup e eficiência usando MPI e, opcionalmente, GPU.

Arquitetura paralela usada
-------------------------
- Modelo: MPI (SPMD) via `mpi4py` com fallback serial quando MPI não está disponível.
- Cada processo calcula uma parcela (chunk) do domínio e realiza redução global (MPI_Reduce) para agregação de resultados.
- Scripts SLURM estão prontos (`scripts/job_cpu.slurm`, `scripts/job_gpu.slurm`) e um runner de experimentos (`scripts/experiment.sh`) executa múltiplas configurações.

Descrição do código
--------------------
- `src/main.py`: implementação principal. Divide trabalho por rank, mede tempos de computação e comunicação, grava uma linha em `results/timings.csv` contendo: procs, compute_time, comm_time, total_time, result.
- `src/main_gpu.py`: placeholder para implementação GPU (PyTorch/CUDA) para comparação.
- `scripts/experiment.sh`: executa experimentos para um conjunto de valores de processos e repetições.
- `scripts/plot_results.py`: gera `results/speedup.png` a partir do CSV de resultados.

Dados e I/O
-----------
O exemplo atual é computacional (f(x)=sqrt(x)) e não depende de entradas externas pesadas. Resultados e métricas são gravados em `results/timings.csv` em formato CSV para facilitar pós-processamento. Para cenários com I/O intensivo, recomenda-se instrumentar callbacks de I/O e gravar tempos separados.

Metodologia experimental
------------------------
- Parâmetro de trabalho: `--n` no `src/main.py` controla o tamanho do problema (default 100000). No runner de experimentos é usado `n=200000`.
- Variáveis controladas: número de processos (p), repetições (r) para média.
- Métricas coletadas por execução: tempo de computação, tempo de comunicação, tempo total e resultado agregado.

Configuração de execução usada para este relatório
--------------------------------------------------
- Execução de verificação (local, serial):

  Comando:

  ```bash
  python src/main.py --n 10000
  ```

- Resultado produzido (arquivo `results/timings.csv`):

  | procs | compute_time (s) | comm_time (s) | total_time (s) | result |
  |-------:|-----------------:|--------------:|---------------:|-------:|
  | 1     | 0.001222         | 0.000000      | 0.001223       | 666616.459197 |

Resultados e análise
---------------------
- Com os dados atuais temos apenas a execução serial (p=1). A linha acima é a base (baseline) para speedup.
- O gráfico de speedup (`results/speedup.png`) já foi gerado automaticamente após a execução do plotter; com mais runs para p>1 o gráfico mostrará speedup real.

Análise de bottlenecks (orientações)
-----------------------------------
- Comunicação: em execuções reais, a etapa `comm.reduce` será a responsável por overhead à medida que `p` cresce. Recomenda-se medir tempo de comunicação agregada por rank e por tamanho de mensagem.
- Computação: verifique distribuição de workloads (balanceamento). Usar `n % p` para distribuir o resto de forma equilibrada.
- I/O: se o problema envolve leitura de grandes arquivos, medir tempo de read/write separadamente e considerar paralel I/O (por exemplo, MPI-IO) ou leitura pré-carregada por rank 0 seguida de scatter.

Reprodutibilidade
-----------------
- Para reproduzir os experimentos, siga os passos no README:

  ```bash
  python -m pip install -r env/requirements.txt
  bash scripts/experiment.sh
  python scripts/plot_results.py
  ```

- Para rodar em cluster SLURM (Santos Dumont), recomenda-se criar um job que execute o loop de experimentos e salve `results/timings.csv` em `$SCRATCH`. Posso gerar `job_cpu_experiments.slurm` se desejar.

Limitações e próximos passos
---------------------------
- Limitações atuais:
  - Ainda não há execuções paralelas (p>1) gravadas neste repositório de exemplo—é necessário rodar `scripts/experiment.sh` em ambiente com MPI para preencher os dados.
  - `src/main_gpu.py` é apenas um placeholder; para avaliação GPU é necessário implementar a versão com PyTorch/CUDA.

- Próximos passos recomendados:
  1. Rodar `scripts/experiment.sh` em máquina com MPI para coletar dados p=1,2,4,8 com repetições e reexecutar o plot.
  2. Implementar `job_cpu_experiments.slurm` para automatizar experimentos em SLURM e salvar resultados em `$SCRATCH`.
  3. Implementar a versão GPU em `src/main_gpu.py` e comparar tempo/throughput.
  4. Adicionar profiling (cProfile / NVIDIA tools) para identificar gargalos e reportar p50/p95 em caso de inferência.

Conclusão
---------
O repositório fornece um esqueleto robusto para realizar experimentos de paralelização com MPI, coletar medições e gerar gráficos de speedup. Com as ações recomendadas (rodar experiments com MPI, implementar versão GPU e job SLURM para experimentos), o projeto atenderá plenamente os três critérios de avaliação (engenharia & paralelismo; experimentos & resultados; reprodutibilidade & comunicação).

---

Arquivo(s) referenciados:
- `results/timings.csv`
- `results/speedup.png`
