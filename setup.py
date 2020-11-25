from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
    name='particle-playground',
    version='1.0',
    license="MIT",
    description='An open-source 2D particle simulator written in python.',
    long_description=long_description,
    author='William Boeckman',
    author_email='wmboeckman@gmail.com',
    url="https://www.wmboeckman.com/",
    packages=['particle_playground'],  # same as name
    # install_requires=['bar', 'greek'],  # external packages as dependencies
)
