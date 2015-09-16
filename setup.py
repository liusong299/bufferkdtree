'''
Created on 15.09.2015

@author: fgieseke
'''

import os
import sys
from distutils.command.clean import clean as Clean
import shutil

DISTNAME = 'bufferkdtree'
DESCRIPTION = 'A Python library for large-scale exact nearest neighbor search using Buffer k-d Trees (bufferkdtree).'
LONG_DESCRIPTION = open('README.rst').read()
MAINTAINER = 'Fabian Gieseke'
MAINTAINER_EMAIL = 'fgieseke@cs.ru.nl'
URL = 'https://github.com/gieseke/bufferkdtree'
LICENSE = 'GNU GENERAL PUBLIC LICENSE'
DOWNLOAD_URL = 'https://github.com/gieseke/bufferkdtree'

import bufferkdtree
VERSION = bufferkdtree.__version__

if len(set(('develop', 'release', 'bdist_egg', 'bdist_rpm',
           'bdist_wininst', 'install_egg_info', 'build_sphinx',
           'egg_info', 'easy_install', 'upload', 'bdist_wheel',
           '--single-version-externally-managed',
            )).intersection(sys.argv)) > 0:
    import setuptools
    extra_setuptools_args = dict(
        zip_safe=False,  
        include_package_data=True,
    )
else:
    extra_setuptools_args = dict()

def configuration(parent_package='', top_path=None):

    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('bufferkdtree')

    return config

# define new clean command
class CleanCommand(Clean):

    description = "Cleans up code ..."

    def run(self):

        Clean.run(self)

        if os.path.exists('build'):
            shutil.rmtree('build')

        for dirpath, dirnames, filenames in os.walk('bufferkdtree'):
            for filename in filenames:
                if (filename.endswith('.so') or \
                    filename.endswith('.pyd') or \
                    filename.endswith('.dll') or \
                    filename.endswith('.pyc') or \
                    filename.endswith('_wrap.c') or \
                    filename.startswith('wrapper_') or \
                    filename.endswith('~')):
                        os.unlink(os.path.join(dirpath, filename))

            for dirname in dirnames:
                if dirname == '__pycache__' or dirname == 'build':
                    shutil.rmtree(os.path.join(dirpath, dirname))

def setup_package():
    
    metadata = dict(name=DISTNAME,
                    maintainer=MAINTAINER,
                    maintainer_email=MAINTAINER_EMAIL,
                    description=DESCRIPTION,
                    license=LICENSE,
                    url=URL,
                    version=VERSION,
                    download_url=DOWNLOAD_URL,
                    long_description=LONG_DESCRIPTION,
                    classifiers=[
                                 'Intended Audience :: Science/Research',
                                 'Intended Audience :: Developers',
                                 'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                                 'Programming Language :: C',
                                 'Programming Language :: Python',
                                 'Programming Language :: Python :: 2',
                                 'Programming Language :: Python :: 2.6',
                                 'Programming Language :: Python :: 2.7',
                                 'Programming Language :: Python :: 3',
                                 'Programming Language :: Python :: 3.2',
                                 'Programming Language :: Python :: 3.3',
                                 'Programming Language :: Python :: 3.4',
                                 ],
                    cmdclass={'clean': CleanCommand},                    
                    **extra_setuptools_args)

    if (len(sys.argv) >= 2
            and ('--help' in sys.argv[1:] or sys.argv[1]
                 in ('--help-commands', 'egg_info', '--version', 'clean'))):

        try:
            from setuptools import setup
        except ImportError:
            from distutils.core import setup

        metadata['version'] = VERSION

    else:

        from numpy.distutils.core import setup
        metadata['configuration'] = configuration

    setup(**metadata)

if __name__ == "__main__":

    setup_package()
