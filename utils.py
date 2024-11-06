def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


composite_translation = {
    'True Color No Correction': 'true_color_nocorr',
    'CIMSS True Color Sun Zenith Rayleigh': 'cimss_true_color_sunz_rayleigh',
    'CIMSS True Color Sun Zenith': 'cimss_true_color_sunz',
    'CIMSS True Color': 'cimss_true_color',
    'True Color Reproduction Corrected': 'true_color_reproduction_corr',
    'True Color Reproduction Uncorrected': 'true_color_reporduction_uncorr',
    'True Color Reproduction': 'true_color_reproduction',
    'Night IR with High-resolution': 'night_ir_alpha'
}

satellite_translation = {
    'GOES-EAST (16)': 16,
    'GOES-WEST (17)': 17,
    'GOES-WEST (18)': 18
}

