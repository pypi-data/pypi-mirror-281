import os
import subprocess
import sys
from setuptools import setup, find_packages

# def check_and_install_nvidia_packages():
#     try:
#         import pynvml
#         pynvml.nvmlInit()
#         gpu_count = pynvml.nvmlDeviceGetCount()
#         if gpu_count > 0:
#             if os.name == 'nt' or sys.platform.startswith('linux'):
#                 print("NVIDIA GPUs detected. Installing NVIDIA packages...")
#                 subprocess.check_call([
#                     sys.executable, "-m", "pip", "install",
#                     "--extra-index-url=https://pypi.nvidia.com",
#                     "cudf-cu12==24.6.*", "dask-cudf-cu12==24.6.*", "cuml-cu12==24.6.*",
#                     "cugraph-cu12==24.6.*", "cuspatial-cu12==24.6.*", "cuproj-cu12==24.6.*",
#                     "cuxfilter-cu12==24.6.*", "cucim-cu12==24.6.*", "pylibraft-cu12==24.6.*",
#                     "raft-dask-cu12==24.6.*", "cuvs-cu12==24.6.*"
#                 ])
#     except ImportError:
#         print("pynvml is not installed. Skipping NVIDIA package installation.")
#     except Exception as e:
#         print(f"An error occurred while checking/installing NVIDIA packages: {e}")


def check_and_install_nvidia_packages():
    try:
        if sys.platform.startswith('darwin'):
            print("Running on macOS. Skipping NVIDIA package installation.")
            return
        
        import pynvml
        pynvml.nvmlInit()
        gpu_count = pynvml.nvmlDeviceGetCount()
        if gpu_count > 0:
            if os.name == 'nt' or sys.platform.startswith('linux'):
                print("NVIDIA GPUs detected. Installing NVIDIA packages...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install",
                    "--extra-index-url=https://pypi.nvidia.com",
                    "cudf-cu12==24.6.*", "dask-cudf-cu12==24.6.*", "cuml-cu12==24.6.*"
                ])
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install",
                    "tensorrt"
                ])
    except ImportError:
        print("pynvml is not installed. Skipping NVIDIA package installation.")
    except Exception as e:
        print(f"An error occurred while checking/installing NVIDIA packages: {e}")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='nanosense',
    version='0.5.6',
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
)

check_and_install_nvidia_packages()
