import pytest
import pathlib

def test_version():
    import soxm
    version = soxm.__version__
    root = pathlib.Path(__file__).parent.parent.resolve()
    with open(root / 'src/soxm/__init__.py', 'r', encoding='utf-8') as fi:
        text = fi.readline();
    dequoted_text = text.replace("'","").replace('"','').rstrip()
    version_text = dequoted_text.split('=')[-1]
    assert(version == version_text)

if __name__ == '__main__':
    test_version()