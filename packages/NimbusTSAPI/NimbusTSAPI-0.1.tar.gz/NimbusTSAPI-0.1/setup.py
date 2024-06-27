from distutils.core import setup
setup(
  name = 'NimbusTSAPI',         # How you named your package folder (MyLib)
  packages = ['NimbusTSAPI'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Volue\'s Nimbus TS API GraphQL webservice python parser',   # Give a short description about your library
  author = 'Gudmundur Smari Gudmundsson',                   # Type in your name
  author_email = 'gummismari@gummismari.com',      # Type in your E-Mail
  url = 'https://github.com/gsmari/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/gsmari/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['nimbus', 'time series', 'API web service', 'hydropower software'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)