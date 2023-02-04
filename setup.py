from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in holidays/__init__.py
from holidays import __version__ as version

setup(
	name="holidays",
	version=version,
	description="All International Holiday Lists",
	author="IoTReady",
	author_email="hello@iotready.co",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
