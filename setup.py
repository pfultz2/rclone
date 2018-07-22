import os, re
from setuptools import setup, find_packages

def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

def get_requires(filename):
    requirements = []
    with open(filename) as req_file:
        for line in req_file.read().splitlines():
            if not line.strip().startswith("#"):
                requirements.append(line)
    return requirements

project_requirements = get_requires("requirements.txt")

setup(
    name="rclone",
    version=get_version("rclone"),
    url='https://github.com/pfultz2/rclone',
    license='boost',
    description='Recursive git clone',
    author='Paul Fultz II',
    author_email='pfultz2@yahoo.com',
    packages=find_packages(),
    install_requires=project_requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rclone = rclone.cli:cli',
        ]
    },
    zip_safe=False
)
