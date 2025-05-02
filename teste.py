import os
import stat
import shutil

def remove_readonly(func, path, exc_info):
    """Força a remoção de arquivos protegidos."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

destiny = 'teste'

if os.path.exists(destiny):
    try:
        shutil.rmtree(destiny)
        print("Pasta deletada com sucesso!")
    except Exception as e:
        print(f"Erro ao excluir a pasta: {e}")