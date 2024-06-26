# setup.py

from setuptools import setup, find_packages

setup(
    name='flareec',
    version='0.2b1',
    packages=find_packages(),
    description='A package for with a coding toolset thet kikostudios use an is made to code faster',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kiko.Studios',
    author_email='hrdykrystof@gmail.com',
    url='https://github.com/yourusername/flareec',  # Replace with your repository URL if available
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
