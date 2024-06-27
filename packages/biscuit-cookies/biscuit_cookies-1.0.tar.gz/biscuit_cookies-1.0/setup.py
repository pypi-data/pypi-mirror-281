from setuptools import setup

name = 'biscuit-cookies'
version = '1.0'
author = 'GooseG4G'
email = 'danilnegusev@inbox.ru'
desc = ('The package is designed to work with cookies for the Chrome browser. The package allows you to delete, '
        'insert, receive and decrypt cookies.')
url = 'https://github.com/GooseG4G/biscuit'
packages = ['biscuit']
requires = ['pywin32', 'pycryptodome', 'pywin32']

setup(
    name=name,
    version=version,
    author=author,
    author_email=email,
    description=desc,
    url=url,
    packages=packages,
    install_requires=requires
)
