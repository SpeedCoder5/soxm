from setuptools import find_packages, setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')
license = (here / 'LICENSE').read_text(encoding='utf-8')

from src.soxm.__init__ import __version__

setup(
    author='ASRC Federal',
    author_email='rneely@asrcfederal.com',
    description='Social Exploit Matrix (SoXM) Social Exploit Matrix with LLMs',
    python_requires='>=3.6',
    include_package_data=False,
    install_requires=[
        'matplotlib',
        'numpy',
        'python-dotenv',
        'scipy',
        ],
    license=license,
    long_description_content_type='text/markdown',
    long_description=long_description,
    name='soxm',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    project_urls={  # Optional
        'Bug Reports': 'https://jira.avde.net/projects/DSR',
        'Source': 'https://github.sandbox-asrcfederal.com/data-science/soxm.git',
    },
    version=__version__,
    url='https://github.sandbox-asrcfederal.com/data-science/soxm.git',
)

