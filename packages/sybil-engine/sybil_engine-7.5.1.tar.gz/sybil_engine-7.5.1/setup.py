from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as file:
    requirements = file.readlines()

setup(
    name='sybil_engine',
    version='7.5.1',
    py_modules=['sybil_engine'],
    packages=find_packages(),
    install_requires=requirements,
    data_files=[('', ['requirements.txt'])],
    author='Indeoo',
    author_email='indeooars@gmail.com',
    description='Engine for web3 smart contracts automatization.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Indeoo/sybil-engine/',
)
