from setuptools import setup, find_packages

setup(
    name='ct-treedir',
    version='0.2',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ct-treedir = cttreedir:main",
        ],
    },
)