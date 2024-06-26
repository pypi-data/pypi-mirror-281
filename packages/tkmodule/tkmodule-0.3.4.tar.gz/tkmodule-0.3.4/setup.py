from setuptools import setup

with open('README.md') as file:
    long_description=file.read()
setup(
  name = 'tkmodule',         # How you named your package folder (MyLib)
  packages = ['tkmodule'],   # Chose the same as "name"
  version = '0.3.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TkModule equips developers with a suite of tools and functions that elevate the Tkinter experience to new heights, making GUI creation more intuitive, faster, and more enjoyable. TkModule comes in offering a simplified and more Pythonic approach to GUI development.',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Kartavya Shukla',                   # Type in your name
  author_email = 'novfensec@protonmail.com',      # Type in your E-Mail
  url = 'https://novfensec.vercel.app/projects/tkmodule',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Novfensec/tkmodule/archive/refs/tags/v_0.3.4.tar.gz',    # I explain this later on
  keywords = ['Tkinter', 'tkmodule', 'TkinterUtitlity'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
          'pillow',
          'pathlib'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
  include_package_data=True
)