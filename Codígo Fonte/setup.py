import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "sqlite3", "pandas", "tkinter", "tkcalendar"],
    "includes": ["winsound"],
    "include_files": ["Arquivos Excel/", "Database/", "Imagens/", "Sons/"]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("main.py", base=base, icon="Imagens/icon.ico")
]

setup(
    name="Return System",
    version="2.0",
    description="Controle de Entrada e Saída de Produtos",
    options={"build_exe": build_exe_options},
    executables=executables
)

