from setuptools import find_packages, setup

setup(
    name="accessgap-utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "geopandas>=0.9.0,<0.13.0",
        "osmnx>=1.1.0,<2.0.0",
        "pandas>=1.3.0,<2.1.0",
        "pyproj>=3.0.0,<4.0.0",
        "shapely>=1.8.0,<2.1.0",
    ],
    url="https://github.com/Navxihziq/accessgap-utils",
    classifiers=[],
    python_requires=">=3.6",
)
