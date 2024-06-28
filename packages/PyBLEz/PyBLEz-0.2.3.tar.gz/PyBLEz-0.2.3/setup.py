from setuptools import setup, find_packages

setup(
    name='PyBLEz',
    version='0.2.3',
    description='A Python library for creating BLE peripherals using BlueZ and D-Bus',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kgoke/PyBLEz',
    author='Keegan Goecke',
    author_email='goecke.dev@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'dbus-python',
        'pycairo',
        'pygobject',
    ],
    python_requires='>=3.6',
)
