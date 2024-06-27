from setuptools import setup, find_packages

setup(
    name='funkmodel',
    version='0.1.0',
    description='Pre Built Functionality for Tortoise Class Models Inheritance',
    url='https://github.com/funkaclau',
    author='funkaclau',
    packages=find_packages(),
    install_requires=[
        "tortoise-orm"
    ],
)

