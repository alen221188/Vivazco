# Vivazco - ComfyUI Bathroom Fixtures Pipeline

## Visão Geral do Projeto

Pipeline ComfyUI especializado para criar renderizações profissionais de louças de banheiro em ambientes luxuosos. O sistema preserva as características originais dos produtos enquanto os insere estrategicamente em cenários sofisticados, gerando múltiplas variações otimizadas para e-commerce.

## Objetivos Principais

- ✅ Processar imagens de produtos (com/sem background)
- ✅ Gerar ambientes luxuosos coerentes
- ✅ Manter fidelidade 100% às características do produto
- ✅ Garantir realismo natural em luz, sombra e texturas
- ✅ Produzir carrosséis de múltiplas variações
- ✅ Incluir dimensões e croquis (opcional)
- ✅ Otimizar para e-commerce (Mercado Livre, Shopee)

## Arquitetura do Pipeline

### Fluxo Principal de Processamento

```
1. INPUT: Imagem do Produto
   ├─ Detecção de background (com/sem)
   └─ Extração/Isolamento do produto

2. PROCESSAMENTO: Análise e Preparação
   ├─ Mapeamento de dimensões
   ├─ Análise de características (cor, material, forma)
   └─ Geração de máscara de produto

3. GERAÇÃO: Criação de Cenários Luxuosos
   ├─ Geração de ambiente base (ComfyUI nodes)
   ├─ Condicionamento estético (prompt sophisticated)
   └─ Variações de iluminação (3-5 versões)

4. COMPOSIÇÃO: Inserção Realista do Produto
   ├─ Posicionamento estratégico
   ├─ Ajuste de iluminação e sombras
   ├─ Matching de reflexos e brilhos
   └─ Blend natural com background

5. REFINAMENTO: Pós-processamento
   ├─ Ajuste de cores e contraste
   ├─ Detalhe de texturas
   └─ Compressão otimizada para e-commerce

6. SAÍDA: Múltiplas Variações
   ├─ Carrossel 3-5 ângulos/iluminações
   ├─ Dimensões padrão e-commerce
   ├─ Croquis dimensional (opcional)
   └─ Metadados de produto
```

## Estrutura de Pastas

```
Vivazco/
├── CLAUDE.md (este arquivo)
├── README.md
├── pipeline/
│   ├── main_pipeline.json          # Pipeline principal ComfyUI
│   ├── product_extraction.json     # Subnodo: extração de produto
│   ├── environment_generation.json # Subnodo: geração de ambiente
│   └── composition_blend.json      # Subnodo: composição final
├── models/
│   ├── checkpoints/                # Modelos SDXL/SDXL-Turbo
│   ├── vae/                        # VAE para qualidade
│   ├── loras/                      # LoRAs específicas (opcional)
│   └── controlnets/                # ControlNet para posicionamento
├── inputs/
│   ├── products/                   # Imagens de produtos
│   ├── references/                 # Fotos de referência (ambientes)
│   └── dimensions/                 # Croquis e dimensões (opcional)
├── outputs/
│   ├── carousel/                   # Carrosseis gerados
│   ├── variations/                 # Variações por ângulo
│   └── ecommerce/                  # Otimizadas para plataformas
├── scripts/
│   ├── batch_processor.py          # Processamento em lote
│   ├── dimension_overlay.py        # Overlay de dimensões
│   └── image_optimizer.py          # Otimização para e-commerce
└── docs/
    ├── WORKFLOW.md                 # Guia passo-a-passo
    ├── PROMPTS.md                  # Biblioteca de prompts
    └── SETTINGS.md                 # Configurações recomendadas
```

## Tecnologias e Requisitos

### Core
- **ComfyUI**: Framework de processamento visual
- **SDXL/SDXL-Turbo**: Modelo base (rápido e qualidade)
- **ControlNet**: Posicionamento preciso de objetos
- **LoRA**: Refinamento estético (opcional)

### Processamento
- **Python 3.8+**: Scripts auxiliares
- **Pillow**: Processamento de imagem
- **NumPy**: Operações matriciais
- **OpenCV**: Detecção de bordas e masks

### Otimização E-commerce
- **Dimensões padrão**: 1080x1080, 800x800, 600x600
- **Formatos**: JPEG (85% qualidade), WebP
- **Compressão**: TinyPNG/TinyJPG workflow

## Fluxo de Trabalho Prático

