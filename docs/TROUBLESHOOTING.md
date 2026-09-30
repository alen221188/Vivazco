# TROUBLESHOOTING.md - Solução de Problemas

## 🔍 Problemas Comuns e Soluções

### ❌ ComfyUI não carrega o pipeline

**Erro:** "Invalid JSON" ou "Cannot load file"

**Soluções:**

1. Verificar caminho do arquivo
```bash
# Certifique-se que existe
ls -la pipeline/main_pipeline.json
```

2. Validar JSON
```bash
# Online: https://jsonlint.com/
# Ou usar Python:
python -c "import json; json.load(open('pipeline/main_pipeline.json'))"
```

3. Usar GUI do ComfyUI
   - Clique em "Load"
   - Selecione arquivo via diálogo
   - NÃO copie-cole caminhos

4. Atualizar ComfyUI
```bash
cd ComfyUI
git pull origin main
pip install -r requirements.txt
```

---

### ❌ Imagem não carrega no node 1

**Erro:** "Image not found" ou arquivo vazio

**Soluções:**

1. Verificar caminho
```bash
# Arquivo deve estar em:
ls -la inputs/products/seu_arquivo.jpg
```

2. Verificar formato
   - ✓ JPEG (.jpg, .jpeg)
   - ✓ PNG (.png)
   - ✓ WebP (.webp)
   - ✗ AVIF, HEIC (não suportados)

3. Tamanho de arquivo
   - ✓ Até 2MB por arquivo
   - ✗ Maior que 2MB = pode falhar

4. Resolução
   - ✓ Mínimo: 512x512px
   - ✓ Ideal: 1024x1024px ou 800x600px
   - ✗ Muito pequeno (<512px) = qualidade ruim

5. Re-upload
```
Node 1: Choose File → Browse → Selecione arquivo
Clique "Upload"
Aguarde "Image uploaded successfully"
```

---

### ❌ GPU Out of Memory (VRAM)

**Erro:** "CUDA out of memory" ou "OutOfMemoryError"

**GPU Mínima:** 12GB VRAM

**Soluções (em ordem):**

1. **Usar SDXL-Turbo** (padrão)
   - Muito mais eficiente que SDXL
   - 2-3 min vs 8-10 min
   - Usa ~6GB VRAM

2. **Desabilitar otimizações**
   - ComfyUI → Settings
   - Memory → Normal (não use "Aggressive")
   - Pode ganhar 1-2GB

3. **Reduzir resolução**
   ```
   ImageScale node: 1024 → 768
   ou até: 640 (economiza 50% VRAM)
   ```

4. **Reduzir steps**
   ```
   Sampler: steps 30 → 20
   Menos steps = mais rápido, menos VRAM
   ```

5. **Batch size = 1**
   ```
   Se tiver múltiplas imagens, processar uma por vez
   ```

6. **Fechar outros programas**
   ```bash
   # Liberar VRAM
   pkill -f "chrome\|firefox\|discord"
   # Reiniciar ComfyUI
   ```

