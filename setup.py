try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst', "r", encoding="utf8") as file:
    long_description = file.read()

setup(
    name='nairaland',
    version='0.1.0',
    description='Fetches and parses data from Nairaland.',
    long_description=long_description,
    author='Zacchaeus Bolaji',
    author_email='djunehor@gmail.com',
    url='https://github.com/makinde2013/pynairaland',
    packages=['nairaland'],
    install_requires=[
        "beautifulsoup4==4.4.0",
		"feedparser==5.2.1",
		"future==0.16.0",
		"requests==2.21.0",
		"dateparser",
		"selenium"
    ]
)