#!/usr/bin/env python3
"""
Image Optimizer - Vivazco Pipeline
Otimiza imagens para diferentes plataformas e-commerce
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image, ImageOps
import json

class ImageOptimizer:
    """Otimizador de imagens para e-commerce"""

    # Configurações por plataforma
    PLATFORM_CONFIGS = {
        'mercado_livre': {
            'resolutions': [(800, 800), (1080, 1080), (1600, 1600)],
            'quality': 85,
            'format': 'JPEG',
            'max_size_kb': 500
        },
        'shopee': {
            'resolutions': [(600, 600), (800, 800), (1080, 1080)],
            'quality': 80,
            'format': 'JPEG',
            'max_size_kb': 400
        },
        'amazon': {
            'resolutions': [(1200, 1200), (1600, 1600)],
            'quality': 90,
            'format': 'JPEG',
            'max_size_kb': 800
        },
        'wix': {
            'resolutions': [(800, 600), (1200, 900), (1600, 1200)],
            'quality': 85,
            'format': 'JPEG',
            'max_size_kb': 500
        },
        'webp': {
            'resolutions': [(800, 800), (1080, 1080)],
            'quality': 80,
            'format': 'WEBP',
            'max_size_kb': 300
        }
    }

    def __init__(self, input_dir, output_dir):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.optimized = []

    def find_images(self):
        """Encontra todas as imagens"""
        supported = ('*.jpg', '*.jpeg', '*.png', '*.webp')
        images = []
        for pattern in supported:
            images.extend(self.input_dir.glob(pattern))
        return sorted(images)

    def optimize_image(self, image_path, output_path, width, height, quality, fmt):
        """Otimiza uma imagem para dimensões e formato específicos"""
        try:
            img = Image.open(image_path)

            # Converter para RGB se necessário
            if img.mode in ('RGBA', 'LA', 'P'):
                # Criar background branco
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Redimensionar com aspecto mantido
            img = ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS)

            # Salvar
            output_path.parent.mkdir(parents=True, exist_ok=True)
            save_kwargs = {'quality': quality, 'optimize': True}

            if fmt.lower() == 'webp':
                img.save(output_path, 'WEBP', quality=quality)
            else:
                img.save(output_path, 'JPEG', **save_kwargs)

            return True

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return False

    def process_image(self, image_path):
        """Processa uma imagem para todas as plataformas"""
        image_name = image_path.stem
        results = []

        print(f"\n🖼️  {image_name}")

        for platform, config in self.PLATFORM_CONFIGS.items():
            platform_dir = self.output_dir / platform
            platform_dir.mkdir(parents=True, exist_ok=True)

            print(f"   📦 {platform}:")

            for width, height in config['resolutions']:
                filename = f"{image_name}_{width}x{height}.{config['format'].lower()}"
                output_path = platform_dir / filename

                if self.optimize_image(image_path, output_path, width, height,
                                      config['quality'], config['format']):
                    size_kb = output_path.stat().st_size / 1024
                    status = "✓" if size_kb <= config['max_size_kb'] else "⚠️"
                    print(f"      {status} {width}x{height} ({size_kb:.1f}KB)")

                    results.append({
                        'platform': platform,
                        'resolution': f"{width}x{height}",
                        'file': str(output_path),
                        'size_kb': round(size_kb, 2),
                        'max_kb': config['max_size_kb']
                    })

        return results

    def run(self):
        """Executa otimização"""
        print("\n" + "="*60)
        print("🚀 VIVAZCO - IMAGE OPTIMIZER".center(60))
        print("="*60)

        images = self.find_images()
        if not images:
            print(f"\n❌ Nenhuma imagem encontrada em: {self.input_dir}")
            return False

        print(f"\n📊 Otimizando {len(images)} imagem(ns)...")
        print(f"   📁 Entrada: {self.input_dir}")
        print(f"   📁 Saída: {self.output_dir}")
        print(f"\n   Plataformas: {', '.join(self.PLATFORM_CONFIGS.keys())}")

        for image in images:
            results = self.process_image(image)
            self.optimized.extend(results)

        self.print_summary()
        return True

    def print_summary(self):
        """Imprime resumo de otimização"""
        print("\n" + "="*60)
        print("✅ OTIMIZAÇÃO COMPLETA".center(60))
        print("="*60)

        print(f"\n📊 Total de imagens geradas: {len(self.optimized)}")

        by_platform = {}
        for item in self.optimized:
            platform = item['platform']
            if platform not in by_platform:
                by_platform[platform] = []
            by_platform[platform].append(item)

        for platform, items in by_platform.items():
            total_size = sum(item['size_kb'] for item in items)
            print(f"\n📦 {platform.upper()}:")
            print(f"   Imagens: {len(items)}")
            print(f"   Tamanho total: {total_size:.1f}KB")
            for item in items:
                warning = " ⚠️" if item['size_kb'] > item['max_kb'] else ""
                print(f"   • {item['resolution']}: {item['size_kb']}KB{warning}")

        print("\n" + "="*60)
        print("ESTRUTURA DE SAÍDA:")
        print("="*60)

        for platform in self.PLATFORM_CONFIGS.keys():
            print(f"\n{platform}/")
            platform_dir = self.output_dir / platform
            if platform_dir.exists():
                for img in sorted(platform_dir.glob('*')):
                    size_mb = img.stat().st_size / (1024 * 1024)
                    print(f"  └─ {img.name} ({size_mb:.2f}MB)")

        print("\n" + "="*60)
        print("DICAS:")
        print("="*60)
        print("""
1. Use as imagens otimizadas para cada plataforma
2. WebP oferece melhor compressão (use se a plataforma suportar)
3. Verifique tamanhos em produção (alguns hosts têm limites)
4. Teste em mobile - resolução é importante para UX

PRÓXIMAS PLATAFORMAS A ADICIONAR:
- Instagram Shopping
- Facebook Catalog
- Pinterest Buyable Pins
- TikTok Shop
        """)
        print("="*60 + "\n")

def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description='Vivazco Image Optimizer - Otimiza para e-commerce'
    )

    parser.add_argument(
        '--input',
        type=str,
        default='outputs/ecommerce',
        help='Diretório de entrada (padrão: outputs/ecommerce)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='outputs/optimized',
        help='Diretório de saída (padrão: outputs/optimized)'
    )

    args = parser.parse_args()

    optimizer = ImageOptimizer(
        input_dir=args.input,
        output_dir=args.output
    )

    success = optimizer.run()
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
