from setuptools import setup, find_packages

setup(
    name='iros',
    version='0.1.0',
    description='A simple neural network library',
    author='Roger Ros',
    author_email='rogerrosvidal@gmail.com',
    url='https://github.com/RogerRos/iros',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
