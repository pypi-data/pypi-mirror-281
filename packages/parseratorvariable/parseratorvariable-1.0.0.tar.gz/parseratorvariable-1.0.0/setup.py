try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools"
    )

setup(
    name="parseratorvariable",
    url="https://github.com/datamade/parseratorvariables",
    version="1.0.0",
    description="Structured variable type for dedupe",
    packages=["parseratorvariable"],
    install_requires=["dedupe>=3.0.0", "numpy", "probableparsing"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="The MIT License: http://www.opensource.org/licenses/mit-license.php",
)
