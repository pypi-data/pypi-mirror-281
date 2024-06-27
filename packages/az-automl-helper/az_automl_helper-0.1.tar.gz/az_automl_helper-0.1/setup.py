# setup.py

from setuptools import setup, find_packages

setup(
    name='az_automl_helper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'azureml-core'
    ],
    author='Microsoft Corporation',
    author_email='support@microsoft.com',
    maintainer='M.R. Vijay Krishnan',
    maintainer_email='vijaykrishnanmr@gmail.com',
    description='A helper library for Azure AutoML solutions',
    license='MIT',
    url='https://github.com/kitranet/automl_helper',  # Replace with your GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
