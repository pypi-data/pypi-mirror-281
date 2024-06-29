# setup.py
from setuptools import setup, find_packages

setup(
    name='wapsok',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='exy',
    author_email='ex@exy.lol',
    description='something',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ex0f',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)