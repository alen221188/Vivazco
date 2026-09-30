#!/usr/bin/env python3
"""
Setup Script - Vivazco Pipeline
Cria estrutura de pastas e valida ambiente
"""

import os
import sys
from pathlib import Path

def setup_directories():
    """Cria todas as pastas necessárias"""
    base_dir = Path(__file__).parent.parent

    directories = [
        'pipeline',
        'models/checkpoints',
        'models/vae',
        'models/loras',
        'models/controlnets',
        'inputs/products',
        'inputs/references',
        'inputs/dimensions',
        'outputs/carousel',
        'outputs/variations',
        'outputs/ecommerce',
        'scripts',
        'docs',
        '.gitkeep'
    ]

    print("🔧 Criando estrutura de pastas...\n")

    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        status = "✓" if dir_path.exists() else "✗"
        print(f"  {status} {directory}/")

    print("\n✅ Estrutura de pastas criada com sucesso!")
    return True

def check_requirements():
    """Verifica dependências Python"""
    print("\n🔍 Verificando requisitos...\n")

    required_modules = {
        'PIL': 'Pillow',
        'numpy': 'NumPy',
        'cv2': 'OpenCV'
    }

    missing = []

    for module, package_name in required_modules.items():
        try:
            __import__(module)
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ✗ {package_name} (não encontrado)")
            missing.append(package_name)

    if missing:
        print(f"\n⚠️  Pacotes faltando: {', '.join(missing)}")
        print(f"\nInstale com:")
        print(f"  pip install {' '.join(missing)}")
        return False

    print("\n✅ Todos os requisitos estão OK!")
    return True

def create_gitignore():
    """Cria arquivo .gitignore apropriado"""
    print("\n📝 Criando .gitignore...\n")

    base_dir = Path(__file__).parent.parent
    gitignore_path = base_dir / '.gitignore'

    gitignore_content = """# Modelos (muito grandes)
models/checkpoints/*
models/vae/*
models/loras/*
models/controlnets/*
!models/checkpoints/.gitkeep
!models/vae/.gitkeep
!models/loras/.gitkeep
!models/controlnets/.gitkeep

# Outputs temporários
outputs/carousel/*
outputs/variations/*
outputs/ecommerce/*
!outputs/carousel/.gitkeep
!outputs/variations/.gitkeep
!outputs/ecommerce/.gitkeep

# Cache e temp
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
"""

    gitignore_path.write_text(gitignore_content)
    print(f"  ✓ {gitignore_path.name} criado")
    print("\n✅ Configuração Git OK!")

def create_requirements():
    """Cria arquivo requirements.txt"""
    print("\n📋 Criando requirements.txt...\n")

    base_dir = Path(__file__).parent.parent
    requirements_path = base_dir / 'requirements.txt'

    requirements_content = """# Vivazco Pipeline Requirements
# Python 3.8+

# Image Processing
Pillow>=10.0.0
numpy>=1.24.0
opencv-python>=4.8.0

# Optional: ComfyUI Integration
# (ComfyUI deve ser instalado separadamente)

# Utilities
python-dotenv>=1.0.0
tqdm>=4.65.0

# Development (opcional)
black>=23.0.0
pytest>=7.4.0
"""

    requirements_path.write_text(requirements_content)
    print(f"  ✓ {requirements_path.name} criado")
    print("\nInstale com: pip install -r requirements.txt")

def print_instructions():
    """Imprime instruções finais"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETO!")
    print("="*60)

    print("""
PRÓXIMOS PASSOS:

1. 📦 Instale dependências Python:
   pip install -r requirements.txt

2. 📊 Copie seus modelos ComfyUI:
   - SDXL ou SDXL-Turbo → models/checkpoints/
   - VAE (opcional) → models/vae/
   - ControlNets (opcional) → models/controlnets/

3. 📸 Prepare imagens de produto:
   - Coloque em: inputs/products/
   - Formatos: JPEG, PNG, WebP
   - Resolução: 512px a 2048px

4. 🚀 Abra ComfyUI e carregue:
   - File → Load → pipeline/main_pipeline.json

5. ⚙️ Configure o pipeline:
   - Edite os prompts conforme necessário
   - Ajuste seeds para variações
   - Selecione modelo base (SDXL-Turbo recomendado)

6. ▶️ Execute:
   - Click em "Queue Prompt"
   - Resultados em: outputs/ecommerce/

DOCUMENTAÇÃO:
- CLAUDE.md: Documentação técnica completa
- README.md: Guia rápido
- docs/WORKFLOW.md: Passo-a-passo detalhado
- docs/PROMPTS.md: Biblioteca de prompts

SUPORTE:
Veja docs/TROUBLESHOOTING.md para problemas comuns.

""")

    print("="*60)
    print("Bom trabalho! 🎨")
    print("="*60 + "\n")

def main():
    """Executa setup completo"""
    print("\n" + "🚀 VIVAZCO - BATHROOM FIXTURES PIPELINE".center(60))
    print("Setup Script v1.0.0".center(60) + "\n")

    try:
        # Criar pastas
        if not setup_directories():
            sys.exit(1)

        # Criar arquivos de configuração
        create_gitignore()
        create_requirements()

        # Verificar requisitos
        if not check_requirements():
            print("\n⚠️  Instale os pacotes faltando com:")
            print("  pip install -r requirements.txt")

        # Instruções finais
        print_instructions()

        return 0

    except Exception as e:
        print(f"\n❌ Erro durante setup: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
