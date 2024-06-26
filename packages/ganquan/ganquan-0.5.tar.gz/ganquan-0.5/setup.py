from setuptools import setup, find_packages

setup(
    name='ganquan',
    version='0.5',
    description="this is a tesk package",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
    ],
    packages=find_packages(),
)
