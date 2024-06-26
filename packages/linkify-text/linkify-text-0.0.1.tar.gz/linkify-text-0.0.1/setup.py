from io import open
from setuptools import setup

version = '0.0.1'

description = """Python AI powered module for selecting links in text"""

setup(
    name = "linkify-text",
    version = version,
    author = "Gaduki",

    description = description,

    url = "https://github.com/Im-personal/processTextWithAI.git",
    packages = ['linkify-text'],
    install_requires = ['openai']

)
