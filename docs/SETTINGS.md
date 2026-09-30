# SETTINGS.md - Configurações Avançadas

## 🎛️ Configurações do Sampler

### Parâmetros Principais

#### Seed
```
Função: Número aleatório que gera resultado único
Padrão: 42
Variações: Use 42, 123, 456, 789 para diferentes resultados

Dica: Mesmo seed + mesmo prompt = resultado idêntico
      Seeds diferentes = variações diferentes
```

#### Steps
```
Função: Número de iterações de refinamento
Padrão: 30 (SDXL-Turbo)

SDXL-Turbo:
├─ 15 steps:    Muito rápido (1-2 min), qualidade média
├─ 20 steps:    Rápido, qualidade boa
├─ 30 steps:    Normal, ótima qualidade (PADRÃO)
└─ 50+ steps:   Muito lento, mínima melhoria

SDXL Normal:
├─ 20 steps:    Rápido, qualidade aceitável
├─ 30 steps:    Normal, boa qualidade
├─ 40 steps:    Melhor qualidade
├─ 50 steps:    Muito boa qualidade
└─ 80+ steps:   Excessivo, não compensa
```

#### CFG Scale (Classifier-Free Guidance)
```
Função: Quanto aderir ao prompt (6-15)
Padrão: 7.5

Valores:
├─ 5-6:     Muito criativo, pode não seguir prompt
├─ 6-7:     Criativo, natural (RECOMENDADO)
├─ 7-8:     Balanceado (PADRÃO)
├─ 8-10:    Muito aderente, pode ficar "forçado"
└─ 10-15:   Muito rígido, parece IA

Para Vivazco:
├─ Cubas/Pias: 7.0-7.5 (delicado)
├─ Sanitários: 7.5-8.0 (mais detalhado)
└─ Ambiental:  6.5-7.5 (mais natural)
```

#### Sampler (Método)
```
Recomendados (em ordem de qualidade):
1. dpmpp_2m_sde_karras      ✓ MELHOR, padrão
2. dpmpp_2m_sde             ✓ Bom, sem karras
3. euler_ancestral          ✓ Rápido e bom
4. dpmpp_3m_sde             ⚠ Mais lento

Evitar:
├─ heun:                     ✗ Artefatos visíveis
├─ lms:                      ✗ Qualidade pior
└─ uni_pc:                   ✗ Inconsistente
```

#### Scheduler (Agendador)
```
Função: Controla a sequência de noise reduction

Opções:
├─ karras                    ✓ PADRÃO (melhor)
├─ normal                    ✓ Bom
├─ linear                    ⚠ Menos natural
└─ simple                    ⚠ Menos natural

Recomendação: Manter em "karras"
```

#### Denoise
```
Função: Força da alteração (0.0-1.0)
Padrão: 1.0

Uso:
├─ 0.1-0.3:     Mínima alteração (inpainting)
├─ 0.5-0.7:     Inpainting com modificação
├─ 0.8-0.95:    Normal, bom balanço
└─ 1.0:         Máxima alteração (nova geração)

Para Vivazco: Manter em 0.8-1.0
```

---

## 🖼️ Configurações de Imagem

### ImageScale Node

```
Width/Height:
├─ Input: Resolução de entrada (redimensiona se necessário)
├─ Output: 1080x1080 (padrão para e-commerce)
└─ Alternativas: 800x800, 1600x1600

Upscale Method:
├─ lanczos   ✓ MELHOR (padrão)
├─ bicubic   ✓ Bom
├─ bilinear  ⚠ Mais rápido, qualidade menor
└─ nearest   ✗ Pixelado

Crop:
├─ center    ✓ PADRÃO (recorta do centro)
├─ top       ⚠ Recorta de cima
├─ bottom    ⚠ Recorta de baixo
└─ fill      ✓ Estende mantendo proporção
```

---

## 🎨 Configurações de Qualidade

