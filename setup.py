from setuptools import setup, find_packages
import sys, os

setup(name='nanoweb',
      version="1.0",
      description="The nano web framework",
      long_description="""\
The nano framework provides some glue for Webob and Routes.""",
      classifiers=[],
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
