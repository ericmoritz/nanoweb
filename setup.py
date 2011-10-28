from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='nanoweb',
      version=version,
      description="The nano web framework",
      long_description="""\
The nano framework provides some glue for Webob and Routes.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='WSGI',
      author='Eric Moritz',
      author_email='eric@themoritzfamily.com',
      url='http://eric.themoritzfamily.com',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
        "routes",
        "webob",
        "json-schema-validator",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
