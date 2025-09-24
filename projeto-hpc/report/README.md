# Projeto HPC - LoRA Fine-tuning + Inference Batching

## Descrição

Este projeto implementa um pipeline completo de fine-tuning leve via LoRA (Low-Rank Adaptation) e inferência em lote (batching) otimizada para GPUs. O objetivo é demonstrar técnicas de aceleração de modelos de linguagem no contexto de aplicações TechMed (Tecnologia Médica).

### Pipeline Principal
1. **Fine-tuning LoRA**: Adaptação eficiente de modelos base (padrão: distilgpt2) usando LoRA
2. **Inference Batching**: Execução de inferência em lotes com coleta de métricas de performance
3. **Profiling**: Análise detalhada de tokens/s, latência p50/p95, uso de GPU

## Pré-requisitos

- **Python**: 3.10+
- **Hardware**: GPU recomendada (CUDA), fallback para CPU
- **Ambiente**: Suporte local e clusters SLURM (ex.: Santos Dumont)

### Dependências
- torch
- transformers 
- datasets
- peft
- accelerate
- tqdm
- (Opcional) bitsandbytes, pynvml

## Instalação e Configuração

### 1. Setup Local
```bash
# Clone e navegue para o diretório
cd projeto-hpc-gpu-lora/

# Execute o script de build (cria venv e instala dependências)
bash scripts/build.sh
```

### 2. Execução Local
```bash
# Execute pipeline completo (treino + inferência)
bash scripts/run_local.sh
```

### 3. Execução no SLURM

#### GPU (recomendado)
```bash
sbatch scripts/job_gpu.slurm
```

#### CPU (fallback)
```bash 
sbatch scripts/job_cpu.slurm
```

## Modo Offline (Hugging Face Cache)

Para ambientes sem internet ou com restrições de acesso:

### Download de Modelos Offline
```python
from huggingface_hub import snapshot_download

# Download do modelo base
snapshot_download(
    repo_id="distilgpt2",
    cache_dir="/path/to/cache",
    local_files_only=False
)
```

### Configuração de Variáveis de Ambiente
```bash
# Definir cache local do Hugging Face
export HF_HOME="/path/to/hf_cache"
export TRANSFORMERS_CACHE="/path/to/transformers_cache"

# Modo offline
export TRANSFORMERS_OFFLINE=1
```

### No Santos Dumont
```bash
# Recomendação: usar /scratch para cache
export HF_HOME="/scratch/${USER}/hf_cache"
export TRANSFORMERS_CACHE="/scratch/${USER}/transformers_cache"

# Baixar modelos antes da execução
python -c "
from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
model = AutoModelForCausalLM.from_pretrained('distilgpt2')
"
```

## Estrutura do Projeto

```
projeto-hpc-gpu-lora/
├── README.md              # Este arquivo
├── env/
│   └── requirements.txt   # Dependências Python
├── src/
│   ├── train_lora.py     # Script de fine-tuning LoRA
│   ├── infer_batch.py    # Script de inferência em lote
│   └── utils.py          # Utilitários (timer, batchify)
├── data_sample/
│   ├── train.txt         # Dados de treino (sintético TechMed)
│   ├── val.txt           # Dados de validação
│   └── prompts.txt       # Prompts para inferência
├── scripts/
│   ├── build.sh          # Setup do ambiente
│   ├── run_local.sh      # Execução local completa
│   ├── job_gpu.slurm     # Job SLURM para GPU
│   ├── job_cpu.slurm     # Job SLURM para CPU
│   └── profile.sh        # Script de profiling
├── results/              # Outputs e métricas
└── report/
    └── RELATORIO.md      # Template do relatório
```

## Métricas Coletadas

### Performance de Inferência
- **tokens/s**: Taxa de geração de tokens
- **Latência p50**: Mediana do tempo de resposta
- **Latência p95**: 95º percentil do tempo de resposta
- **Throughput**: Tokens processados por segundo

### Training Metrics
- **Tempo por época**: Duração do treinamento
- **Loss**: Função de perda durante treino
- **Uso de GPU**: Memória e utilização (se disponível)

### Monitoramento de Sistema
- **Memória GPU**: Alocação e uso
- **CPU**: Utilização de cores
- **I/O**: Taxa de leitura/escrita de dados

## Comandos de Exemplo

### Treino LoRA Customizado
```bash
python src/train_lora.py \
    --base_model distilgpt2 \
    --train_path data_sample/train.txt \
    --val_path data_sample/val.txt \
    --save_dir results/lora-custom \
    --epochs 2 \
    --max_steps 100 \
    --lr 2e-4 \
    --lora_r 16 \
    --lora_alpha 32
```

### Inferência em Lote
```bash
python src/infer_batch.py \
    --base_model distilgpt2 \
    --adapter_dir results/lora-distilgpt2 \
    --prompts data_sample/prompts.txt \
    --batch_size 16 \
    --max_new_tokens 64 \
    --iters 20
```

## Otimizações Implementadas

### LoRA (Low-Rank Adaptation)
- Redução de parâmetros treináveis (~0.1% do modelo original)
- Fine-tuning eficiente mantendo qualidade
- Menor uso de memória GPU

### Inference Batching
- Processamento paralelo de múltiplas entradas
- Otimização de throughput GPU
- Balanceamento latência vs. throughput

### Precision Optimization
- FP16 automático em GPU para economia de memória
- Compatibilidade com quantização (preparado para bitsandbytes)

## Troubleshooting

### Problemas Comuns

**GPU Out of Memory**:
```bash
# Reduza batch_size ou use CPU
python src/train_lora.py --no_cuda --batch_size 4
```

**Modelo não encontrado offline**:
```bash
# Verifique cache e variáveis de ambiente
echo $HF_HOME
echo $TRANSFORMERS_CACHE
```

**Erro de dependências**:
```bash
# Reinstale ambiente limpo
rm -rf .venv
bash scripts/build.sh
```

## Performance Esperada

### Hardware de Referência
- **GPU**: Tesla V100 (Santos Dumont)
- **CPU**: 8+ cores, 24GB+ RAM

### Benchmarks Típicos
- **Treino LoRA**: ~50-100 steps/min (GPU)
- **Inferência**: ~100-500 tokens/s (batch_size=16)
- **Latência p50**: <100ms por batch

## Contribuição

Este projeto segue as boas práticas de HPC:
- Código limpo e documentado
- Scripts reprodutíveis
- Logs estruturados
- Métricas padronizadas

Para modificações, mantenha:
- PEP8 compliance
- Comentários essenciais
- Compatibilidade CPU/GPU
- Suporte a SLURM

## Licença

Projeto acadêmico para fins educacionais em HPC e Machine Learning.