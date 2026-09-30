# Vivazco - ComfyUI Bathroom Fixtures Pipeline

Transforme imagens de louças de banheiro em renderizações profissionais luxuosas para e-commerce.

![Status](https://img.shields.io/badge/status-development-yellow)
![ComfyUI](https://img.shields.io/badge/ComfyUI-ready-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## 🎯 O Que É

Vivazco é um pipeline ComfyUI especializado que converte imagens de produtos (louças, sanitários, cubas, pias) em renderizações realistas dentro de ambientes luxuosos, mantendo 100% fidelidade ao produto original e gerando múltiplas variações otimizadas para plataformas de e-commerce.

## ✨ Principais Características

- 🏆 **Preservação Total do Produto**: Nenhuma alteração em cor, dimensão ou característica
- 🎨 **Ambientes Luxuosos**: Cenários sofisticados com materiais premium
- 💡 **Iluminação Realista**: 3-point lighting profissional, sem parecer IA
- 📸 **Múltiplas Variações**: Carrosseis de 3-5 ângulos/iluminações
- 📦 **E-commerce Ready**: Otimizado para Mercado Livre, Shopee, etc
- 📐 **Dimensões Opcionais**: Croquis e especificações quando necessário
- ⚡ **Processamento Rápido**: SDXL-Turbo com batch processing

## 🚀 Quick Start

### 1. Setup Inicial

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/vivazco.git
cd vivazco

# Crie as pastas de entrada/saída
python scripts/setup.py

# Copie seus modelos ComfyUI
# Coloque em: models/checkpoints/, models/vae/, etc
```

### 2. Prepare a Imagem de Produto

```bash
# Coloque sua imagem em:
cp seu_produto.jpg inputs/products/

# Formatos suportados: JPEG, PNG, WebP
# Resolução recomendada: 512px a 2048px
# Com ou sem background (ambos suportados)
```

### 3. Execute o Pipeline

```bash
# Abra ComfyUI e carregue:
# pipeline/main_pipeline.json

# Configure:
# - Modo background: AUTO / MANUAL
# - Estilo ambiental: LUXURY / CONTEMPORARY
# - Variações: 3, 4 ou 5
# - Incluir dimensões: SIM / NÃO

# Clique em "Queue Prompt"
```

### 4. Obtenha os Resultados

```
outputs/ecommerce/
├── seu_produto_carousel_01.jpg
├── seu_produto_carousel_02.jpg
├── seu_produto_carousel_03.jpg
└── seu_produto_metadata.json
```

## 📋 Requisitos

### Hardware
- **GPU**: NVIDIA com 12GB+ VRAM (RTX 3060 ou melhor)
- **RAM**: 16GB mínimo
- **SSD**: 50GB espaço livre para modelos

### Software
- **ComfyUI**: Última versão
- **Python**: 3.8 ou superior
- **Dependencies**: Ver `requirements.txt`

## 📁 Estrutura do Projeto

```
Vivazco/
├── CLAUDE.md                    # Documentação técnica completa
├── README.md                    # Este arquivo
├── requirements.txt             # Dependências Python
├── pipeline/
│   ├── main_pipeline.json       # Pipeline principal
│   ├── product_extraction.json  # Extração de produto
│   ├── environment_gen.json     # Geração de ambiente
│   └── composition_blend.json   # Composição final
├── models/                      # (Não incluído - você adiciona)
│   ├── checkpoints/
│   ├── vae/
│   └── controlnets/
├── inputs/
│   ├── products/                # Suas imagens de produtos
│   ├── references/              # Fotos de referência
│   └── dimensions/              # Specs de dimensão
├── outputs/
│   ├── carousel/                # Carrosseis gerados
│   ├── variations/              # Variações por ângulo
│   └── ecommerce/               # Prontos para publicar
├── scripts/
│   ├── setup.py                 # Setup inicial
│   ├── batch_processor.py       # Processamento lote
│   ├── dimension_overlay.py     # Adiciona dimensões
│   └── image_optimizer.py       # Otimiza para e-commerce
└── docs/
    ├── WORKFLOW.md              # Passo a passo detalhado
    ├── PROMPTS.md               # Biblioteca de prompts
    ├── SETTINGS.md              # Configs recomendadas
    └── TROUBLESHOOTING.md       # Soluções de problemas
```

## 🎛️ Configuração do Pipeline

### Parâmetros Principais

| Parâmetro | Opções | Padrão | Descrição |
|-----------|--------|--------|-----------|
| Background Mode | AUTO / MANUAL | AUTO | Detecção automática ou manual |
| Ambiente Style | LUXURY / CONTEMPORARY | LUXURY | Tipo de cenário |
| Variações | 3 / 4 / 5 | 4 | Número de ângulos/iluminações |
| Inclui Dimensões | SIM / NÃO | NÃO | Adiciona croquis com medidas |
| Qualidade Output | ALTA / STANDARD | ALTA | Resolução final |
| Modelo Base | SDXL / SDXL-TURBO | SDXL-TURBO | Rápido vs. Qualidade |

### Prompts Recomendados

O pipeline inclui prompts pré-otimizados para diferentes estilos:

- **Luxury Bathroom**: Mármores, ouro, iluminação dramática
- **Contemporary Minimal**: Linhas limpas, luz natural
- **Spa-like**: Relaxante, tons neutros, plantas
- **Industrial Chic**: Concreto, metal, design moderno

Ver `docs/PROMPTS.md` para biblioteca completa.

## 🔧 Como Usar

### Cenário 1: Produto Sem Background

```
1. Coloque imagem em inputs/products/
2. ComfyUI detectará automaticamente
3. Extrairá a cuba/pia isoladamente
4. Criará ambiente ao redor
5. Gerará 4 variações (padrão)
```

### Cenário 2: Produto Com Background

```
1. Coloque imagem em inputs/products/
2. Selecione "MANUAL" mode se background específico importa
3. Ou deixe "AUTO" para extrair só o produto
4. Pipeline processará normalmente
```

### Cenário 3: Adicionar Dimensões

```
1. Prepare arquivo dimensions.json com specs
2. Coloque em inputs/dimensions/
3. Na configuração: ativar "Inclui Dimensões: SIM"
4. Pipeline adicionará croqui às imagens finais
```

### Cenário 4: Batch Processing

```bash
# Processar múltiplos produtos de uma vez
python scripts/batch_processor.py \
  --input inputs/products/ \
  --output outputs/ecommerce/ \
  --variations 4 \
  --quality ALTA
```

## 📊 Exemplos de Saída

### Carrossel de 4 Variações
```
Variação 1 (Frontal + Iluminação dramática)
└─ 1080x1080px, JPEG 85% qualidade

Variação 2 (Ângulo esquerdo + Luz natural)
└─ 1080x1080px, JPEG 85% qualidade

Variação 3 (Ângulo direito + Destaque)
└─ 1080x1080px, JPEG 85% qualidade

Variação 4 (Overhead + Contexto completo)
└─ 1080x1080px, JPEG 85% qualidade

+ Metadata JSON
  └─ Dimensões, cor, material, etc
```

## 🎓 Documentação Completa

Para documentação completa, ver:

- **CLAUDE.md**: Arquitetura técnica e decisões
- **docs/WORKFLOW.md**: Passo-a-passo detalhado
- **docs/PROMPTS.md**: Biblioteca de prompts customizáveis
- **docs/SETTINGS.md**: Configurações avançadas e otimizações
- **docs/TROUBLESHOOTING.md**: Solução de problemas comuns

## 🐛 Troubleshooting

### Produto aparece distorcido
```
→ Verificar resolução de entrada (512px-2048px ideal)
→ Ajustar ControlNet depth settings
→ Ver docs/TROUBLESHOOTING.md
```

### Background não sai limpo
```
→ Tentar modo MANUAL
→ Refinar máscara manualmente
→ Usar referência com background similar
```

### Imagem parece "muito IA"
```
→ Reduzir CFG Scale (6-7 é melhor que 7-10)
→ Aumentar steps (40-50)
→ Usar SDXL em vez de SDXL-TURBO
```

## 📈 Performance

### Tempo de Processamento (por produto)
```
SDXL-Turbo:    2-3 minutos (4 variações)
SDXL:          5-8 minutos (4 variações)
SDXL (SLOW):   12-15 minutos (qualidade máxima)
```

### Otimizações Recomendadas
- Usar batchsize 2-4
- Habilitar xFormers no ComfyUI
- Usar Memory Efficient Attention
- Reduzir resolution a 832px se necessário

## 🤝 Contribuindo

Melhorias e sugestões são bem-vindas!

1. Faça fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

MIT License - Ver LICENSE para detalhes

## 📞 Suporte

- **Issues**: GitHub Issues
- **Documentação**: Ver pasta `/docs`
- **Email**: suporte@vivazco.com

## 🙏 Agradecimentos

- ComfyUI community
- Stability AI (SDXL)
- Community de IA generativa

---

**Versão**: 1.0.0-dev  
**Última atualização**: 2026-09-30  
**Mantido por**: Claude Code

---

### Status do Desenvolvimento

- [x] Documentação arquitetônica
- [ ] Pipeline principal ComfyUI
- [ ] Scripts Python auxiliares
- [ ] Testes com produtos reais
- [ ] Otimização performance
- [ ] Documentação final completa

**Contribua**: Seu feedback ajuda a melhorar Vivazco!
