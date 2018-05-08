# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
<<<<<<< HEAD
=======
try: # for pip >= 10
	from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
	from pip.req import parse_requirements
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
import re, ast

# get version from __version__ variable in erpnext/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

<<<<<<< HEAD
with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

=======
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
with open('erpnext/__init__.py', 'rb') as f:
	version = str(ast.literal_eval(_version_re.search(
		f.read().decode('utf-8')).group(1)))

<<<<<<< HEAD
=======
requirements = parse_requirements("requirements.txt", session="")

>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
setup(
	name='erpnext',
	version=version,
	description='Open Source ERP',
	author='Frappe Technologies',
	author_email='info@erpnext.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
<<<<<<< HEAD
	install_requires=install_requires
=======
	install_requires=[str(ir.req) for ir in requirements],
	dependency_links=[str(ir._link) for ir in requirements if ir._link]
>>>>>>> 40a584d5ce3e69a651094c866f1ddc7f5302b825
)
