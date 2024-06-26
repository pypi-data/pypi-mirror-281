from setuptools import setup, find_packages

setup(
    name='ganquan',
    version='0.4',
    description="this is a tesk package",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    license='Apache-2.0',
    packages=find_packages(),
)
