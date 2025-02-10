from pathlib import Path
import sys
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def test_selenium_firefox(url="https://www.google.cm", keyword="Google"):
    # Detect geckodriver path using 'which'; if not found, print error
    try:
        detected_path = subprocess.check_output(['which', 'geckodriver']).strip().decode('utf-8')
        print(f"Detected geckodriver at: {detected_path}")
    except subprocess.CalledProcessError:
        print("geckodriver not found; please install it.")
        return

    options = FirefoxOptions()
    options.add_argument("--headless")  # Run Firefox headless

    service = FirefoxService(executable_path=detected_path)
    driver = webdriver.Firefox(service=service, options=options)

    driver.get(url)
    # Wait for the page to load
    time.sleep(2)

    if keyword in driver.page_source:
        print(f"{keyword} found: Selenium works!")
    else:
        print(f"{keyword} not found. Please install the prerequisites described in README.md and then run `make venv`.")
    driver.quit()

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
    overrides = {
        'beautifulsoup4':'bs4',
        'matplotlib==3.8.2':'matplotlib',
        'scikit-learn':'sklearn',
        'umap-learn':'umap'
    }
    libraries = [line for line in contents.split('\n') if line and not line.startswith('#')]
    for i,library_name in enumerate(libraries):
        if library_name in overrides:
            libraries[i]=overrides[library_name]
    print(libraries)
    # for library_name in libraries:
    #     print(f'importing {library_name}', end=':')
    #     module = importlib.import_module(library_name)        
    #     version = getattr(module, '__version__', None)        
    #     if version:
    #         print(f"{version}")
    #     else:
    #         print("no __version__")

    test_selenium_firefox()

if __name__ == '__main__':
    main()
