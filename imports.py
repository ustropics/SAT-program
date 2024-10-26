def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


def test_func():
    install_and_import('goes2go')
    install_and_import('satyp')
    install_and_import('pysepctral')