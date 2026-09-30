# WORKFLOW.md - Guia Passo-a-Passo

## 📋 Índice

1. [Preparação Inicial](#preparação-inicial)
2. [Fluxo Básico](#fluxo-básico)
3. [Fluxo Avançado](#fluxo-avançado)
4. [Processamento em Lote](#processamento-em-lote)
5. [Otimização para E-commerce](#otimização-para-e-commerce)
6. [Adição de Dimensões](#adição-de-dimensões)

---

## 🚀 Preparação Inicial

### 1. Setup do Projeto

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/vivazco.git
cd vivazco

# Execute setup
python scripts/setup.py

# Instale dependências
pip install -r requirements.txt
```

### 2. Prepare Modelos ComfyUI

```
models/
├── checkpoints/
│   ├── sd_xl_turbo_1.0.safetensors    ← Recomendado (rápido)
│   └── sd_xl_base_1.0.safetensors     ← Alternativa (melhor qualidade)
├── vae/
│   └── sdxl_vae.safetensors           ← Opcional (melhor qualidade)
└── controlnets/
    └── (ControlNets opcionais)
```

**Download Recomendado:**
- SDXL-Turbo: https://huggingface.co/stabilityai/sdxl-turbo
- SDXL Base: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
- VAE: https://huggingface.co/stabilityai/sdxl-vae

### 3. Copie Imagens de Produto

```
inputs/products/
├── cuba_preta_01.jpg       (1024x1024px, 500KB)
├── pia_marmore_02.jpg      (800x600px, 300KB)
└── sanitario_branco_03.png (1200x800px, 400KB)
```

**Especificações:**
- Formato: JPEG, PNG, WebP
- Resolução: 512px a 2048px (mínimo 512x512)
- Tamanho: Até 2MB por arquivo
- Background: Com ou sem (ambos suportados)

---

## 📊 Fluxo Básico

### Passo 1: Abrir ComfyUI

```bash
# Em um terminal, navegue até ComfyUI
cd /caminho/para/ComfyUI

# Inicie o servidor
python main.py
```

Acesse: `http://localhost:8188`

### Passo 2: Carregar o Pipeline

1. Clique em **"Load"** (canto superior esquerdo)
2. Navegue até: `pipeline/main_pipeline.json`
3. Clique em **"Open"**

O pipeline com todos os nodes será carregado.

### Passo 3: Editar Node de Entrada

1. **Encontre o node "🖼️ Carregar Imagem do Produto"** (node 1)
2. Clique em **"Choose File"** ou edite o caminho:
   ```
   inputs/products/seu_produto.jpg
   ```
3. Clique em **"Upload"** se for novo arquivo

### Passo 4: Ajustar Prompts (Opcional)

Existem 4 nodes de prompt para diferentes estilos:

#### Node 4 - Estilo Luxury (Padrão)
```
a luxury bathroom with [PRODUTO], sophisticated lighting, 
marble countertops, premium fixtures, professional photography, 
cinematic lighting, 8k quality, hyperrealistic
```

**Customize:**
- Substitua `[PRODUTO]` por: "black bathroom sink", "ceramic toilet", etc
- Adicione detalhes: "gold fixtures", "natural light", "spa-like"

#### Node 10 - Estilo Studio Clean
```
professional product photography, studio lighting, clean white background, 
[PRODUTO], centered composition, sharp focus, commercial photography
```

#### Node 15 - Estilo Industrial Moderno
```
modern bathroom interior design, industrial chic, concrete and steel, 
dramatic side lighting, [PRODUTO] as focal point, architectural photography
```

#### Node 20 - Estilo Spa Minimalista
```
spa-like bathroom, zen aesthetic, natural light, plants, wooden accents, 
minimalist design, [PRODUTO], calming atmosphere
```

### Passo 5: Configurar Sampler

Para cada **Sampler** (nodes 6, 11, 16, 21):

```
Configurações Principais:
├─ Seed: [42, 123, 456, 789]  ← Mude para variar resultado
├─ Steps: 30                   ← SDXL-Turbo (20-30)
│  └─ Para SDXL: 40-50        ← Melhor qualidade
├─ CFG: 7.5                    ← 6-8 para naturalidade
├─ Sampler: dpmpp_2m_sde      ← Recomendado
└─ Scheduler: karras           ← Padrão recomendado
```

### Passo 6: Executar Pipeline

1. Clique em **"Queue Prompt"** (lado direito)
2. Aguarde processamento (2-5 minutos com SDXL-Turbo)
3. Veja progresso no console

### Passo 7: Obter Resultados

Resultados salvos em:
```
outputs/ecommerce/
├── seu_produto_carousel_01.jpg
├── seu_produto_carousel_02.jpg
├── seu_produto_carousel_03.jpg
└── seu_produto_carousel_04.jpg
```

---

## 🎨 Fluxo Avançado

### Customizar Completamente

#### 1. Criar Novo Node de Prompt

```
CLIP Text Encode (Positive) - Novo node
├─ Texto: Seu prompt customizado
└─ Conectar a: KSampler -> positive
```

**Prompts Recomendados por Tipo de Produto:**

**Para Cubas (Sinks):**
```
luxurious bathroom with modern black sink, 
waterfall faucet, marble vanity, professional 
product photography, studio lighting, 8k resolution, 
trending on behance
```

**Para Sanitários:**
```
premium bathroom design, white ceramic toilet, 
modern fixtures, clean lines, luxury home interior, 
professional photography, warm lighting, 4k
```

**Para Pias (Wash Basins):**
```
contemporary bathroom interior, vessel sink, 
bronze or gold faucet, granite countertop, 
professional architectural photography, 
daylight, minimalist aesthetic
```

#### 2. Adicionar ControlNet (Opcional)

Para precisão de posicionamento:

```
Load ControlNet Model
↓
Apply ControlNet (conectar à imagem)
↓
KSampler (com ControlNet)
```

**ControlNets Úteis:**
- **Depth**: Mantém profundidade e perspectiva
- **Canny**: Preserva bordas do produto
- **OpenPose**: Posicionamento específico

#### 3. Aumentar Qualidade

Para SDXL (não SDXL-Turbo):

```
Sampler Config:
├─ Model: SDXL (não turbo)
├─ Steps: 50                ← Aumentado
├─ CFG: 7.5
├─ Sampler: dpmpp_2m_sde_karras
└─ Denoise: 1.0
```

**Tempo esperado:** 8-12 minutos

---

## 🔄 Processamento em Lote

Para múltiplos produtos:

### Método 1: Batch Processor Script

```bash
python scripts/batch_processor.py \
  --input inputs/products \
  --output outputs/ecommerce \
  --variations 4 \
  --quality ALTA
```

**O script:**
1. ✓ Encontra todas as imagens em inputs/products/
2. ✓ Cria metadados para cada produto
3. ✓ Gera instruções de processamento
4. ✓ Salva estrutura em outputs/

### Método 2: Processamento Manual

Para cada produto:

1. Abra `main_pipeline.json`
2. Edite node 1 com nova imagem
3. Altere seeds dos samplers
4. Execute
5. Salve resultados com novo nome

**Dica:** Use números nas imagens:
```
cuba_01.jpg → cuba_01_carousel.jpg
cuba_02.jpg → cuba_02_carousel.jpg
```

---

## 📦 Otimização para E-commerce

### 1. Usar Image Optimizer

```bash
python scripts/image_optimizer.py \
  --input outputs/ecommerce \
  --output outputs/optimized
```

**Gera automaticamente:**
```
optimized/
├── mercado_livre/
│   ├── produto_800x800.jpg
│   ├── produto_1080x1080.jpg
│   └── produto_1600x1600.jpg
├── shopee/
│   ├── produto_600x600.jpg
│   ├── produto_800x800.jpg
│   └── produto_1080x1080.jpg
├── amazon/
│   ├── produto_1200x1200.jpg
│   └── produto_1600x1600.jpg
└── webp/
    ├── produto_800x800.webp
    └── produto_1080x1080.webp
```

### 2. Teste em Plataformas Reais

**Mercado Livre:**
- Resolução: 1080x1080px ideal
- Formato: JPEG 85% qualidade
- Tamanho: Até 10MB por imagem (relaxado)

**Shopee:**
- Resolução: 800x800px ou 1080x1080px
- Formato: JPEG ou PNG
- Tamanho: Até 5MB por imagem

**Amazon:**
- Resolução mínima: 1200x1200px
- Formato: JPEG recomendado
- Tamanho: Até 10MB por imagem

### 3. Verificação de Qualidade

```
Checklist de Qualidade:
□ Produto preservado 100% (sem alterações)
□ Sem artefatos visíveis de IA
□ Iluminação realista
□ Cores naturais
□ Ambiente coerente com produto
□ Texto legível (se houver metadados)
□ Dimensões corretas (1080x1080 ideal)
```

---

## 📐 Adição de Dimensões

### Passo 1: Prepare Arquivo de Dimensões

Crie `inputs/dimensions/dimensions.json`:

```json
{
  "cuba_preta_01": {
    "Comprimento": "65 cm",
    "Profundidade": "45 cm",
    "Altura": "15 cm",
    "Capacidade": "25 litros",
    "Material": "Cerâmica",
    "Acabamento": "Preto Fosco"
  },
  "pia_marmore_02": {
    "Comprimento": "80 cm",
    "Profundidade": "50 cm",
    "Altura": "20 cm",
    "Peso": "35 kg",
    "Material": "Mármore Branco",
    "Acabamento": "Polido"
  }
}
```

### Passo 2: Execute Dimension Overlay

```bash
python scripts/dimension_overlay.py \
  --images outputs/ecommerce \
  --dimensions inputs/dimensions/dimensions.json \
  --output outputs/with_dimensions
```

### Passo 3: Resultados

Gera dois tipos:

**1. Imagem com Rodapé (Footer):**
```
cuba_preta_01_com_dimensoes.jpg
└─ Dimensões no rodapé da imagem
```

**2. Infografia Separada:**
```
cuba_preta_01_infografia.jpg
└─ Infográfico bonito e profissional
```

---

## 🎯 Fluxo Completo Recomendado

```
1. ENTRADA
   └─ Imagens em inputs/products/

2. PROCESSAMENTO COMFYUI
   ├─ Carregar main_pipeline.json
   ├─ Editar node 1 (imagem)
   ├─ Ajustar prompts (opcional)
   └─ Queue Prompt

3. BATCH PROCESSING (opcional)
   └─ python scripts/batch_processor.py

4. OTIMIZAÇÃO
   └─ python scripts/image_optimizer.py

5. ADIÇÃO DE DIMENSÕES (opcional)
   └─ python scripts/dimension_overlay.py

6. SAÍDA
   ├─ outputs/ecommerce/      (básico)
   ├─ outputs/optimized/      (por plataforma)
   └─ outputs/with_dimensions/(com especificações)
```

---

## ⏱️ Tempo Estimado

| Operação | SDXL-Turbo | SDXL | SDXL (SLOW) |
|----------|-----------|------|-----------|
| 1 produto, 4 variações | 2-3 min | 8-10 min | 15-20 min |
| 10 produtos, 4 var | 20-30 min | 80-100 min | 150-200 min |
| + Otimização | +2 min | +2 min | +2 min |
| + Dimensões | +1 min | +1 min | +1 min |

---

## 💾 Organizar Resultados

**Estrutura Recomendada:**

```
Campanha_Banheiros_2026/
├── 01_Cubas/
│   ├── cuba_preta/
│   │   ├── carousel/
│   │   │   ├── 01.jpg
│   │   │   ├── 02.jpg
│   │   │   ├── 03.jpg
│   │   │   └── 04.jpg
│   │   ├── otimizado/
│   │   │   ├── mercado_livre/
│   │   │   ├── shopee/
│   │   │   └── amazon/
│   │   └── dimensoes.jpg
│   └── cuba_branca/
│       └── (mesma estrutura)
├── 02_Sanitarios/
│   └── (mesma estrutura)
└── 03_Pias/
    └── (mesma estrutura)
```

---

## 🆘 Troubleshooting Rápido

**Problema:** Produto aparece distorcido
```
→ Verificar resolução entrada (512-2048px)
→ Reduzir ControlNet strength
→ Ver docs/TROUBLESHOOTING.md
```

**Problema:** Background sujo
```
→ Tentar semear diferente (novo seed)
→ Ajustar prompt negativo
→ Usar modo MANUAL se background específico
```

**Problema:** Imagem parece "IA"
```
→ Reduzir CFG (6-7)
→ Aumentar steps (40-50)
→ Usar SDXL em vez de SDXL-Turbo
```

---

Para ajuda completa, ver: `docs/TROUBLESHOOTING.md`
