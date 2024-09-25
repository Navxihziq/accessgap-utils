from setuptools import find_packages, setup

setup(
    name="accessgap-utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "geopandas==0.14.4",
        "pandas==2.2.3",
        "pyproj==3.6.1",
        "shapely==2.0.6",
        "overpy==0.6.1",
        "osmnx==1.9.4",
    ],
    extras_require={
        "dev": [
            "cfgv==3.4.0",
            "distlib==0.3.8",
            "filelock==3.16.1",
            "identify==2.6.1",
            "iniconfig==2.0.0",
            "nodeenv==1.9.1",
            "packaging==24.1",
            "platformdirs==4.3.6",
            "pluggy==1.5.0",
            "pre-commit==3.8.0",
            "pyright==1.1.381",
            "pytest==8.3.3",
            "PyYAML==6.0.2",
            "virtualenv==20.26.5",
        ],
    },
)
