from setuptools import setup, find_packages

setup(
    name='rmrag',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Lasse Tranekjær Leed',
    author_email='lasseleed@gmail.com',
    description='RAG functions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9']
)