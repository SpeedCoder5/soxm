import importlib
from pathlib import Path
import sys

def main():
    system_major = sys.version_info.major
    print("Using interpreter: " + sys.executable)
    # check to see if the venv is running https://stackoverflow.com/a/58026969
    if sys.prefix == sys.base_prefix:
        raise ModuleNotFoundError("venv not activated. " +
        "Please first activate venv for project via `source activate.sh`.\n" +
        "To debug, after activating venv, use `which python` to get interpreter path " + 
        "to add VS code via https://code.visualstudio.com/docs/python/environments.")
    
    # print python version
    print(f'python version  == {sys.version}')

    contents = Path('requirements.txt').read_text()
    libraries = [line.split('==')[0].split('-learn')[0] for line in contents.split('\n') if line and not line.startswith('scikit') and not line.startswith('#')]
    print(libraries)
    for library_name in libraries:
        print(f'importing {library_name}', end=':')
        module = importlib.import_module(library_name)        
        version = getattr(module, '__version__', None)        
        if version:
            print(f"{version}")
        else:
            print("no __version__")

if __name__ == '__main__':
    main()