### Preset Rápido (2-3 min)
```
├─ Model: SDXL-Turbo
├─ Steps: 20
├─ CFG: 7.0
├─ Sampler: dpmpp_2m_sde_karras
├─ Scheduler: karras
└─ Denoise: 0.95

Quando usar: Testes rápidos, muitas variações
```

### Preset Balanceado (3-5 min) ⭐ PADRÃO
```
├─ Model: SDXL-Turbo
├─ Steps: 30
├─ CFG: 7.5
├─ Sampler: dpmpp_2m_sde_karras
├─ Scheduler: karras
└─ Denoise: 1.0

Quando usar: Produção, maioria dos casos
```

### Preset Alta Qualidade (8-12 min)
```
├─ Model: SDXL (não turbo)
├─ Steps: 50
├─ CFG: 7.0
├─ Sampler: dpmpp_2m_sde_karras
├─ Scheduler: karras
└─ Denoise: 1.0

Quando usar: Produtos premium, qualidade máxima
```

### Preset Máxima Qualidade (15-25 min)
```
├─ Model: SDXL
├─ Steps: 80
├─ CFG: 7.0
├─ Sampler: dpmpp_2m_sde_karras
├─ Scheduler: karras
└─ Denoise: 1.0

Quando usar: Raramente, quando qualidade é crítica
```

---

## 💾 Configurações de Performance

### Para GPU RTX 3060 (12GB)

```
Otimizado:
├─ Batch: 1
├─ VRAM Split: Default
├─ Memory Mode: Normal
├─ Steps: 20-30 (SDXL-Turbo)
└─ Resolution: 1024x1024

Máximo:
├─ Batch: 2
├─ Steps: 40-50 (SDXL-Turbo)
├─ Resolution: 1280x1280
└─ VAE: Ativado
```

### Para GPU RTX 4080 (24GB)

```
Normal:
├─ Batch: 2-4
├─ VRAM Split: 50/50
├─ Memory Mode: Normal
├─ Steps: 30-50 (SDXL)
└─ Resolution: 1280x1280

Máximo:
├─ Batch: 4
├─ Steps: 80 (SDXL)
├─ Resolution: 1536x1536
├─ VAE: Ativado
└─ ControlNet: Sim
```

### Para CPU Only (sem GPU)

```
⚠️ NÃO RECOMENDADO

Se forçado:
├─ Model: SDXL-Turbo (menor)
├─ Steps: 10-15
├─ Resolution: 512x512
├─ Batch: 1
├─ Esperar: 60-90 min por imagem
└─ Considerar: Usar serviço em nuvem
```

---

## 🎛️ Configurações ComfyUI

### Arquivo `settings.json` Recomendado

```json
{
  "auto_queue": false,
  "default_graph": null,
  "input_directory": "inputs",
  "output_directory": "outputs",
  "enable_execution_history": true,
  "execution_history_expiration": 86400,
  "temp_directory": "temp",
  "listen": "0.0.0.0",
  "port": 8188,
  "tls_keyfile": null,
  "tls_certfile": null,
  "enable_cors_header": false,
  "cuda_malloc": false,
  "disable_xformers": false,
  "cudnn_enabled": true,
  "cpu": false,
  "gpu_device_id": 0,
  "cudnn_benchmark": true,
  "num_threads": 4
}
```

### Environment Variables

```bash
# Para performance
export CUDA_VISIBLE_DEVICES=0          # Usar GPU 0
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb=512

# Para debug
export COMFYUI_DEVMODE=true
export COMFYUI_DEBUG=1

# Para proxy
export HTTP_PROXY=http://proxy:8080
export HTTPS_PROXY=https://proxy:8080
```

---

## 📊 Matriz de Recomendações

### Por Tipo de Produto

