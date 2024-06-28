from setuptools import setup, find_packages

setup(
    name="rocauc_comparison",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.6.0"
    ],
    author="Mohamed Mostafa",
    author_email="mmsa12@gmail.com",
    description="A package for comparing ROC AUC scores using DeLong's method.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/mmsa/rocauc_comparison",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
