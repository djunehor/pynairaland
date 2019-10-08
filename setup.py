try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst', 'r', encoding="utf-8") as file:
    long_description = file.read()

setup(
    name='nairaland',
    version='1.0.1',
    description='Fetches and parses data from Nairaland.',
    long_description=long_description,
    author='Zacchaeus Bolaji',
    author_email='djunehor@gmail.com',
    url='https://github.com/djunehor/pynairaland',
    packages=['nairaland'],
    install_requires=[
        "beautifulsoup4==4.4.0",
		"feedparser==5.2.1",
		"requests==2.21.0",
		"dateparser",
		"selenium",
        "lxml"
    ]
)