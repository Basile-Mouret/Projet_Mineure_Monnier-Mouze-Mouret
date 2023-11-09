from cx_Freeze import setup, Executable
import fonctions
base = None
executables = [Executable("analyse.py", base=base)]
packages = ["idna","fonctions"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}
setup(
    name = "PERT",
    options = options,
    version = "1.0",
    description = 'Programme realise lors de la mineure info par Benjamin Monnier, Guillermo Mouze et Basile Mouret',
    executables = executables
)