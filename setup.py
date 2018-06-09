# core modules
from setuptools import find_packages
from setuptools import setup
import io
import os

# internal modules
exec(open('edapy/_version.py').read())


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(os.path.join(os.path.dirname(__file__), file_name),
                 encoding='utf-8') as f:
        return f.read()


config = {
    'name': 'edapy',
    'version': __version__,
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
    'description': 'A tookit for exploratoriy data analysis.',
    'long_description': read('README.md'),
    'long_description_content_type': 'text/markdown',
    'install_requires': [
        'cfg_load>=0.3.1',
        'click>=6.7',
        'pandas>=0.20.3',
        'Pillow>=4.2.1',
        'PyPDF2>=1.26.0',
        'PyYAML>=3.12',
    ],
    'keywords': ['EDA', 'Data Science'],
    'download_url': 'https://github.com/MartinThoma/edapy',
    'classifiers': ['Development Status :: 3 - Alpha',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Science/Research',
                    'Intended Audience :: Information Technology',
                    'License :: OSI Approved :: MIT License',
                    'Natural Language :: English',
                    'Programming Language :: Python :: 3.6',
                    'Topic :: Scientific/Engineering :: Information Analysis',
                    'Topic :: Software Development',
                    'Topic :: Utilities'],
    'zip_safe': False,
}

setup(**config)
