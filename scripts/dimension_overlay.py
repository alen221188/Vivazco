#!/usr/bin/env python3
"""
Dimension Overlay - Vivazco Pipeline
Adiciona dimensões e croquis às imagens (opcional)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess

class DimensionOverlay:
    """Adiciona dimensões e croquis às imagens"""

    def __init__(self, image_dir, dimensions_file, output_dir):
        self.image_dir = Path(image_dir)
        self.dimensions_file = Path(dimensions_file)
        self.output_dir = Path(output_dir)
        self.dimensions_data = {}

    def load_dimensions(self):
        """Carrega arquivo de dimensões"""
        if not self.dimensions_file.exists():
            print(f"❌ Arquivo de dimensões não encontrado: {self.dimensions_file}")
            return False

        try:
            with open(self.dimensions_file, 'r', encoding='utf-8') as f:
                self.dimensions_data = json.load(f)

            print(f"✓ Dimensões carregadas: {len(self.dimensions_data)} produtos")
            return True

        except Exception as e:
            print(f"❌ Erro ao carregar dimensões: {e}")
            return False

    def add_dimension_text(self, image_path, product_name, dimensions):
        """Adiciona texto de dimensões à imagem"""
        try:
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)

            # Tentar usar fonte padrão
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
                font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
            except:
                font = ImageFont.load_default()
                font_small = ImageFont.load_default()

            # Fundo semi-transparente para legibilidade
            width, height = img.size
            footer_height = 120

            # Criar overlay
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)

            # Fundo branco semi-transparente no rodapé
            overlay_draw.rectangle(
                [(0, height - footer_height), (width, height)],
                fill=(240, 240, 240, 220)
            )

            # Adicionar dimensões
            y_offset = height - footer_height + 15

            # Título
            overlay_draw.text(
                (20, y_offset),
                f"Dimensões - {product_name}",
                font=font,
                fill=(0, 0, 0, 255)
            )

            y_offset += 40

            # Dimensões individuais
            if isinstance(dimensions, dict):
                for key, value in dimensions.items():
                    text = f"{key}: {value}"
                    overlay_draw.text(
                        (20, y_offset),
                        text,
                        font=font_small,
                        fill=(60, 60, 60, 255)
                    )
                    y_offset += 25

            # Mesclar overlay
            img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

            return img

        except Exception as e:
            print(f"   ❌ Erro ao adicionar dimensões: {e}")
            return None

    def create_dimension_infographic(self, product_name, dimensions):
        """Cria infográfico com dimensões"""
        try:
            # Criar imagem branca
            width, height = 600, 400
            img = Image.new('RGB', (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(img)

            # Carregar fonte
            try:
                font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
                font_text = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
                font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
            except:
                font_title = ImageFont.load_default()
                font_text = ImageFont.load_default()
                font_small = ImageFont.load_default()

            # Desenhar header
            draw.rectangle([(0, 0), (width, 80)], fill=(33, 150, 243))
            draw.text(
                (20, 20),
                f"ESPECIFICAÇÕES - {product_name}",
                font=font_title,
                fill=(255, 255, 255)
            )

            # Desenhar dimensões
            y = 120
            if isinstance(dimensions, dict):
                for idx, (key, value) in enumerate(dimensions.items()):
                    # Background alternado
                    if idx % 2 == 0:
                        draw.rectangle([(10, y-5), (width-10, y+35)], fill=(245, 245, 245))

                    # Texto
                    draw.text(
                        (30, y),
                        f"• {key}:",
                        font=font_text,
                        fill=(0, 0, 0)
                    )
                    draw.text(
                        (300, y),
                        str(value),
                        font=font_text,
                        fill=(33, 150, 243)
                    )

                    y += 45

            # Footer
            draw.line([(10, height-40), (width-10, height-40)], fill=(200, 200, 200))
            draw.text(
                (20, height-30),
                "Vivazco - Bathroom Fixtures",
                font=font_small,
                fill=(100, 100, 100)
            )

            return img

        except Exception as e:
            print(f"   ❌ Erro ao criar infográfico: {e}")
            return None

    def process_image(self, image_path):
        """Processa uma imagem adicionando dimensões"""
        product_name = image_path.stem

        if product_name not in self.dimensions_data:
            print(f"   ⚠️  Sem dimensões para: {product_name}")
            return False

        print(f"\n📐 {product_name}")
        dimensions = self.dimensions_data[product_name]

        # Adicionar dimensões à imagem
        img_with_dims = self.add_dimension_text(image_path, product_name, dimensions)
        if img_with_dims:
            output_path = self.output_dir / f"{product_name}_com_dimensoes.jpg"
            img_with_dims.save(output_path, 'JPEG', quality=90)
            print(f"   ✓ Salvo: {output_path.name}")

        # Criar infográfico
        infographic = self.create_dimension_infographic(product_name, dimensions)
        if infographic:
            output_path = self.output_dir / f"{product_name}_infografia.jpg"
            infographic.save(output_path, 'JPEG', quality=90)
            print(f"   ✓ Infografia: {output_path.name}")

        return True

    def run(self):
        """Executa adição de dimensões"""
        print("\n" + "="*60)
        print("📐 VIVAZCO - DIMENSION OVERLAY".center(60))
        print("="*60)

        # Validar inputs
        if not self.image_dir.exists():
            print(f"\n❌ Diretório não encontrado: {self.image_dir}")
            return False

        if not self.load_dimensions():
            return False

        # Criar diretório de saída
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Saída: {self.output_dir}")

        # Processar imagens
        images = list(self.image_dir.glob('*.jpg')) + list(self.image_dir.glob('*.jpeg'))

        if not images:
            print(f"❌ Nenhuma imagem encontrada em: {self.image_dir}")
            return False

        print(f"\n🔄 Processando {len(images)} imagem(ns)...")

        for image in images:
            self.process_image(image)

        self.print_summary()
        return True

    def print_summary(self):
        """Imprime resumo"""
        print("\n" + "="*60)
        print("✅ OVERLAY COMPLETO".center(60))
        print("="*60)

        print("\n📁 Arquivos gerados em:")
        print(f"   {self.output_dir}")

        if self.output_dir.exists():
            files = list(self.output_dir.glob('*.jpg'))
            print(f"\n📊 Total: {len(files)} arquivo(s)")
            for f in files:
                print(f"   • {f.name}")

        print("\n" + "="*60)
        print("PRÓXIMOS PASSOS:")
        print("="*60)
        print("""
1. Verifique as imagens geradas
2. Ajuste estilos/cores conforme necessário
3. Combine com outras imagens do carrossel
4. Faça upload para plataformas de e-commerce
        """)
        print("="*60 + "\n")

def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description='Vivazco Dimension Overlay - Adiciona dimensões às imagens'
    )

    parser.add_argument(
        '--images',
        type=str,
        default='outputs/ecommerce',
        help='Diretório com imagens'
    )

    parser.add_argument(
        '--dimensions',
        type=str,
        default='inputs/dimensions/dimensions.json',
        help='Arquivo JSON com dimensões'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='outputs/with_dimensions',
        help='Diretório de saída'
    )

    args = parser.parse_args()

    overlay = DimensionOverlay(
        image_dir=args.images,
        dimensions_file=args.dimensions,
        output_dir=args.output
    )

    success = overlay.run()
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
