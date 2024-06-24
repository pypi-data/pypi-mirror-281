from setuptools import setup, find_packages

setup(
    name='cherryterm',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        cherryterm=cherryterm.cli:cli
    ''',
)