import setuptools
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read().strip()

setuptools.setup(
    name="delta-sharing-example",
    version=version,
    author="Rodrigo Parada",
    author_email="rodrigo.parada@spinup.cl",
    description="Delta Sharing Example",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: Proprietary :: SpinUp",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.10"
)
