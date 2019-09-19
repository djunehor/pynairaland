try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README') as file:
    long_description = file.read()

setup(
    name='quora',
    version='0.1.22',
    description='Fetches and parses data from Nairaland.',
    long_description=long_description,
    author='Zacchaeus Bolaji',
    author_email='djunehor@gmail.com',
    url='https://github.com/makinde2013/pynairaland',
    packages=['nairaland'],
    install_requires=[
        "beautifulsoup4 == 4.3.2",
        "feedparser == 5.1.3",
        "requests == 2.5.0"
    ]
)