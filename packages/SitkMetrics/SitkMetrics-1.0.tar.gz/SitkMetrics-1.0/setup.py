from setuptools import setup, find_packages

setup(
    name='SitkMetrics',
    version='1.0',
    description='A library for calculating image segmentation metrics using SimpleITK',
    author='Peyman Pakzaban',
    author_email='pakzaban@gmail.com',
    url='https://github.com/pakzaban/SitkMetrics',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'SimpleITK'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
