from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='asyncdl',  # How you named your package folder (MyLib)
        packages=['asyncdl'],  # Chose the same as "name"
        version='0.1.0',  # Start with a small number and increase it with every change you make
        license='mit',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
        description='asyncdl is a simple wrapper around the aiohttp Python library. Its aim is to simplify the process of securely downloading files in Python applications.',  # Give a short description about your library
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Makoto',  # Type in your name
        author_email='makoto+github@taiga.sh',  # Type in your E-Mail
        url='https://github.com/FujiMakoto/asyncdl/',  # Provide either the link to your github or to your website
        download_url='https://github.com/FujiMakoto/asyncdl/archive/0.1.0.tar.gz',
        keywords=['aiohttp', 'downloading', 'http', 'requests'],  # Keywords that define your package best
        install_requires=[
            'aiohttp',
            'aiodns'
        ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Multimedia :: Graphics',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Security',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9'
        ],
)
