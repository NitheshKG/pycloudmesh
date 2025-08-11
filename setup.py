from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="pycloudmesh",
    version="1.0.2",
    author="Nithesh",
    author_email="nitheshkg18@gmail.com",
    description="Unified FinOps and cost analytics toolkit for AWS, Azure, and GCP. Provides programmatic access to cloud cost, budgeting, optimization, and governance APIs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NitheshKG/pycloudmesh",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,  # This ensures MANIFEST.in is used
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
