# setup.py

from setuptools import setup, find_packages

setup(
    name='projectlumina',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'projectlumina-cli = projectlumina.__main__:main',
        ],
    },
    author='riqvip',
    author_email='riqvip@gmail.com',
    description='A Python library providing an API wrapper and tools to edit Minecraft Bedrock level.dat files for Project Lumina.',
    url='https://github.com/riqvip/projectlumina.py',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)