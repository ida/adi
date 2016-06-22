from setuptools import setup, find_packages
import os

version = '0.1.dev0'

long_description = ''
if os.path.exists("README.rst"):
    long_description = open("README.rst").read()

setup(name='adi.samplesite',
      version=version,
      description="This addon does nothing but and shouldn't do anything else \
than install other addons for having a sample set of addons.",
      long_description=long_description,
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='https://github.com/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['adi'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'adi.stepbysteps',
          'adi.enabletopics',
          'adi.noviewlets',
          'adi.reset',
          'adi.minset',
          'adi.info',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
