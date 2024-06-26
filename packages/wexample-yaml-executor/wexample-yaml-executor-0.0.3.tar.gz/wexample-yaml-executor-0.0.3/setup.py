from setuptools import setup, find_packages

setup(
    name='wexample-yaml-executor',
    version=open('version.txt').read(),
    author='weeger',
    author_email='contact@wexample.com',
    description='Helper to execute commands based on yaml content',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wexample/python-workspaces',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pydantic'
    ],
    python_requires='>=3.6',
)
