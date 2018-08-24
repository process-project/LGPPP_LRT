from setuptools import setup
 
def readme():
    with open('README.md') as f:
        return f.read()
 
setup(
    name='LRT',    # This is the name of your PyPI-package.
    version='0.1',                          # Update the version number for new releases
)
