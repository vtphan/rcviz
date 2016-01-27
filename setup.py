#!/usr/bin/env python

from distutils.core import setup

setup(name='rcviz',
      version='0.1',
      description='Python call graph visualization for recursive functions',
      author='Vinhthuy Phan',
      author_email='vphan@memphis.edu',
      url='https://github.com/vtphan/rcviz',
      packages=['rcviz'],
	    include_package_data=True,
	    install_requires=['pygraphviz'],
	    zip_safe=False,
     )