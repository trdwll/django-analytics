#!/usr/bin/env python
import sys
from analytics import __version__, __description__, __license__

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='django-analytics',
    version=__version__,
    description=__description__,
    long_description=open('./README.md', 'r').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    keywords='django analytics',
    maintainer='Russ \'trdwll\' Treadwell',
    maintainer_email='russ@trdwll.com',
    url='https://github.com/trdwll/django-analytics',
    download_url='https://github.com/trdwll/django-analytics/tarball/v%s' % __version__,
    license=__license__,
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    )
