from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='sealevelrise',
    version='0.3.0',
    description='Model for sea level rise using height map data.',
    long_description=readme,
    author='Riley Krall',
    author_email='rileykrall@gmail.com',
    url='https://github.com/rileykrall/ICM-2020-Problem-F-Model',
    license=license,
    packages=find_packages(exclude=('doc'))
)
