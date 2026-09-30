#!/usr/bin/env python3
"""
Batch Processor - Vivazco Pipeline
Processa múltiplas imagens de produtos em lote
"""

import os
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
import subprocess

class BatchProcessor:
    """Processador em lote para Vivazco"""

    def __init__(self, input_dir, output_dir, variations=4, quality='ALTA'):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.variations = variations
        self.quality = quality
        self.processed = []
        self.failed = []

    def find_products(self):
        """Encontra todas as imagens de produtos"""
        supported_formats = ('*.jpg', '*.jpeg', '*.png', '*.webp')
        products = []

        for pattern in supported_formats:
            products.extend(self.input_dir.glob(pattern))

        return sorted(products)

    def validate_input(self):
        """Valida diretório de entrada"""
        if not self.input_dir.exists():
            print(f"❌ Diretório não encontrado: {self.input_dir}")
            return False

        products = self.find_products()
        if not products:
            print(f"❌ Nenhuma imagem encontrada em: {self.input_dir}")
            return False

        print(f"✓ {len(products)} imagem(ns) encontrada(s)")
        return True

    def prepare_pipeline_config(self, product_image):
        """Prepara configuração do pipeline para um produto"""
        product_name = product_image.stem

        config = {
            'product_name': product_name,
            'input_image': str(product_image),
            'variations': self.variations,
            'quality': self.quality,
            'output_dir': str(self.output_dir),
            'timestamp': datetime.now().isoformat(),
            'seeds': [42, 123, 456, 789, 1011][:self.variations]
        }

        return config

    def generate_product_metadata(self, product_image, config):
        """Gera metadados do produto"""
        metadata = {
            'produto': product_image.stem,
            'data_processamento': config['timestamp'],
            'variações_geradas': self.variations,
            'qualidade_output': self.quality,
            'resolução_final': '1080x1080',
            'formato': 'JPEG 85%',
            'imagem_original': str(product_image),
            'diretório_saída': str(self.output_dir),
            'seeds_utilizadas': config['seeds']
        }

        return metadata

    def process_product(self, product_image, index, total):
        """Processa um produto individual"""
        product_name = product_image.stem

        print(f"\n📸 Produto {index}/{total}: {product_name}")
        print(f"   📁 Entrada: {product_image}")

        try:
            # Preparar configuração
            config = self.prepare_pipeline_config(product_image)

            # Gerar metadados
            metadata = self.generate_product_metadata(product_image, config)

            # Salvar metadados
            metadata_file = self.output_dir / f"{product_name}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            print(f"   ✓ Configuração preparada")
            print(f"   ✓ Metadados salvos: {metadata_file.name}")

            # Aqui entraria integração com ComfyUI
            # Por enquanto, apenas criamos estrutura
            print(f"   ⏳ Pronto para processamento no ComfyUI")

            self.processed.append({
                'produto': product_name,
                'status': 'PRONTO',
                'metadados': str(metadata_file)
            })

            return True

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            self.failed.append({
                'produto': product_name,
                'erro': str(e)
            })
            return False

    def run(self):
        """Executa processamento em lote"""
        print("\n" + "="*60)
        print("🚀 VIVAZCO - BATCH PROCESSOR".center(60))
        print("="*60)

        # Validar entrada
        print("\n🔍 Validando entrada...")
        if not self.validate_input():
            return False

        # Criar diretório de saída
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Saída: {self.output_dir}")

        # Processar produtos
        products = self.find_products()
        total = len(products)

        print(f"\n📊 Processando {total} produto(s)...")
        print(f"   Variações: {self.variations}")
        print(f"   Qualidade: {self.quality}")

        for index, product in enumerate(products, 1):
            self.process_product(product, index, total)

        # Relatório final
        self.print_report()

        return len(self.failed) == 0

    def print_report(self):
        """Imprime relatório final"""
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE PROCESSAMENTO".center(60))
        print("="*60)

        print(f"\n✓ Processados com sucesso: {len(self.processed)}")
        print(f"❌ Falhas: {len(self.failed)}")

        if self.processed:
            print("\n✅ SUCESSO:")
            for item in self.processed:
                print(f"   • {item['produto']}")
                print(f"     Status: {item['status']}")
                print(f"     Metadados: {item['metadados']}")

        if self.failed:
            print("\n❌ FALHAS:")
            for item in self.failed:
                print(f"   • {item['produto']}: {item['erro']}")

        print("\n" + "="*60)
        print("PRÓXIMOS PASSOS:")
        print("="*60)
        print("""
1. Abra ComfyUI
2. Carregue pipeline/main_pipeline.json
3. Para cada produto processado:
   - Edite o caminho da imagem (Load Image node)
   - Ajuste os prompts conforme necessário
   - Clique "Queue Prompt"
4. Resultados estarão em outputs/ecommerce/
        """)
        print("="*60 + "\n")

def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description='Vivazco Batch Processor - Prepara múltiplos produtos'
    )

    parser.add_argument(
        '--input',
        type=str,
        default='inputs/products',
        help='Diretório de entrada (padrão: inputs/products)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='outputs/ecommerce',
        help='Diretório de saída (padrão: outputs/ecommerce)'
    )

    parser.add_argument(
        '--variations',
        type=int,
        default=4,
        choices=[3, 4, 5],
        help='Número de variações (padrão: 4)'
    )

    parser.add_argument(
        '--quality',
        type=str,
        default='ALTA',
        choices=['STANDARD', 'ALTA'],
        help='Qualidade de saída (padrão: ALTA)'
    )

    args = parser.parse_args()

    processor = BatchProcessor(
        input_dir=args.input,
        output_dir=args.output,
        variations=args.variations,
        quality=args.quality
    )

    success = processor.run()
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
