# Projeto HPC

## Visão geral
Neste projeto implementamos um pipeline de computação paralela simples usando MPI em Python. Substitua o conteúdo desta seção pela descrição do seu problema (por exemplo: processamento de imagens médicas, análise de séries temporais, simulações numéricas), os dados usados e a motivação.

## Requisitos
- Python 3.10
- mpi4py
- SLURM (Santos Dumont) para execução em cluster
- (Opcional) CUDA e PyTorch para versões GPU

## Como rodar localmente
1. Prepare o ambiente:
```bash
bash scripts/build.sh
```
2. Execute localmente com MPI (exemplo 4 processos):
```bash
bash scripts/run_local.sh
```

Como rodar no Santos Dumont
```bash
sbatch scripts/job_cpu.slurm
# ou
sbatch scripts/job_gpu.slurm
```

## Estrutura do repositório
- src/ → código principal (MPI e implementação)
- scripts/ → automação (build/run/perfil/slurm)
- env/ → requisitos do ambiente (requirements.txt)
- data_sample/ → amostras de dados (opcional)
- results/ → logs, métricas e saídas das execuções
- report/ → relatório final (RELATORIO.pdf)

## Scripts importantes
- scripts/build.sh → instala dependências locais via pip
- scripts/run_local.sh → executa `src/main.py` com mpirun
- scripts/profile.sh → executa com `time` para perfilamento
- scripts/job_cpu.slurm → job SLURM de CPU (Santos Dumont)
- scripts/job_gpu.slurm → job SLURM para GPU

## Resultados esperados
- Registre speedup, throughput e limitações.
- Salve gráficos e tabelas em `results/`.

## Relatório
Coloque o relatório final em `report/RELATORIO.pdf` com 5–8 páginas cobrindo:
- Problema e relevância
- Arquitetura paralela usada
- Dados / I/O
- Metodologia (execuções, filas, parâmetros)
- Resultados (gráficos / tabelas)
- Limitações e próximos passos

---

Se quiser, posso também gerar um `RELATORIO.pdf` básico em LaTeX ou um esqueleto de relatório em Markdown.

## Mapeamento dos requisitos principais
Este projeto foi pensado para cumprir os três blocos de avaliação. Abaixo está o status atual e ações recomendadas para fechar gaps.

1) Engenharia & Paralelismo (1,2 pt)
- Implementado: arquitetura MPI com fallback serial em `src/main.py`.
- Implementado: scripts SLURM básicos em `scripts/job_cpu.slurm` e `scripts/job_gpu.slurm`.
- Implementado: runner de experimentos (`scripts/experiment.sh`) e coleta em CSV (`results/timings.csv`).
- Faltas / recomendações: instruir/ajustar `module load` e adicionar uma versão do job que executa o loop de experimentos no cluster e salva `timings.csv` em $SCRATCH. Se for necessário, adicionar OpenMP or GPU kernels em `src/main_gpu.py` para pontos de comparação.

2) Experimentos & Resultados (1,2 pt)
- Implementado: medições por execução (compute/comm/total) gravadas em `results/timings.csv`.
- Implementado: script de plotagem `scripts/plot_results.py` que gera `results/speedup.png` (requer `matplotlib`).
- Faltas / recomendações: rodar `scripts/experiment.sh` em ambiente com MPI para coletar dados p>1 e repetir execuções (repetições) para calcular médias/erro; instrumentar I/O real se for relevante; adicionar análise de gargalos (por exemplo, cronometrar I/O, profiling com cProfile para Python e perf/NVIDIA tools para GPU).

3) Reprodutibilidade & Comunicação (0,6 pt)
- Implementado: README, scripts, requirements em `env/requirements.txt`, e logs limpos em `results/timings.csv` e `results/speedup.png`.
- Faltas / recomendações: adicionar notebook ou `report/RELATORIO.md` com resultados e instruções passo-a-passo (opcional: CI para checar `python -m py_compile` e rodar smoke tests). Posso gerar esse relatório esqueleto automaticamente.

## Como reproduzir experimentos (resumo executável)
1. Instale dependências:
```powershell
python -m pip install -r env/requirements.txt
```
2. Rodar experimento local (serial ou com mpirun):
```bash
# executa as configurações definidas em scripts/experiment.sh
bash scripts/experiment.sh
# ou executar manualmente com mpirun
mpirun -np 4 python src/main.py --n 200000
```
3. Gerar plots:
```bash
python scripts/plot_results.py
# saída: results/speedup.png
```

## Próximos passos (para maximizar pontuação)
- Gerar um `job_cpu_experiments.slurm` que executa o loop de experimentos no cluster e copia `results/timings.csv` para $SCRATCH ou pasta persistente.
- Incluir I/O representativo se seu caso envolver leitura/gravação intensiva.
- Adicionar instrumentação de profiling (cProfile) e, se GPU, Nsight/NVPROF para identificar gargalos.
- Gerar relatório `report/RELATORIO.md` com gráficos e interpretação; posso criar o esqueleto automaticamente.

Se quiser, eu já crio o `job_cpu_experiments.slurm` e o esqueleto do relatório agora.
