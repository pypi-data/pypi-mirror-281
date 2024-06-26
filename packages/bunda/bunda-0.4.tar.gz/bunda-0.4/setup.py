from setuptools import setup, find_packages

setup(
    name='bunda',
    version='0.4',
    packages=find_packages(),
       install_requires=[],
    author='bunda',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', 
    author_email='bunda@bunda.com',
    description='bunda',
    url='https://github.com/bunda/bunda',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
