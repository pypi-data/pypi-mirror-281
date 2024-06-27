import os

from setuptools import setup, find_packages
from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements

requirements = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'), session=PipSession())

setup(
    name='github_changes',
    version='1.0.0',
    author='danniel',
    author_email='danniel.shalev@gmail.com',
    description='A github file changes module',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[str(requirement.requirement) for requirement in requirements],
    include_package_data=True
)
