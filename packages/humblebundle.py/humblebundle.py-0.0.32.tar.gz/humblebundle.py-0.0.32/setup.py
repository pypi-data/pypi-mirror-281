from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.32'
DESCRIPTION = 'HumbleBundle.com unofficial web interaction.'
LONG_DESCRIPTION = 'A package that allows you to interact with HumbleBundle.com to pull retrieve data such as bundles, humble choice, etc.'

# Setting up
setup(
    name="humblebundle.py",
    version=VERSION,
    author="ghostapps",
    #author_email="<mail@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'humblebundle', 'games', 'webapi'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)