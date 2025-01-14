from setuptools import setup, find_packages

setup(
    name="alfred-python",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'lxml>=4.9.3',
    ],
    entry_points={
        'console_scripts': [
            'alfred-python=alfred.main:main',
        ],
    },
) 