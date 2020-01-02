from distutils.core import setup
setup(
  name = 'pyogame2',
  packages = ['pyogame2'],
  version = '7.1.0',
  license='MIT',
  description = 'lib for the popular browsergame ogame',
  author = 'PapeprPieceCode',
  author_email = 'marcos.gam@hotmail.com',      # Type in your E-Mail
  url = 'https://github.com/PiecePaperCode/pyogame2',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/PiecePaperCode/pyogame2.git',    # I explain this later on
  keywords = ['OGame', 'lib', 'for bots'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
  ],
)