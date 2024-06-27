from setuptools import setup, find_packages

setup(
    name='calculate-lib',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    description='A simple library for basic arithmetic operations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/calculate-lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)