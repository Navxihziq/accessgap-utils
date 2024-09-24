from setuptools import find_packages, setup


# Read requirements from requirements.txt
def parse_requirements(filename: str) -> list[str]:
    """Parse requirements from a file."""
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

try:
    requirements = parse_requirements("requirements.txt")
except Exception as e:
    print(f"Warning: Could not parse requirements.txt: {e}")
    requirements = []

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
