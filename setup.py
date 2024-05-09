from setuptools import find_packages, setup

import sparksql_jupyter

setup(
    name="sparksql-jupyter",
    version=sparksql_jupyter.__version__,
    description="Spark SQL magic command for Jupyter notebooks",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Cinyoung Hur",
    author_email="cinyoung.hur@gmail.com",
    url="https://github.com/cryeo/sparksql-jupyter",
    license="MIT License",
    install_requires=["pyspark>=2.3.0", "ipython>=7.4.0", "jinja2>=3.0.0"],
    packages=find_packages(exclude=("tests", "docs")),
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
