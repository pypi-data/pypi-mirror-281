from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.1'
DESCRIPTION = 'Streaming msic data via neural networks'
LONG_DESCRIPTION = 'A package used for music to used in neural networks'

# Setting up
setup(
    name="DeepMusicshot",
    version=VERSION,
    author="ZXEcoder",
    author_email="<surajjha@gmail.com>",
    description=DESCRIPTION,
   
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'music', 'stream', 'neural networks', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)