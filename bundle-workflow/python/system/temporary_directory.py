from contextlib import contextmanager
import tempfile
import shutil

@contextmanager
def TemporaryDirectory(keep = False):
    name = tempfile.mkdtemp()
    try:
        yield name
    finally:
        if keep:
            print(f'Keeping {name}')
        else:
            shutil.rmtree(name)