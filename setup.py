from setuptools import setup

setup(name = 'dunendggd',
      version = '1.0.0',
      description = 'DUNE Near Detector based on General Geometry Description',
      author = 'Jose Palomino and Guang Yang',
      author_email = 'guang.yang.1@stonybrook.edu, jose.palominogallo@stonybrook.edu',
      license = 'GPLv2',
      url = 'https://github.com/gyang9/GuJo',
      package_dir = {},
      packages = ['duneggd', 'duneggd.Det', 'duneggd.SubDetector', 'duneggd.Component', 'duneggd.Active', 'duneggd.LocalTools', 'duneggd.Booleans', 'duneggd.Hall', 'duneggd.ArgonCube'],
      install_requires = [
        "gegede >= 0.6.1",    # In reality we need the '0.7' tag, but its setup.py still reports itself as 0.6.1
        "pint >= 0.5.1",      # for units
        "lxml >= 3.3.5",      # for GDML export
      ],
  )

