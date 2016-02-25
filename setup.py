from setuptools import setup

setup(
    name='pyxley-app',
    version='0.0.1',
    author='Nick Kridler',
    author_email='nmkridler@gmail.com',
    license='MIT',
    description='Pyxley Dashboard',
    packages=['pyxley-app'],
    long_description='Pyxley Dashboard Template',
    url='https://github.com/nmkridler/pyxley-app/',
    install_requires=[
        'flask',
        'matplotlib',
        'numpy',
        'pyxley',
        'pandas==0.17.0'
    ]
)