7. **Atualizar drivers**
   ```bash
   # NVIDIA
   nvidia-driver-update
   
   # Também atualizar CUDA:
   pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

---

### ⚠️ Imagem parece distorcida ou feia

**Problema:** Produto não está bem formado, cores estranhas

**Causas Comuns:**

1. **Entrada ruim**
   - Imagem com fundo muito complexo
   - Resolução muito baixa (<512px)
   - Imagem muito borrenta

**Solução:**
```
- Use imagem de melhor qualidade
- Limpe o background manualmente
- Aumente resolução (se possível)
```

2. **Prompt inadequado**
```
Ruim: "a sink" (muito genérico)
Bom: "modern black ceramic sink, vessel style, matte finish"
Melhor: "luxury black matte ceramic sink, organic rounded shape, minimalist vessel design"
```

**Solução:**
```
- Edite prompts com mais detalhes
- Veja docs/PROMPTS.md para exemplos
```

3. **Sampler settings errados**

**Solução:**
```
Use configurações padrão:
├─ Sampler: dpmpp_2m_sde_karras
├─ Steps: 30 (SDXL-Turbo) ou 40-50 (SDXL)
├─ CFG: 7-7.5
└─ Scheduler: karras
```

4. **ControlNet muito forte**
```
Se usar ControlNet, reduzir strength:
├─ Começar com 0.5-0.7
├─ Aumentar gradualmente se necessário
└─ Máximo 0.9
```

---

### ❌ Produto aparece modificado (cores ou forma diferentes)

**CRÍTICO:** Isso não deve acontecer. Vivazco preserva produtos 100%.

**Causas:**

1. **Denoise muito alto**
```
Sampler: denoise 1.0 (máximo)
↓ Isso muda tudo!
Solução: reduzir a 0.5-0.7
```

2. **ControlNet danificando**
```
Se usar ControlNet:
- Testar sem ControlNet primeiro
- Se ControlNet causa problema, desabilitar
- Usar máximo 0.3 strength
```

3. **Prompt negativo muito forte**
```
Evite:
"no modifications, preserve original colors"
Isso pode fazer contrário!

Use:
"artifact, blur, distortion, low quality"
(defeitos a evitar, não modificações)
```

**Solução Definitiva:**
```
1. Remover ControlNet
2. Usar denoise = 0.5
3. Sampler padrão
4. Executar novamente
```

---

### 🌫️ Imagem parece "muito IA"

**Problema:** Resultado parece renderizado, não realista

**Causas:**

1. **CFG muito alto**
```
CFG 9-10: Parece IA forçado
CFG 7-7.5: Natural, realista
CFG 6: Mais criativo, menos aderente
```

**Solução:**
```
Testar CFG: 6.5, 7.0, 7.5 em sequência
Escolher mais natural
```

2. **Sampler errado**
```
Pior: heun (artefatos)
Bom: dpmpp_2m_sde
Melhor: dpmpp_2m_sde_karras (padrão)
```

3. **Não usar SDXL-Turbo**
```
SDXL-Turbo: parece mais natural
SDXL: pode ficar "plástico" se CFG alto
```

4. **Steps insuficientes**
```
20 steps: pode parecer IA
30 steps: normal
50+ steps: muito detalhado
```

**Solução Completa:**
```
1. CFG: 7.0
2. Sampler: dpmpp_2m_sde_karras
3. Scheduler: karras
4. Steps: 30-40
5. Model: SDXL-Turbo
6. Denoise: 0.75-0.95
```

---

### 💾 Erros ao salvar imagem

**Erro:** "Permission denied" ou "Cannot write file"

**Soluções:**

1. Verificar permissões
```bash
# Dar permissão de escrita
chmod -R 755 outputs/
```

2. Verificar espaço em disco
```bash
# Ver espaço livre
df -h

# Limpar cache se necessário
rm -rf ~/.cache/comfyui_*
```

3. Verificar pasta de saída
```bash
# Criar pasta se não existir
mkdir -p outputs/ecommerce

# Verificar se existe
ls -la outputs/
```

4. ComfyUI em modo read-only
```bash
# Reiniciar ComfyUI com permissões corretas
sudo python main.py
```

---

### 🎨 Cores incorretas na saída

**Problema:** Cores não correspondem ao original

**Causas:**

1. **Espaço de cor incorreto**
```
ComfyUI → Settings → Color Space
Certificar que está em: sRGB (padrão)
```

2. **VAE corrompido**
```
Solução: Usar VAE padrão SDXL
ou fazer re-download
```

3. **Prompt menciona cores erradas**
```
Verificar prompts (nodes 4, 10, 15, 20)
Se mencionar "gold" e quer "silver", corrigir
```

4. **Monitor/Display calibração**
```
Cores podem variar por monitor
Testar em múltiplos dispositivos
```

**Solução:**
```
1. Remover color mentions de prompts
2. Deixar IA inferir de imagem original
3. Usar SDXL VAE se disponível
4. Testar com CFG 6.5-7.0
```

---

### 📐 Dimensões erradas na saída

**Problema:** Imagem não é 1080x1080px como esperado

**Verificar:**

```bash
# Ver dimensões da imagem
identify seu_arquivo.jpg
# ou
file seu_arquivo.jpg
```

**Soluções:**

1. **Node ImageScale está certo?**
   - Verificar node 8, 13, 18, 23
   - Width: 1080
   - Height: 1080
   - Crop: center

2. **Imagem original distorcida?**
```
Se entrada era 512x800 (não quadrada)
Saída pode ser 1080x1440 (mantém proporção)

