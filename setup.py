from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in catalyst_management/__init__.py
from catalyst_management import __version__ as version

setup(
	name="catalyst_management",
	version=version,
	description="Catalyst Management Services",
	author="Simon Wanyama",
	author_email="simon.w@indictranstech.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
