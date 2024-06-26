from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ampari",
    version="0.1.5",
    install_requires=[
        'requests'                   
    ],
    extras_require={
        "dev": ["twine>=5.1.0"]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
)