Solução: Fazer crop manual em entrada
ou editar node ImageScale: crop = "fill"
```

3. **Output diferente do esperado**
```bash
# Redimensionar manualmente
python scripts/image_optimizer.py \
  --input outputs/ecommerce \
  --output outputs/fixed
```

---

### 🔄 Batch Processor não funciona

**Erro:** "No images found" ou "FileNotFoundError"

**Soluções:**

1. Verificar pasta
```bash
ls -la inputs/products/
# Deve ter arquivos .jpg, .png, etc
```

2. Verificar permissões
```bash
chmod 755 inputs/products/*
```

3. Testar manualmente
```bash
python -c "
from pathlib import Path
p = Path('inputs/products')
print(f'Pasta existe: {p.exists()}')
imgs = list(p.glob('*.jpg'))
print(f'Imagens: {len(imgs)}')
for img in imgs:
    print(f'  - {img.name}')
"
```

4. Executar com caminho absoluto
```bash
python scripts/batch_processor.py \
  --input /caminho/completo/inputs/products \
  --output /caminho/completo/outputs/ecommerce
```

---

### 🐍 Erros Python

**"ModuleNotFoundError: No module named 'PIL'"**
```bash
pip install Pillow
```

**"ModuleNotFoundError: No module named 'numpy'"**
```bash
pip install numpy
```

**"ModuleNotFoundError: No module named 'cv2'"**
```bash
pip install opencv-python
```

**Instalar tudo de uma vez:**
```bash
pip install -r requirements.txt
```

---

### 🌐 ComfyUI não inicia

**Erro:** Porta 8188 já em uso ou não inicia

**Soluções:**

1. **Porta já em uso**
```bash
# Encontrar processo
lsof -i :8188
# Matar processo
kill -9 PID

# Ou usar porta diferente
python main.py --listen 0.0.0.0 --port 8189
```

2. **Dependências faltando**
```bash
cd ComfyUI
pip install -r requirements.txt
```

3. **GPU drivers desatualizados**
```bash
# NVIDIA
nvidia-smi  # ver versão
# Atualizar se necessário

# AMD (se usando)
rocm-smi
```

---

## 📞 Precisa de Ajuda?

### Antes de Relatar Issue:

1. ✓ Verificar este documento
2. ✓ Ver `docs/WORKFLOW.md`
3. ✓ Executar `python scripts/setup.py` novamente
4. ✓ Testar com imagem de exemplo
5. ✓ Ver logs de ComfyUI

### Ao Relatar Issue:

Incluir:
- [ ] Descrição clara do problema
- [ ] Mensagem de erro completa
- [ ] Caminho da imagem
- [ ] Screenshot se possível
- [ ] Configuração de hardware (GPU, VRAM, etc)
- [ ] Versão de ComfyUI e Python

### Recursos:

- **ComfyUI Issues**: https://github.com/comfyanonymous/ComfyUI/issues
- **Community Discord**: https://discord.gg/comfyui
- **Stability AI Docs**: https://platform.stability.ai/docs/

---

**Última atualização:** 2026-09-30  
**Contribuições:** Bem-vindas via GitHub Issues
