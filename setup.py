from setuptools import setup, find_packages

__version__ = '0.0.1'
__author__ = 'al7ech'
__name__ = 'checker'

setup(name=__name__,
      version=__version__,
      url='https://github.com/al7ech/checker',
      author=__author__,
      author_email='al7ech@gmail.com',
      description='Backtesting tool for Automated Trading Systems',
      packages=find_packages(exclude=['examples']),
      long_description=open('README.md').read(),
      setup_requires=['numpy>=1.15','pandas'],
      install_requires=['numpy>=1.15','pandas']
)