from setuptools import setup, find_packages
 
def readme():
    with open('README.md') as f:
        return f.read()
 
setup(
    name='LRT',    # This is the name of your PyPI-package.
    version='0.1',                          # Update the version number for new releases
    packages=find_packages(),
    include_package_data=True
)
