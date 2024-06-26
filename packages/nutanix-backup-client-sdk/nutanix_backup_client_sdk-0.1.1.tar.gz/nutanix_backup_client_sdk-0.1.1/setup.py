# setup.py

from setuptools import setup, find_packages

setup(
    name="nutanix_backup_client_sdk",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.20.0",
    ],
    author="Anirudh Goyal",
    author_email="anirudh.goyal1@nutanix.com",
    description="A client SDK for Nutanix Backup",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/nutanix_backup_client_sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
