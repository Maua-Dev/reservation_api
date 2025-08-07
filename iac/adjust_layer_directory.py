import os
import shutil
import subprocess

# --- Configurações ---
# Define os nomes e caminhos principais que o script vai usar.
# Isso facilita a manutenção se um dia os nomes das pastas mudarem.
BUILD_DIRECTORY = "build"
PYTHON_TOP_LEVEL_DIR = os.path.join(BUILD_DIRECTORY, "python")
SHARED_CODE_SOURCE = "src/shared"
REQUIREMENTS_FILE = "requirements-layer.txt"

def adjust_layer_directory():
    """
    Prepara um diretório 'build' para uma Lambda Layer do AWS CDK.
    
    A função junta o código local compartilhado e as dependências externas (pip)
    na estrutura de pastas que a Lambda espera (/python).
    """

    # Garante que o build seja sempre limpo, removendo qualquer artefato antigo.
    if os.path.exists(BUILD_DIRECTORY):
        shutil.rmtree(BUILD_DIRECTORY)
    
    # Cria a estrutura de pastas 'build/python/src/'.
    # Isso é necessário para que os imports 'from src.shared...' funcionem na Lambda.
    shared_code_intermediate_dir = os.path.join(PYTHON_TOP_LEVEL_DIR, "src")
    os.makedirs(shared_code_intermediate_dir)

    # Copia o código compartilhado (de 'src/shared') para dentro da estrutura da Layer.
    # O resultado final será 'build/python/src/shared'.
    shared_code_dest = os.path.join(shared_code_intermediate_dir, os.path.basename(SHARED_CODE_SOURCE))
    shutil.copytree(SHARED_CODE_SOURCE, shared_code_dest)

    # Se o arquivo de dependências existir, instala todas as bibliotecas.
    if os.path.exists(REQUIREMENTS_FILE):
        # Instala os pacotes diretamente na pasta 'build/python'.
        # Isso permite que a Lambda importe as bibliotecas de forma padrão (ex: import requests).
        subprocess.check_call(
            ["pip", "install", "-r", REQUIREMENTS_FILE, "-t", PYTHON_TOP_LEVEL_DIR, "--no-cache-dir"]
        )
    else:
        # Apenas um aviso caso o arquivo não seja encontrado.
        print(f"Aviso: Arquivo '{REQUIREMENTS_FILE}' não encontrado. Nenhuma dependência externa será instalada.")

if __name__ == '__main__':
    adjust_layer_directory()