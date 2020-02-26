import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dashboard',
    version='0.0.1',
    author='Michael Elliott et al',
    author_email='robotzapa@gmail.com',
    description='A framework for creating a cluster of data visualizers and controls.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/RobotZapa/Dashboard',
    packages=setuptools.find_packages()
)
