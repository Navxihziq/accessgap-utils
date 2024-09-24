from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="accessgap-utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    author="Zhixuan Qi",
    author_email="zhixuanqi@outlook.com",
    description="Utility functions for Urban Access Gap Project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/accessgap-utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)