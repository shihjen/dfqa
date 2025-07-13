from setuptools import setup, find_packages

setup(
    name="dfqa",
    version="0.1.7",
    description="A Python library for assessing the data quality in pandas DataFrames.",
    author="Tan Shih Jen",      
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "seaborn",
        "plotly",
        "openpyxl"
    ],
    python_requires='>=3.7',      
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
