from setuptools import find_packages, setup

# Read requirements from requirements.txt
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="accessgap-utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    author="Zhixuan Qi",
    author_email="zhixuanqi@outlook.com",
    description="Utility functions for Urban Access Gap Project",
    url="https://github.com/yourusername/accessgap-utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
