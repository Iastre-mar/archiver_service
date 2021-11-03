import subprocess


def du(path):
    """Возвращает использованное директорией место"""
    return subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')