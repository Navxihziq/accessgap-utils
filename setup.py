from setuptools import find_packages, setup

setup(
    name="accessgap-utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "geopandas",
        "osmnx",
        "pandas",
        "pyproj",
        "shapely",
    ],
    url="https://github.com/Navxihziq/accessgap-utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
