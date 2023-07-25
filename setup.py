from setuptools import setup, find_packages

setup(
    name='spicyy',
    version='0.6',
    url='https://github.com/michael7nightingale/spicy',
    install_requires=[],
    license='MIT',
    author='Michael Nightingale',
    author_email='suslanchikmopl@gmail.com',
    description='DOM parser for html, xml and other.',
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['tests', "main.py", ".pytest_cache", "flake8", ".gitignore"]),
    long_description=open('README.md').read(),
    zip_safe=False
)
