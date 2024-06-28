import os
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install as _install


class PostInstallCommand(_install):
    def run(self):
        _install.run(self)
        self.execute_post_install_script()

    def execute_post_install_script(self):
        script_path = os.path.join(os.path.dirname(__file__), 'post_install.py')
        if os.path.exists(script_path):
            subprocess.call([sys.executable, script_path])

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='nanosense',
    version='0.5.9',
    description='A comprehensive package for solid state nanopore data analysis and visualization.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Shankar Dutt',
    author_email='shankar.dutt@anu.edu.au',
    url='https://github.com/shankardutt/nanosense',
    packages=find_packages(include=['nanosense', 'nanosense.*']),
    include_package_data=True,
    package_data={
        'nanosense': ['icons.icns', 'image_1.jpg'],
    },
    install_requires=[
        'PySide6',
        'cryptography',
        'matplotlib',
        'neo',
        'numpy',
        'pyabf',
        'scipy',
        'joblib',
        'bottleneck',
        'ruptures',
        'pywavelets',
        'detecta',
        'hmmlearn',
        'scikit-learn',
        'h5py',
        'seaborn',
        'pandas',
        'tabulate',
        'sktime',
        'lightgbm',
        'torch',
        'torchvision',
        'tensorflow',
        'numexpr',
        'uncertainties',
        'pyqtgraph',
        'lightgbm',
        'pynvml',
        'psutil'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'nanosense=nanosense.nanosense:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
)
