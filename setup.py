from setuptools import find_packages
from setuptools import setup

config = {
    'name': 'edapy',
    'version': '0.1.0',
    'author': 'Martin Thoma',
    'author_email': 'info@martin-thoma.de',
    'maintainer': 'Martin Thoma',
    'maintainer_email': 'info@martin-thoma.de',
    'packages': find_packages(),
    'scripts': ['bin/edapy'],
    # 'package_data': {'hwrt': ['templates/*', 'misc/*']},
    'platforms': ['Linux'],
    'url': 'https://github.com/MartinThoma/edapy',
    'license': 'MIT',
    'description': 'Exploratory Data Analysis',
    'long_description': ("A tookit for exploratoriy data analysis."),
    'install_requires': [
        "argparse",
        "PyYAML",
        "pandas"
    ],
    'keywords': ['EDA', 'Data Science'],
    'download_url': 'https://github.com/MartinThoma/edapy',
    'classifiers': ['Development Status :: 1 - Planning',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Science/Research',
                    'Intended Audience :: Information Technology',
                    'License :: OSI Approved :: MIT License',
                    'Natural Language :: English',
                    'Programming Language :: Python :: 3.5',
                    'Topic :: Scientific/Engineering :: Information Analysis',
                    'Topic :: Software Development',
                    'Topic :: Utilities'],
    'zip_safe': False,
}

setup(**config)
