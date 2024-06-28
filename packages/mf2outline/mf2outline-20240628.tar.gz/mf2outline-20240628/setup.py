from distutils.core import setup
setup(
  name = 'mf2outline',
  packages = ['mf2outline'],
  version = '20240628',
  description = 'mf2outline is a python script that converts METAFONT fonts to outline formats like OpenType.',
  author = 'Linus Romer',
  author_email = 'linusromer@gmx.ch',
  url = 'https://github.com/linusromer/mf2outline',
  include_package_data = True,
  package_data = {'': ['*.mp'],},
  keywords = ['mf2outline', 'metafont', 'metapost'], 
  classifiers=[
        "Programming Language :: Python :: 2.7",
  ],
)
