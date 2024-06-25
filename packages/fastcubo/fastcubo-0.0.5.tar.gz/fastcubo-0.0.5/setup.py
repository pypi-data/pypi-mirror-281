# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastcubo']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.0.0', 'utm>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'fastcubo',
    'version': '0.0.5',
    'description': '🏎💨vroom vroom - data downloader',
    'long_description': '# FastCubo\n\nA simple API for `ee.data.pixels` inspired by [cubo](https://github.com/ESDS-Leipzig/cubo), designed for creating and managing data cubes up to 10 times faster.\n\n## Installation\n\nInstall the latest version from PyPI:\n\n```bash\npip install cubo\n```\n\nInstall cubo with the required GEE dependencies from PyPI:\n\n```bash\npip install cubo[ee]\n```\n\nUpgrade cubo by running:\n\n```bash\npip install -U cubo\n```\n\nInstall the latest version from conda-forge:\n\n```bash\nconda install -c conda-forge cubo\n```\n\nInstall the latest dev version from GitHub by running:\n\n```bash\npip install git+https://github.com/davemlz/cubo\n```\n\n\n## How to use\n\n\nDownload a S2 data cube.\n\n```python\n\nimport fastcubo\nimport ee\n\nee.Initialize(opt_url="https://earthengine-highvolume.googleapis.com")\n\ntable = fastcubo.query_image(\n    task_id= "EU2560_E4521N3012",\n    points=[(51.079225, 10.452173), (-76.5, -9.5)],\n    outnames=["demo_0.tif", "demo_1.tif"],\n    collection="NASA/NASADEM_HGT/001",\n    bands=["elevation", "num", "swb"],\n    edge_size=256,\n    resolution=90\n)\n\nda = fastcubo.downloader(table=table, nworkers=8)\n```\n\nDownload DEM data cube\n\n\n```python\nimport fastcubo\nimport ee\n\nee.Initialize(opt_url="https://earthengine-highvolume.googleapis.com")\n\ntable = fastcubo.query_imagecollection(\n    task_id= "EU2560_E4521N3011", # Task id\n    point=(51.079225, 10.452173),\n    collection="COPERNICUS/S2_HARMONIZED", # Id of the GEE collection\n    bands=["B4","B3","B2"], # Bands to retrieve\n    start_date="2016-06-01", # Start date of the cube\n    end_date="2017-07-01", # End date of the cube\n    edge_size=128, # Edge size of the cube (px)\n    resolution=10, # Pixel size of the cube (m)\n)\n\nda = fastcubo.downloader(table=table, nworkers=8)    \n```',
    'author': 'Cesar Aybar',
    'author_email': 'fcesar.aybar@uv.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/csaybar/fastcubo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
