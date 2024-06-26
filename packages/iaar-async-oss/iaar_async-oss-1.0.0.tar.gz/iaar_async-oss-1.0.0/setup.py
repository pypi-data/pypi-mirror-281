#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='iaar_async-oss',
    version='1.0.0',

    description='An asynchronous OSS library based on OSS2=2.15.0.',
    author='Gie',
    author_email='593443714@qq.com',
    license='MIT',
    install_requires=['aiohttp', 'oss2'],
    packages=find_packages(),
)



