from setuptools import setup, find_packages
import sys

if sys.platform.startswith("win"):
    raise RuntimeError("This package is not supported on a Windows platform.")

setup(
    name="DeployStack",
    version="1.0.0",
    description="DeployStack is a command-line utility for deploying OpenStack on Debian.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sorecchione07435/DeployStack",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "psutil",
        "python-dotenv",
        "PyYAML",
        "requests",
        "tqdm",
        "bs4"
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "deploystack=deploystack.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)