#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pypi-cleanup',
        version = '0.1.8.dev20240626030133',
        description = 'PyPI Bulk Release Version Cleanup Utility',
        long_description = '# PyPI Bulk Release Version Cleanup Utility\n\n[![PyPI Cleanup Version](https://img.shields.io/pypi/v/pypi-cleanup?logo=pypi)](https://pypi.org/project/pypi-cleanup/)\n[![PyPI Cleanup Python Versions](https://img.shields.io/pypi/pyversions/pypi-cleanup?logo=pypi)](https://pypi.org/project/pypi-cleanup/)\n[![Build Status](https://img.shields.io/github/actions/workflow/status/arcivanov/pypi-cleanup/pypi-cleanup.yml?branch=master)](https://github.com/arcivanov/pypi-cleanup/actions/workflows/pypi-cleanup.yml)\n[![PyPI Cleanup Downloads Per Day](https://img.shields.io/pypi/dd/pypi-cleanup?logo=pypi)](https://pypi.org/project/pypi-cleanup/)\n[![PyPI Cleanup Downloads Per Week](https://img.shields.io/pypi/dw/pypi-cleanup?logo=pypi)](https://pypi.org/project/pypi-cleanup/)\n[![PyPI Cleanup Downloads Per Month](https://img.shields.io/pypi/dm/pypi-cleanup?logo=pypi)](https://pypi.org/project/pypi-cleanup/)\n\n## Overview\n\nPyPI Bulk Release Version Cleanup Utility (`pypi-cleanup`) is designed to bulk-delete releases from PyPI that match\nspecified patterns.\nThis utility is most useful when CI/CD method produces a swarm of temporary\n[.devN pre-releases](https://www.python.org/dev/peps/pep-0440/#developmental-releases) in between versioned releases.\n\nBeing able to cleanup past .devN junk helps PyPI cut down on the storage requirements and keeps release history neatly\norganized.\n\n## WARNING\n\nTHIS UTILITY IS DESTRUCTIVE AND CAN POTENTIALLY WRECK YOUR PROJECT RELEASES AND MAKE THE PROJECT INACCESSIBLE ON PYPI.\n\nThis utility is provided on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or\nimplied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY,\nor FITNESS FOR A PARTICULAR PURPOSE.\n\n## Details\n\nThe default package release version selection pattern is `r".*dev\\d+$"`.\n\nAuthentication password may be passed via environment variable\n`PYPI_CLEANUP_PASSWORD`. Otherwise, you will be prompted to enter it.\n\nAuthentication with TOTP is supported.\n\n### Examples:\n\n```bash\n$ pypi-cleanup --help\nusage: pypi-cleanup [-h] [-u USERNAME] -p PACKAGE [-t URL] [-r PATTERNS | --leave-most-recent-only] [--query-only] [--do-it] [-y] [-d DAYS] [-v]\n\nPyPi Package Cleanup Utility v0.1.7.dev20240624230606\n\noptions:\n  -h, --help            show this help message and exit\n  -u USERNAME, --username USERNAME\n                        authentication username (default: None)\n  -p PACKAGE, --package PACKAGE\n                        PyPI package name (default: None)\n  -t URL, --host URL    PyPI <proto>://<host> prefix (default: https://pypi.org/)\n  -r PATTERNS, --version-regex PATTERNS\n                        regex to use to match package versions to be deleted (default: None)\n  --leave-most-recent-only\n                        delete all releases except the *most recent* one, i.e. the one containing the most recently created files (default: False)\n  --query-only          only queries and processes the package, no login required (default: False)\n  --do-it               actually perform the destructive delete (default: False)\n  -y, --yes             confirm extremely dangerous destructive delete (default: False)\n  -d DAYS, --days DAYS  only delete releases **matching specified patterns** where all files are older than X days (default: 0)\n  -v, --verbose         be verbose (default: 0)\n```\n\n#### Regular Cleanup of Development Artifacts\n```bash\n$ pypi-cleanup -u arcivanov -p pybuilder\nPassword: \nAuthentication code: 123456\nINFO:root:Deleting pybuilder version 0.12.3.dev20200421010849\nINFO:root:Deleted pybuilder version 0.12.3.dev20200421010849\nINFO:root:Deleting pybuilder version 0.12.3.dev20200421010857\nINFO:root:Deleted pybuilder version 0.12.3.dev20200421010857\n```\n\n#### Using Custom Regex Pattern\n```bash\n$ pypi-cleanup -u arcivanov -p geventmp -r \'.*\\\\.dev1$\' \nWARNING:root:\nWARNING:\n        You\'re using custom patterns: [re.compile(\'.*\\\\\\\\.dev1$\')].\n        If you make a mistake in your patterns you can potentially wipe critical versions irrecoverably.\n        Make sure to test your patterns before running the destructive cleanup.\n        Once you\'re satisfied the patterns are correct re-run with `-y`/`--yes` to confirm you know what you\'re doing.\n        Goodbye.\n$ pypi-cleanup -u arcivanov -p geventmp -r \'.*\\\\.dev1$\' -y\nPassword:\nWARNING:root:RUNNING IN DRY-RUN MODE\nINFO:root:Will use the following patterns [re.compile(\'.*\\\\.dev1$\')] on package geventmp\nAuthentication code: 123456\nINFO:root:Deleting geventmp version 0.0.1.dev1\n```\n\n#### Deleting All Versions Except The Most Recent One\n\n```bash\n$ pypi-cleanup -p pypi-cleanup --leave-most-recent-only\nWARNING:root:\nWARNING:\n        You\'re trying to delete ALL versions of the package EXCEPT for the *most recent one*, i.e.\n        the one with the most recent (by the wall clock) files, disregarding the actual version numbers \n        or versioning schemes!\n\n        You can potentially wipe critical versions irrecoverably.\n        Make sure this is what you really want before running the destructive cleanup.\n        Once you\'re sure you want to delete all versions except the most recent one,\n        re-run with `-y`/`--yes` to confirm you know what you\'re doing.\n        Goodbye.\n$ pypi-cleanup -p pypi-cleanup --leave-most-recent-only -y --query-only\nINFO:root:Running in DRY RUN mode\nINFO:root:Will only leave the MOST RECENT version of the package \'pypi-cleanup\'\nINFO:root:Leaving the MOST RECENT package version: 0.1.7.dev20240624221535 - 2024-06-24T22:15:52.778775+0000\nINFO:root:Found the following releases to delete:\nINFO:root: 0.0.1\nINFO:root: 0.0.2\nINFO:root: 0.0.3\nINFO:root: 0.1.0\nINFO:root: 0.1.1\nINFO:root: 0.1.2\nINFO:root: 0.1.3\nINFO:root: 0.1.4\nINFO:root: 0.1.5\nINFO:root: 0.1.6\nINFO:root:Query-only mode - exiting\n```\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Topic :: Software Development :: Build Tools'
        ],
        keywords = 'PyPI cleanup build dev tool release version',

        author = 'Arcadiy Ivanov',
        author_email = 'arcadiy@ivanov.biz',
        maintainer = 'Arcadiy Ivanov',
        maintainer_email = 'arcadiy@ivanov.biz',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/arcivanov/pypi-cleanup',
        project_urls = {
            'Bug Tracker': 'https://github.com/arcivanov/pypi-cleanup/issues',
            'Documentation': 'https://github.com/arcivanov/pypi-cleanup',
            'Source Code': 'https://github.com/arcivanov/pypi-cleanup'
        },

        scripts = [],
        packages = ['pypi_cleanup'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {
            'console_scripts': ['pypi-cleanup = pypi_cleanup:main']
        },
        data_files = [],
        package_data = {
            'pypi_cleanup': ['LICENSE']
        },
        install_requires = ['requests~=2.23'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '>=3.7',
        obsoletes = [],
    )
