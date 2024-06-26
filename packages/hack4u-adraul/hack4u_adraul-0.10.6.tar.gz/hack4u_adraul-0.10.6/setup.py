from setuptools import setup,find_packages

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hack4u-adraul",
    version="0.10.6",
    packages=find_packages(),
    install_requires=[],
    author="raul leon",
    description="ejemplo de proyecto cursos Hack4u",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io"
)