from setuptools import setup, find_packages

setup(
    name='PyBLEz',
    version='0.2.1',
    description='A Python library for creating BLE peripherals using BlueZ and D-Bus',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kgoke/PyBLEz',
    aurhtor='Keegan Goecke',
    author_email='goecke.dev@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'dbus-python',
        'pycairo',
        'pygobject',
    ],
    classifeiers=[
        'Developement Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