### 1. Preparação de Entrada
```
usuario/ 
└── produto.jpg (512x512 a 2048x2048)
    └── Inserir em inputs/products/
```

### 2. Processamento no ComfyUI
```
Executar pipeline com:
- Modo background: AUTO-DETECT ou MANUAL
- Estilo ambiental: LUXURY (padrão) ou CONTEMPORARY
- Variações: 3-5 (carrossel)
- Incluir dimensões: SIM/NÃO
```

### 3. Geração Automática
```
Pipeline gera:
✓ 3-5 ângulos diferentes
✓ Iluminações variadas (frontal, lateral, destaque)
✓ Carrossel otimizado para e-commerce
✓ Croquis dimensional (se ativado)
```

### 4. Entrega Final
```
outputs/ecommerce/
├── produto_carousel_01.jpg
├── produto_carousel_02.jpg
├── produto_carousel_03.jpg
├── produto_dimensions.png (opcional)
└── produto_metadata.json
```

## Configurações Críticas

### Preservação de Produto
- **Isolamento**: Máscara precisa 100%
- **Cor**: Nenhuma alteração de pigmentação
- **Forma**: Preservação exata de proporções
- **Reflexos**: Manutenção de brilhos originais

### Ambiente Luxuoso
- **Materiais**: Granito, mármores, madeira premium
- **Iluminação**: Profissional (3-point lighting)
- **Detalhes**: Decoração sofisticada (plantas, toalhas, cosméticos)
- **Coesão**: Ambiente harmonioso com produto

### Qualidade de Saída
- **Resolução**: 1080x1080px mínimo (e-commerce)
- **Realismo**: Sem artefatos visíveis de IA
- **Consistência**: Carrossel coerente visualmente
- **Formato**: JPEG 85-90% ou WebP 80%

## Modelos Recomendados

### Modelos Base (Escolher 1)
```
1. SDXL 1.0 (Qualidade máxima, processamento mais lento)
2. SDXL-Turbo (Rápido, qualidade muito boa)
3. SDXL Lightning (Ultra-rápido, bom para iterações)
```

### ControlNets (Recomendados)
```
- OpenPose: Posicionamento (opcional)
- Depth: Profundidade e perspectiva
- Canny Edge: Estrutura de produto
```

### VAE (Para Qualidade)
```
- VAE SD 1.5 (melhor qualidade)
ou
- SDXL VAE (nativo)
```

## Workflow de Uso Diário

### Simples (Quick Mode)
```
1. Colocar imagem em inputs/products/
2. ComfyUI: Carregar pipeline
3. Ajustar: Cor ambiente, iluminação
4. Executar: Gerar variações
5. Salvar: Em outputs/ecommerce/
⏱️ Tempo: 2-5 minutos por produto
```

### Detalhado (Full Mode)
```
1. Análise de produto (dimensões, características)
2. Captura de referência de ambiente
3. Processamento em ComfyUI (com refinamentos)
4. Adição de metadados e dimensões
5. Otimização por plataforma (Mercado Livre, Shopee, etc)
6. Teste de visualização em mobile
⏱️ Tempo: 15-30 minutos por produto
```

## Performance e Otimização

### Recomendado
- **GPU**: NVIDIA RTX 3060 12GB mínimo
- **VRAM**: 12-24GB ideal
- **RAM**: 16GB mínimo

### Ajustes para Velocidade
```
- Usar SDXL-Turbo (2x mais rápido)
- Reduzir steps de geração (20-30 é suficiente)
- Usar batchsize 2-4
- Habilitar optimizações ComfyUI
```

## Próximos Passos

1. ✅ Criar estrutura de pastas
2. ⏳ Implementar pipeline principal ComfyUI
3. ⏳ Criar subnós especializados
4. ⏳ Desenvolver scripts Python auxiliares
5. ⏳ Documentar prompts otimizados
6. ⏳ Testar com produtos reais
7. ⏳ Otimizar performance
8. ⏳ Documentar guias finais

## Notas Importantes

⚠️ **Preservação de Produto**: O produto original NUNCA deve ser modificado em características, cores ou dimensões.

⚠️ **Realismo**: Evitar qualquer efeito que pareça "renderizado IA". Priorizar autenticidade.

⚠️ **E-commerce**: Sempre testar dimensões em plataformas reais antes de publicação.

⚠️ **Backup**: Manter imagens originais em backup seguro.

---

**Última atualização**: 2026-09-30  
**Status**: Pipeline em desenvolvimento  
**Responsável**: Claude Haiku 4.5
