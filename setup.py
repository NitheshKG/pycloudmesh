from setuptools import setup, find_packages

setup(
    name="cloudmesh",
    version="0.1.0",
    author="Nithesh",
    author_email="nitheshkg18@gmail.com",
    description="A package to retrieve reservation costs from AWS, Azure, and GCP",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NitheshKG/cloudmesh",
    packages=find_packages(),
    install_requires=[
        "boto3",  
        "requests",
        "google",
        "google-cloud-billing"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
