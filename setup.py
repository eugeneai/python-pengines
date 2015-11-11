import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


setup(name='pengines',
      version=0.1,
      description='Python interface to SWI-Prolog penigines.',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords="prolog swi",
      author='Evgeny Cherkashin',
      author_email='eugeneai@irnok.net',
      url='',
      packages=['pengines'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        #'rdflib',
        #'rdflib-jsonld',
        #'rdflib-kyotocabinet==0.1',
        'zope.component',
        'requests',
        ],
      # dependency_links = [
      #   'https://github.com/eugeneai/rdflib-kyotocabinet/archive/master.zip#egg=rdflib-kyotocabinet-0.1',
      #   'https://github.com/Pylons/pyramid/archive/1.6a2.zip#egg=pyramid-1.6a2',
      #   'https://github.com/eugeneai/waitress/archive/0.8.11dev0ipv6-1.zip#egg=waitress-0.8.11dev0ipv6-1',
      #   'https://github.com/mozilla-services/cornice/archive/master.zip#egg=cornice-1.2.0.dev0',
      #   ],
      #package_dir = {'': 'pengines'},
)
