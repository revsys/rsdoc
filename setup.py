from setuptools import setup

setup(
    name='rsdoc',
    version='1.1',
    py_modules=['rsdoc'],
    install_requires=[
        'Click>=6.7',
        'requests>=2.18.1',
        'cookiecutter>=1.5.1',
        'envparse>=0.2.0',
    ],
    entry_points='''
        [console_scripts]
        rsdoc=rsdoc:cli
    ''',
)