```
CUBAS REDONDAS:
├─ Estilo: Spa/Luxury
├─ CFG: 7.0-7.5
├─ Steps: 30-40
├─ Seed: 42, 123, 456
└─ Denoise: 0.95

SANITÁRIOS:
├─ Estilo: Contemporary/Classic
├─ CFG: 7.5-8.0
├─ Steps: 30-40
├─ Seed: 42, 789, 1011
└─ Denoise: 1.0

PIAS MODERNAS:
├─ Estilo: Minimalist/Industrial
├─ CFG: 7.0
├─ Steps: 20-30
├─ Seed: 123, 456, 789
└─ Denoise: 0.9

PEÇAS PREMIUM:
├─ Estilo: Luxury Premium
├─ CFG: 7.5
├─ Steps: 50+ (SDXL)
├─ Seed: Variado
└─ Denoise: 1.0
```

### Por Plataforma E-commerce

```
MERCADO LIVRE:
├─ Resolução: 1080x1080
├─ Formato: JPEG 85%
├─ Qualidade: Normal (SDXL-Turbo)
└─ Tempo: 2-3 min

SHOPEE:
├─ Resolução: 800x800 ou 1080x1080
├─ Formato: JPEG ou WebP
├─ Qualidade: Normal
└─ Tempo: 2-3 min

AMAZON:
├─ Resolução: 1200x1200 mín.
├─ Formato: JPEG 90%
├─ Qualidade: Alta (SDXL)
└─ Tempo: 8-10 min

LOJA PRÓPRIA:
├─ Resolução: 1600x1600
├─ Formato: WebP 85%
├─ Qualidade: Alta (SDXL)
└─ Tempo: 8-10 min
```

---

## 🔐 Segurança e Conformidade

### Preservação de Produto

```
NUNCA modificar:
❌ Cor original
❌ Forma/proporções
❌ Brilho/reflexos naturais
❌ Detalhes de acabamento

SEMPRE preservar:
✓ Dimensões originais
✓ Características únicas
✓ Material aparente
✓ Identidade do produto
```

### Marca d'água (Watermark)

```
Adicionar opcionalmente:
├─ Usar layer separada
├─ Transparência: 10-20%
├─ Posição: canto inferior direito
├─ Tamanho: 5-10% da imagem
└─ Fonte: Sans-serif legível

Remover de prompts negativo:
"watermark, text, logo, brand"
```

---

## 📈 Monitoramento de Performance

### Métricas Importantes

```
VRAM:
├─ Ideal: 6-8GB em uso
├─ Máximo: 11GB (deixe 1GB margem)
└─ Verificar: nvidia-smi a cada execução

TEMPO:
├─ Esperado: 2-3 min (SDXL-Turbo)
├─ Aceitável: até 5 min
└─ Problema: >10 min (otimizar)

QUALIDADE:
├─ Verificar: Artefatos, cores, realismo
├─ Sem IA: Deve parecer fotografia real
└─ Produto: 100% preservado
```

---

## 🚀 Otimizações Extras

### Para Velocidade

```bash
# No ComfyUI:
1. Desabilitar preview automática
2. Usar SDXL-Turbo
3. Reduzir steps a 20
4. Usar xFormers (se NVIDIA GPU)
5. Habilitar CuDNN Benchmark

Ganho: ~40% de velocidade
```

### Para Qualidade

```bash
# No ComfyUI:
1. Usar SDXL (não turbo)
2. Aumentar steps a 50-80
3. Usar VAE bom (SDXl-VAE)
4. CFG: 7.0-7.5
5. Desabilitar Turbo

Ganho: ~30% melhor qualidade
```

### Para VRAM

```bash
# No ComfyUI:
1. Reducir resolution a 832x832
2. Usar SDXL-Turbo
3. Batch: 1
4. Habilitar Memory Efficient Attention
5. Desabilitar CuDNN Benchmark

Ganho: ~50% menos VRAM
```

---

**Última atualização:** 2026-09-30  
**Sugestões de configuração:** Ambiente Linux/Mac/Windows recomendado
