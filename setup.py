from setuptools import setup, find_packages


__version__ = "0.0.1"


setup(
    # package name in pypi
    name='formulaparser',
    # extract version from module.
    version=__version__,
    description="Parse an arythmic formula from a string",
    long_description=open('README.rst').read(),
    classifiers=[],
    keywords='',
    author='Lars van de Kerkhof',
    author_email='lars@permanentmarkers.nl',
    url='https://github.com/specialunderwear/python-formulaparser',
    license='GPL v3',
    # include all packages in the egg, except the test package.
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    # include non python files
    include_package_data=True,
    zip_safe=False,
    # specify dependencies
    install_requires=[
        'setuptools',
        'pyparsing'
    ],
)
