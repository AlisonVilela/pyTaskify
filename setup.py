from setuptools import setup
from pytaskify.version import __version__

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pyTaskify',
    version=__version__,
    description='Um task runner em Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alison Vilela',
    author_email='vilela@alison.dev',
    packages=['pytaskify'],
    install_requires=[
        'PyYAML'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent'
    ],
    entry_points={
        'console_scripts': [
            'taskify=pytaskify.cli:main'
        ]
    }
)
