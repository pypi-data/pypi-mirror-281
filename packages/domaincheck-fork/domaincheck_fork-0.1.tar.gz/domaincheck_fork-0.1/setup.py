#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
	readme = f.read()

REQUIREMENTS = [
	'cryptography>=3.3.2',
	'dnspython>=2.2.1',
]

setup(
	name='domaincheck-fork',
	version='0.1',
	description='check security aspects of a second-level domain name',
	keywords='CAA DMARC DNS DNSKEY DNSSEC MTA-STS SPF TLS-RPT',
	author='Jan Schaumann, Zuza Slawik',
	author_email='jschauma@akamai.com, zslawik@akamai.com',
	license='Apache',
	url='https://github.com/intelowlproject/domaincheck/',
	install_requires=REQUIREMENTS,
	scripts=['domaincheck/domaincheck'],
	data_files=[('share/man/man1', ['doc/domaincheck.1'])],
	packages=["domaincheck"],
)
